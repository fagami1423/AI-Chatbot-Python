# 🤖 AI Customer Support Chatbot (FastAPI + PyTorch + MongoDB)

An intent-based NLP chatbot that answers customer questions automatically. Admins manage the training questions and answers through a REST API, then retrain the model with one call.

![Python](https://img.shields.io/badge/Python-3.8-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?logo=pytorch&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-47A248?logo=mongodb&logoColor=white)

## ✨ Features
- **Intent classification:** a 3-layer feed-forward neural network in PyTorch over bag-of-words features
- **NLP preprocessing** with NLTK (tokenization and stemming)
- **Confidence threshold:** answers only when the prediction confidence is above 75%, and otherwise falls back to a polite "I don't understand"
- **Retrain from the API:** `GET /train` rebuilds the model from the intents stored in MongoDB
- **CRUD APIs** for questions/intents and products, with Swagger docs
- **Web chat UI** served by FastAPI (Jinja2 template and static CSS)

## 🧠 Architecture
```
Browser chat UI ──POST /chat──► FastAPI ──► tokenize + stem (NLTK) ──► bag-of-words
                                                                    │
                    response ◄── intent lookup ◄── PyTorch NeuralNet ◄┘
                                     ▲
             MongoDB (intents, products) ──GET /train──► retrain & save data.pth
```

## 🔌 API endpoints
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Chat web interface |
| `POST` | `/chat` | Send a message and get the bot's reply |
| `GET` | `/train` | Retrain the model from MongoDB intents |
| `GET/POST/PUT/DELETE` | `/questions`, `/{id}` | Manage training intents |
| `GET/POST/PUT/DELETE` | `/products`, `/{id}` | Manage the product catalogue |

Interactive docs are at `http://127.0.0.1:8000/docs`.

## 🚀 Getting started
```bash
git clone https://github.com/fagami1423/AI-Chatbot-Python.git
cd AI-Chatbot-Python
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```
Create a `.env` file with your own MongoDB connection details:
```
MONGO_USERNAME=your_user
MONGO_PASS=your_password
MONGO_DATABASE=your_database
```
Run the server:
```bash
uvicorn main:app --reload
```
Then open http://127.0.0.1:8000.

## 📁 Project structure
```
├── main.py            # FastAPI app and router registration
├── model.py           # PyTorch NeuralNet (3 linear layers + ReLU)
├── train.py           # Training loop
├── chat.py            # Inference and response selection
├── nltk_utils.py      # Tokenize, stem, bag-of-words
├── database.py        # MongoDB connection
├── question/          # Intent models, schemas, routes
├── product/           # Product models, schemas, routes
└── templates/, static/  # Chat UI
```

## 🛣️ Roadmap
- [ ] Replace bag-of-words with sentence embeddings
- [ ] Add retrieval-augmented generation (RAG) for open-ended answers
- [ ] Docker Compose setup (API + MongoDB)

## 👤 Author
**Raj Kumar Phagami**: [GitHub](https://github.com/fagami1423)
