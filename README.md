# Friday - Secure, Local-First Voice Assistant

Friday is a secure, local-first virtual assistant built to automate web workflows, play custom music tracking indexes, aggregate regional news, and handle open conversational requests privately. The software architecture eliminates traditional data privacy concerns by locking operations down within an isolated execution system.

---

## 📋 Comprehensive Feature Specification

### 🎙️ Core Interaction Engine
* **Phonetic Wake-Word Trigger**: Monitors your microphone locally for the word "Friday". It uses sharp consonant detection to initiate the command phase without false positives.
* **Dual-Stage Mic Gating**: Prevents audio overlapping by opening the microphone channel for the wake-word, closing it to say "Ya", and reopening it specifically to catch your action command.
* **Audio Driver Anti-Lockup**: Initializes a dedicated, temporary `pyttsx3` text-to-speech framework for every spoken sentence, completely isolating and destroying the memory allocation right after to avoid audio freezing.

### ⚙️ Operational Features
* **🎯 Local AI Brain (Ollama Integration)**: Offloads general user conversations to a local deployment of the `llama3.1` model. This structure ensures zero text logs or prompt leakages are broadcasted across the web.
* **🎵 Custom Music Playback**: Instantly scans your local `musiclibrary.py` file to resolve song keywords into specific web URLs and auto-launches them.
* **📰 Live Regional News Aggregator**: Authenticates via a hidden `.env` token to `newsdata.io` to gather current Indian English headlines. It dynamically sanitizes the raw API payload text by replacing symbols with spoken phrases to maintain voice cadence.
* **🌐 Web Workspace Automation**: Direct voice shortcuts mapping to system default browser executions for global developer platforms (Google, YouTube, GitHub, and LinkedIn).

### 🔒 Enterprise-Grade Security Architecture
* **🛡️ True AES-256 Symmetric Encryption**: Replaces standard Fernet protocols with high-grade `pycryptodome` encryption. Your conversation data is heavily guarded at-rest via Cipher Block Chaining (CBC) combined with unique initialization vectors (IV).
* **⏳ 24-Hour Automated Purge Ecosystem**: Implements an active memory-decay feature. Every history request triggers a strict log file rewrite, permanently deleting entries with tracking timestamps older than 86,400 seconds.
* **🔑 Zero-Hardcode Environment**: Keeps critical keys completely hidden in local `.env` storage, perfectly isolated within a dedicated Python `venv` context to secure third-party library boundaries.

### 🎭 AI Behavioral Constraints & Persona
The integrated local LLM processes text under an ironclad system prompt structure designed for optimized vocal delivery:
* **Identity**: Behaves exclusively as a polite, structured assistant named Friday.
* **Length Constraints**: Restricts the maximum response ceiling strictly to 2–3 text lines to keep audio playback short and focused.
* **Language Profiling**: Uses clear, simple, and naturally recognizable Indian English words to match regional speech expectations perfectly.

---

## 🛠️ System Prerequisites & Local LLM Setup

### 1. Ollama Installation
Friday processes general text reasoning locally using Ollama.

1. Download the executable client for your platform from [ollama.com](https://ollama.com).
2. Install the client and run the tool inside your system command line to pull the requested model:
   ```bash
   ollama pull llama3.1
   ```
3. Keep the Ollama system background service running while executing your voice assistant script.

### 2. Audio Processing Drivers (Linux/Debian Systems)
If you run Friday on Linux, compile the underlying system sound wrappers before building your Python virtual environment:
```bash
sudo apt-get update && sudo apt-get install espeak portaudio19-dev python3-pyaudio
```

---

## 🚀 Environment Initialization & Installation

Follow these explicit developer steps to initialize Friday inside an isolated runtime wrapper:

### Step 1: Create an Isolated Python Virtual Environment (`venv`)
```bash
# Create target venv folder
python -m venv venv

# Activate venv on Windows (CMD):
venv\Scripts\activate
# Activate venv on Windows (PowerShell):
venv\Scripts\Activate.ps1
# Activate venv on Linux / macOS:
source venv/bin/activate
```

### Step 2: Clean Dependency Standardization
To fix configuration inconsistencies caused by raw `pip freeze` logs, use a clean, platform-agnostic, top-level `requirements.txt`. Save the lines below as your **`requirements.txt`**:

```text
speechrecognition
pyttsx3
requests
ollama
python-dotenv
pycryptodome
pyaudio
```

Execute the installation block inside your activated environment:
```bash
pip install -r requirements.txt
```

### Step 3: Populate Local Secrets (`.env`)
Create a hidden file named `.env` in your project root folder and specify your operational configurations:
```env
# Encryption Key (Must be exactly 32 alphanumeric characters for AES-256)
FERNET_KEY=MySecret32CharacterKeyForAES256!

# External News Token
NEWS_API_KEY=your_newsdata_api_token_here
```

---

## 🏃 Running Friday

1. Boot up your workspace and launch the core program file:
   ```bash
   python main.py
   ```
2. Call out "**Friday**". The terminal logs the audio detection step and the voice driver plays back a validation voice bite ("**Ya**").
3. Speak an automated action phrase (like `"open github"`, `"news"`, or `"history"`) or ask an open question to stream a customized local AI response.
