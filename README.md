# 🎙️ AI-Powered Audio Summarizer

A sophisticated audio summarization tool that leverages OpenAI's Whisper (via whisper.cpp) and Ollama's language models to convert various types of audio content into detailed, contextualized summaries.

## 🚀 Features

- **Multi-Format Audio Support**: Process various audio types including:
  - Meeting Recordings
  - Songs
  - Lectures
  - Podcasts
  - Interviews
  - Audiobooks
  - Voice Memos
  - Conference Talks

- **Advanced AI Integration**:
  - Whisper.cpp for efficient speech-to-text conversion
  - Ollama for intelligent summary generation
  - Context-aware summarization

- **Customizable Processing**:
  - Multiple Whisper model options
  - Flexible Ollama model selection
  - Optional context input for better summaries

- **User-Friendly Interface**:
  - Built with Streamlit
  - Real-time processing status
  - Downloadable transcripts
  - Intuitive settings panel

## 🛠️ Prerequisites

1. **FFmpeg**
   - Download and install FFmpeg from [official website](https://ffmpeg.org/download.html)
   - Add FFmpeg to your system PATH

2. **Ollama**
   - Download and install Ollama from [Ollama's website](https://ollama.ai/)
   - Run Ollama server locally (default port: 11434)

3. **Whisper.cpp**
   - Clone the whisper.cpp repository:
     ```bash
     git clone https://github.com/ggerganov/whisper.cpp.git
     ```
   - Follow whisper.cpp build instructions in their repository
   - Download desired model(s) to the models directory

4. **Python 3.8+**

## 🔧 Installation

1. **Clone this repository**:
   ```bash
   git clone https://github.com/malav-250/AI-Powered-Audio-Summarizer-main.git
   cd AI-Powered-Audio-Summarizer-main
   ```

2. **Create and activate virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   venv\Scripts\activate     # Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Update paths in main2.py**:
   - Set correct path for FFmpeg
   - Update Whisper model directory path
   - Configure Ollama server URL if different
  
## Workflow Diagram

<img src="https://github-production-user-asset-6210df.s3.amazonaws.com/78475119/413510326-c80e8a96-8af9-4274-b437-05fa71dc1f02.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAVCODYLSA53PQK4ZA%2F20250215%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20250215T035000Z&X-Amz-Expires=300&X-Amz-Signature=7cb4a2a17d30d58065450b73cd1eb2d7bd1f1a856f2c4898f1a14bb7a7c72dae&X-Amz-SignedHeaders=host" alt="Description" width="600"/>


## 🚀 Usage

1. **Start Ollama server**:
   ```bash
   ollama serve
   ```

2. **Run the application**:
   ```bash
   streamlit run main2.py
   ```

3. **Use the interface**:
   - Select audio type
   - Choose Whisper and Ollama models
   - Upload audio file
   - Add optional context
   - Get your summary!

## 📝 Configuration

Update these constants in `main2.py` according to your setup:
```python
OLLAMA_SERVER_URL = "http://localhost:11434"
WHISPER_MODEL_DIR = "path/to/whisper/models"
FFMPEG_PATH = "path/to/ffmpeg"
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Whisper.cpp](https://github.com/ggerganov/whisper.cpp) for the efficient Whisper implementation
- [Ollama](https://ollama.ai/) for the local LLM capabilities
- [Streamlit](https://streamlit.io/) for the web interface

