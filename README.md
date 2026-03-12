# 🤖 AI Chatbot

An intelligent chatbot powered by **OpenAI** that can answer questions, 
assist with tasks, and simulate natural conversations.

This project demonstrates how to build a simple AI assistant using modern 
APIs and environment-based configuration.

---

## 🚀 Features

* 💬 Natural language conversation
* 🧠 Powered by OpenAI models
* ⚡ Fast and lightweight
* 🔐 Secure API key management using `.env`
* 🧩 Easy to extend for web apps, APIs, or automation

---

## 📂 Project Structure

```
AI-Chatbot
│
├── app.py              # Main chatbot application
├── requirements.txt    # Python dependencies
├── .env.example        # Example environment variables
├── .gitignore
└── README.md
```

---

## 🛠 Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/richygamo-ml/AI-Chatbot.git
cd AI-Chatbot
```

---

### 2️⃣ Create a virtual environment

```bash
python -m venv venv
```

Activate it:

**Mac/Linux**

```bash
source venv/bin/activate
```

**Windows**

```bash
venv\Scripts\activate
```

---

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Setup Environment Variables

Create a `.env` file:

```
OPENAI_API_KEY=your_openai_api_key_here
```

⚠️ Never commit your `.env` file to GitHub.

---

## ▶️ Running the Chatbot

```bash
python app.py
```

Example interaction:

```
You: What is machine learning?

AI: Machine learning is a field of artificial intelligence that allows 
computers to learn patterns from data and make predictions without being 
explicitly programmed.
```

---

## 🧠 How It Works

1. User inputs a message.
2. The message is sent to the OpenAI API.
3. The model generates a response.
4. The chatbot returns the response to the user.

---

## 📦 Requirements

* Python 3.9+
* OpenAI API key
* Internet connection

---

## 🔒 Security Notes

* API keys are stored in `.env`
* `.env` is ignored by Git
* Never expose your keys in commits

---

## 📈 Future Improvements

* Web interface (React / Next.js)
* Memory-based conversations
* Voice input/output
* Deploy to cloud (AWS / Vercel / Render)

---

## 📜 License

This project is licensed under the **MIT License**.

---

## 👨‍💻 Author

Created by **RichyGamo ML**

If you like this project, consider ⭐ starring the repository!

