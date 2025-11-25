# PROTOCOL: ORACLE_v1

A cyberpunk-themed AI-powered Tarot reading application built with Streamlit and powered by Google Gemini AI.

## 🌟 Features

- **AI-Powered Readings**: Dynamic, personalized Tarot interpretations using Google Gemini API
- **Techno-Gnostic Aesthetic**: Glitchy, terminal-inspired UI with neon green accents
- **22 Major Arcana Cards**: Full deck with rich symbolic meanings
- **Interactive Experience**: Text glitch effects, boot sequences, and streaming prophecies

## 🚀 Quick Start (Local)

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up your Google API Key:
   - Get a key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Add to `.streamlit/secrets.toml`:
     ```toml
     GOOGLE_API_KEY = "your-key-here"
     ```

3. Run the app:
   ```bash
   streamlit run main.py
   ```

## ☁️ Deploy to Streamlit Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo
4. In **Settings > Secrets**, add:
   ```toml
   GOOGLE_API_KEY = "your-key-here"
   ```

## 📁 Project Structure

```
protocol_oracle/
├── main.py              # Main Streamlit application
├── card_library.py      # Tarot card definitions & meanings
├── style.css            # Custom CSS (terminal aesthetic)
├── requirements.txt     # Python dependencies
└── assets/
    └── cards/           # Card images (.gif or .png)
```

## 🔮 How It Works

1. **Draw Cards**: Click "INITIALIZE SEQUENCE" to pull 3 random cards
2. **AI Analysis**: The Google Gemini API generates a unique reading based on:
   - Card archetypes
   - Techno-gnostic symbolism
   - Optional user query
3. **Glitch Effect**: Watch words flicker between human language and "machine code"

## 🎨 Customization

- **Card Images**: Add your own to `assets/cards/` (name format: `the_fool.gif`)
- **Glitch Vocabulary**: Edit `GLITCH_VOCAB` in `main.py`
- **Prompts**: Modify the AI prompt in `generate_interpretation()`
- **Styling**: Tweak `style.css` for different aesthetics

## 📜 License

This project is open source. Feel free to fork and modify!

## 💰 Support

If you enjoy this project, consider [supporting development](https://paypal.me/ryjedwards).

---

**WAKE UP, SEEKER. THE SIMULATION AWAITS.**
