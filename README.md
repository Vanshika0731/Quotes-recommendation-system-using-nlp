# 💬 Quotes Recommendation Chatbot — Rasa NLU

> An intelligent conversational chatbot that recommends personalized quotes based on your mood and preferences, powered by **Rasa NLU** and accessible via a browser-based web interface.

---

## 📌 Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
- [Running the Chatbot](#running-the-chatbot)
- [Using the Web Interface](#using-the-web-interface)
- [Supported Intents](#supported-intents)
- [Quote Categories](#quote-categories)
- [Training the NLU Model](#training-the-nlu-model)
- [Testing](#testing)
- [Screenshots](#screenshots)
- [Future Enhancements](#future-enhancements)
- [License](#license)

---

## 📖 Project Overview

The **Quotes Recommendation Chatbot** is a guided project built using **Rasa Open Source NLU**. It understands natural language inputs from users, detects their intent and emotional context, and responds with contextually appropriate quotes from a curated database across 5 categories: Inspiration, Motivation, Success, Love, and Humor.

The chatbot supports multi-turn conversations and is integrated with a clean web frontend via Rasa's REST API channel.

---

## ✨ Features

- 🧠 **NLU-Powered Understanding** — Detects intent and mood from free-text input
- 💬 **Multi-turn Conversations** — Follow-up questions and satisfaction feedback
- 📚 **60+ Curated Quotes** — Across 5 emotional/thematic categories
- 🌐 **Web Interface** — Browser-based HTML/CSS/JS frontend
- 🔌 **REST API Integration** — Frontend ↔ Rasa backend over HTTP
- 🎲 **Random Quote Mode** — Surprise selection across all categories
- 🔄 **Quote Rotation** — Never repeats the same quote in a session
- 🛡️ **Demo Mode** — Works offline if Rasa server is not running

---

## 🛠️ Tech Stack

| Technology     | Version  | Purpose                          |
|---------------|----------|----------------------------------|
| Rasa Open Source | 3.6.x | NLU & Dialogue Management       |
| Python         | 3.8+     | Backend logic & custom actions  |
| TensorFlow     | 2.12     | ML model training                |
| spaCy          | 3.6      | Tokenization & NLP features     |
| HTML/CSS/JS    | Vanilla  | Web chat frontend                |
| REST API       | HTTP/JSON| Frontend-backend communication  |

---

## 📁 Project Structure

```
quotes-chatbot/
│
├── data/
│   ├── nlu.yml          # NLU training examples (intents + utterances)
│   ├── stories.yml      # Multi-turn conversation flows
│   └── rules.yml        # Rule-based dialogue triggers
│
├── actions/
│   ├── __init__.py
│   └── actions.py       # Custom actions + quote database (60+ quotes)
│
├── frontend/
│   └── index.html       # Web chat interface (self-contained)
│
├── models/              # Trained Rasa model files (generated after training)
├── results/             # NLU evaluation results
│
├── domain.yml           # Intents, entities, slots, responses, actions
├── config.yml           # NLU pipeline & policy configuration
├── credentials.yml      # REST API channel setup
├── endpoints.yml        # Custom action server endpoint
├── requirements.txt     # Python dependencies
├── .gitignore
└── README.md
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 – 3.10
- pip
- Git

### Step 1: Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/quotes-chatbot.git
cd quotes-chatbot
```

### Step 2: Create a Virtual Environment
```bash
python -m venv venv

# Activate on Windows:
venv\Scripts\activate

# Activate on macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

> **Note:** Rasa installation may take 5–10 minutes. Ensure you have at least 4GB of RAM.

---

## ▶️ Running the Chatbot

### Train the NLU Model (required once, or after data changes)
```bash
rasa train
```
This will create a model file in the `models/` directory.

### Start the Action Server (in Terminal 1)
```bash
rasa run actions
```

### Start the Rasa Server with REST API (in Terminal 2)
```bash
rasa run --enable-api --cors "*"
```

The server will start at `http://localhost:5005`.

### Optional: Test in CLI
```bash
rasa shell
```

---

## 🌐 Using the Web Interface

1. Make sure both the action server and Rasa server are running (see above)
2. Open `frontend/index.html` in your browser
3. Start chatting!

> **Demo Mode:** If the Rasa server is not running, the frontend automatically falls back to a built-in demo mode that simulates responses locally.

---

## 🧩 Supported Intents

| Intent                  | Example Utterances                                      |
|------------------------|--------------------------------------------------------|
| `greet`                | "Hi", "Hello", "Hey there"                             |
| `ask_inspiration`      | "Inspire me", "I need a positive quote"                |
| `ask_motivation`       | "Motivate me", "I need to keep going"                  |
| `ask_success`          | "Quote about success", "Help me achieve my goals"      |
| `ask_love`             | "Give me a love quote", "Something romantic"           |
| `ask_humor`            | "Funny quote", "Make me laugh", "Cheer me up"          |
| `ask_random`           | "Surprise me", "Random quote", "Your choice"           |
| `ask_another`          | "Give me another", "One more please", "Next"           |
| `express_satisfaction` | "That was great", "I loved it", "Perfect"              |
| `express_dissatisfaction` | "Not really", "Try again", "Something else"        |
| `goodbye`              | "Bye", "See you", "Goodbye"                            |

---

## 📚 Quote Categories

| Category      | Emoji | Count | Theme                        |
|--------------|-------|-------|------------------------------|
| Inspiration  | ✨    | 12    | Hope, wisdom, uplifting words |
| Motivation   | ⚡    | 12    | Drive, persistence, energy   |
| Success      | 🏆    | 12    | Achievement, hard work, goals |
| Love         | 💛    | 12    | Affection, compassion, heart |
| Humor        | 😄    | 12    | Wit, laughter, lighthearted  |

---

## 🧪 Training the NLU Model

```bash
# Train full model (NLU + Core)
rasa train

# Train NLU only
rasa train nlu

# Evaluate NLU performance
rasa test nlu --nlu data/nlu.yml

# Evaluate dialogue (Core)
rasa test core --stories data/stories.yml
```

---

## 🧪 Testing

```bash
# Run NLU tests
rasa test nlu

# Check if a sentence is classified correctly
rasa shell nlu

# Validate training data
rasa data validate
```

---

## 🔮 Future Enhancements

- [ ] Sentiment analysis integration for deeper emotional understanding
- [ ] External quote API integration (Quotable, ZenQuotes)
- [ ] User profile and favorite quote saving
- [ ] Voice input/output via Web Speech API
- [ ] Multi-language support
- [ ] Analytics dashboard for intent tracking
- [ ] Mobile app (Progressive Web App)

---

## 📄 License

This project is developed as part of a guided internship program. Free to use for educational purposes.

---

## 🙌 Acknowledgements

- [Rasa Open Source](https://rasa.com/) — NLU & Dialogue Framework
- Guided Project Program — Project structure and mentorship
- Quote sources — Various public domain collections
