# AudioTranscribe
# WhisperTranscribe

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.31.0-FF4B4B.svg)](https://streamlit.io/)

## 🎙️ Audio Transcription Web App Powered by Faster Whisper

WhisperTranscribe is a user-friendly web application built with Streamlit that leverages the speed and accuracy of Faster Whisper, an optimized implementation of OpenAI's Whisper model, to transcribe audio files to text. This tool provides a simple interface for uploading audio files, transcribing them, and exporting the results in different formats.

![WhisperTranscribe Demo](demo-placeholder.gif)

## ✨ Features

- **Multi-format Audio Support**: Transcribe MP3, WAV, and M4A audio files
- **Model Selection**: Choose from various Whisper model sizes (tiny, base, small, medium, large-v2)
- **Hardware Optimization**: Select between CPU and GPU processing (when available)
- **Precision Control**: Fine-tune performance with different compute precision options
- **Language Detection**: Automatic language detection or manual selection for improved accuracy
- **Export Options**: Save transcriptions as text files or formatted PDFs
- **User-friendly Interface**: Clean, responsive design with progress indicators and error handling

## 🚀 Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/whispertranscribe.git
   cd whispertranscribe
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 📋 Requirements

Create a `requirements.txt` file with the following dependencies:

```
streamlit>=1.31.0
faster-whisper>=0.9.0
fpdf>=1.7.2
```

## 🖥️ Usage

1. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

2. Open your web browser and navigate to the provided local URL (typically http://localhost:8501)

3. Upload an audio file, select your preferred model and settings, and click "Transcribe Audio"

4. Once transcription is complete, view the results and download in your preferred format

## 🔧 Technical Details

WhisperTranscribe utilizes Faster Whisper, which offers significant speed improvements over the original Whisper implementation through:

- **CTranslate2 Backend**: An optimized inference engine written in C++ with GPU acceleration
- **Weight Quantization**: Support for various precision levels (int8, float16, float32)
- **Efficient Processing**: Optimized memory usage and processing techniques
- **Fallback Mechanisms**: Graceful handling of hardware limitations with automatic fallbacks

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

- [OpenAI's Whisper](https://github.com/openai/whisper) - The original speech recognition model
- [Faster Whisper](https://github.com/guillaumekln/faster-whisper) - The optimized implementation of Whisper
- [Streamlit](https://streamlit.io/) - The framework used to build the web application

---

Made by Rohin Pithwa
