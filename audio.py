import streamlit as st
import tempfile
import os
from faster_whisper import WhisperModel
from fpdf import FPDF
from datetime import datetime
import platform

# Set page configuration
st.set_page_config(
    page_title="Audio Transcription App",
    page_icon="🎙️",
    layout="wide"
)

# Create a title for the app
st.title("🎙️ Audio Transcription with Whisper AI")
st.markdown("Upload an audio file (MP3 or WAV) and get it transcribed to text.")

# Model selection
model_size = st.sidebar.selectbox(
    "Select Whisper Model Size",
    ["tiny", "base", "small", "medium", "large-v2"]
)

# Define compute type options based on platform
compute_options = ["auto", "cpu"]
if platform.system() != "Darwin" or not platform.machine().startswith("arm"):  # Not Apple Silicon
    compute_options.insert(1, "cuda")  # Add CUDA as an option for non-Apple Silicon

compute_type = st.sidebar.radio(
    "Select Compute Device",
    compute_options
)

# Define precision options
precision_type = st.sidebar.radio(
    "Select Compute Precision",
    ["auto", "float32", "float16", "int8"]
)

st.sidebar.info(
    "Model sizes from small to large offer increasing accuracy but require more processing time and resources. "
    "'tiny' and 'base' are fastest but less accurate. 'small' offers a good balance. "
    "'medium' and 'large-v2' are more accurate but slower."
)

# Language selection (optional)
language = st.sidebar.selectbox(
    "Select Language (Optional)",
    ["Auto-detect", "English", "Spanish", "French", "German", "Italian", "Portuguese", "Russian", "Chinese", "Japanese"]
)

language_code_map = {
    "Auto-detect": None,
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Italian": "it",
    "Portuguese": "pt",
    "Russian": "ru",
    "Chinese": "zh",
    "Japanese": "ja"
}

# Upload file
uploaded_file = st.file_uploader("Upload an audio file", type=["mp3", "wav", "m4a"])

# Initialize session state for transcription if not already done
if 'transcription' not in st.session_state:
    st.session_state.transcription = None
if 'filename' not in st.session_state:
    st.session_state.filename = None

# Function to generate PDF
def generate_pdf(text, filename):
    pdf = FPDF()
    pdf.add_page()
    
    # Set font
    pdf.set_font("Arial", size=12)
    
    # Add title
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, f"Transcription of {filename}", ln=True, align="C")
    pdf.ln(10)
    
    # Add timestamp
    pdf.set_font("Arial", "I", 10)
    pdf.cell(200, 10, f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    pdf.ln(10)
    
    # Add content
    pdf.set_font("Arial", size=12)
    
    # Split text into lines to avoid overflow
    pdf.multi_cell(0, 10, text)
    
    # Generate a filename for the PDF
    pdf_filename = f"transcription_{os.path.splitext(filename)[0]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    
    # Save the PDF
    pdf_path = os.path.join(tempfile.gettempdir(), pdf_filename)
    pdf.output(pdf_path)
    
    return pdf_path, pdf_filename

# Function to process audio and get transcription
def transcribe_audio(audio_file, model_size, compute_type, precision_type, language_code):
    try:
        with st.spinner(f"Loading Whisper model ({model_size})..."):
            # Initialize the model with proper error handling for compute type
            try:
                # If auto is selected for precision, let the library decide
                compute_precision = precision_type if precision_type != "auto" else None
                
                model = WhisperModel(model_size, device=compute_type, compute_type=compute_precision)
                st.info(f"Model loaded successfully using {compute_type} device with {model.compute_type} precision.")
            except Exception as e:
                st.warning(f"Failed to initialize with selected options: {str(e)}. Falling back to CPU with float32.")
                model = WhisperModel(model_size, device="cpu", compute_type="float32")
        
        with st.spinner("Transcribing audio... This may take a while depending on the file size and model."):
            # Save upload to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(audio_file.name)[1]) as tmp_file:
                tmp_file.write(audio_file.getvalue())
                tmp_path = tmp_file.name
            
            # Transcribe the audio
            transcribe_options = {}
            if language_code:
                transcribe_options["language"] = language_code
            
            segments, info = model.transcribe(tmp_path, beam_size=5, **transcribe_options)
            
            # Combine all segments into one text
            transcript = ""
            for segment in segments:
                transcript += segment.text + " "
            
            # Clean up the temporary file
            os.unlink(tmp_path)
            
            return transcript.strip()
    except Exception as e:
        st.error(f"An error occurred during transcription: {str(e)}")
        return None

# Transcribe button
if uploaded_file is not None:
    col1, col2 = st.columns([1, 1])
    with col1:
        st.audio(uploaded_file, format=f"audio/{os.path.splitext(uploaded_file.name)[1][1:]}")
    
    with col2:
        file_details = {
            "Filename": uploaded_file.name,
            "File size": f"{uploaded_file.size / (1024 * 1024):.2f} MB",
            "File type": uploaded_file.type
        }
        for key, value in file_details.items():
            st.write(f"**{key}:** {value}")
    
    if st.button("Transcribe Audio"):
        language_code = language_code_map[language]
        transcription = transcribe_audio(uploaded_file, model_size, compute_type, precision_type, language_code)
        
        if transcription:
            st.session_state.transcription = transcription
            st.session_state.filename = uploaded_file.name
            st.success("Transcription complete!")

# Display transcription if available
if st.session_state.transcription:
    st.subheader("Transcription Result")
    st.text_area("Transcribed Text", st.session_state.transcription, height=300)
    
    # Options to save as txt or pdf
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Save as Text File"):
            # Create a downloadable text file
            st.download_button(
                label="Download Text",
                data=st.session_state.transcription,
                file_name=f"transcription_{os.path.splitext(st.session_state.filename)[0]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )
    
    with col2:
        if st.button("Save as PDF"):
            with st.spinner("Generating PDF..."):
                pdf_path, pdf_filename = generate_pdf(st.session_state.transcription, st.session_state.filename)
                
                # Read the generated PDF file
                with open(pdf_path, "rb") as f:
                    pdf_data = f.read()
                
                # Create a download button for the PDF
                st.download_button(
                    label="Download PDF",
                    data=pdf_data,
                    file_name=pdf_filename,
                    mime="application/pdf"
                )
                
                # Delete the temporary PDF file
                os.unlink(pdf_path)

# Footer
st.markdown("---")
st.markdown("### How to use this app")
st.markdown("""
1. Upload an audio file (MP3, WAV, or M4A format)
2. Select the Whisper model size (tiny is fastest, large-v2 is most accurate)
3. Choose your compute device (CPU or GPU if available)
4. Select compute precision (float32 is most compatible)
5. Optionally select a language (if known) to improve transcription
6. Click 'Transcribe Audio' to process the file
7. Once transcription is complete, you can save it as a text file or PDF
""")

st.sidebar.markdown("---")
st.sidebar.markdown("### About")
st.sidebar.info(
    "This app uses Faster Whisper, an efficient implementation of OpenAI's Whisper model to transcribe audio files to text. "
    "The transcription quality depends on the model size and audio quality. "
    "For better results with non-English content, try selecting the specific language."
)