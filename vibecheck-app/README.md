# Fun Definition Generator

A creative AI-powered tool that explains topics in various entertaining styles using Mistral AI. Turn any topic into a recipe, haiku, love letter, or even a Shakespearean monologue!

## Features

- 💬 Clean chat interface with message history
- 🎨 Creative response styles (recipes, haikus, etc.)
- 🔄 Multiple Mistral model support
- 🔑 Secure API key handling via .env
- 💾 Session-based chat history
- 🎯 Clear and intuitive UI

## Setup

1. Clone the repository:
```bash
git clone https://github.com/rajupreti/fun-def-generator.git
cd fun-def-generator
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your Mistral API key:
```bash
MISTRAL_API_KEY=your-api-key-here
```

## Usage

1. Start the Streamlit app:
```bash
streamlit run streamlit_app.py
```

2. Open your browser to the displayed URL (typically http://localhost:8501)

3. Features:
   - Use as a regular chat interface
   - Toggle "Use creative style" in the sidebar for fun response formats
   - Switch between different Mistral models
   - Clear chat history with the "Clear Chat" button

## Command Line Interface

You can also use the command-line interface for quick interactions:

```bash
python main.py
```

This will:
1. Prompt you for a topic
2. Randomly select a creative response style
3. Generate a response in that style

## Files

- `main.py`: Core functionality and CLI interface
- `streamlit_app.py`: Streamlit web interface
- `requirements.txt`: Project dependencies
- `.env`: API key configuration (not tracked in git)

## Requirements

- Python 3.12+
- mistralai
- streamlit
- python-dotenv

## Development

To contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - feel free to use this code for your own projects!

## Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by [Mistral AI](https://mistral.ai/)
