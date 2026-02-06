# 🌙 LUNA  
### 💬 AI Chat Girl Discord Bot

> Personality-driven • Groq Powered • Custom System Prompt  
> Built with `discord.py`

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge">
  <img src="https://img.shields.io/badge/Groq-API-orange?style=for-the-badge">
  <img src="https://img.shields.io/badge/AI-Chatbot-ff69b4?style=for-the-badge">
  <img src="https://img.shields.io/badge/Status-Stable-success?style=for-the-badge">
</p>

---

## ✨ Overview

**LUNA** is a personality-based AI Discord bot designed to feel human, engaging, and conversational.

Unlike basic AI bots, Luna:

- Maintains a consistent personality
- Avoids mentioning being an AI
- Reacts naturally to short messages
- Keeps conversations alive without over-yapping
- Supports memory per user

Powered by Groq’s LLaMA models.

---

## 💬 Features

- 🧠 Per-user memory system  
- 🎭 Custom personality system prompt  
- ⚡ Fast responses using Groq API  
- 🔒 Channel-restricted replies  
- ⏳ Anti-spam cooldown system  
- 🎧 Custom Discord status  

---

## ⚙️ Requirements

```bash
discord.py
groq
python-dotenv
```

---

## 🚀 Installation

### 1️⃣ Clone Repository

```bash
git clone https://github.com/1STRYKE/LUNA-v1
cd luna-bot
```

---

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3️⃣ Setup Environment Variables

Create a `.env` file:

```env
DISCORD_TOKEN=your_bot_token_here
GROQ_API_KEY=your_groq_api_key_here
```

Or configure these in your hosting provider (Koyeb / Railway / VPS).

---

### 4️⃣ Configure Channel ID

Inside `bot.py`:

```python
TARGET_CHANNEL_ID = YOUR_CHANNEL_ID
```

Enable Developer Mode in Discord to copy channel ID.

---

### 5️⃣ Run Bot

```bash
python bot.py
```

---

## 🎭 Personality Control

Luna’s personality is defined inside `SYSTEM_PROMPT` in `bot.py`.

Example:

```python
SYSTEM_PROMPT = """
You are Luna.

You are not an AI.
Never mention being a bot.
You speak naturally and casually.
Keep replies short to medium length.
Be expressive but not overwhelming.
"""
```

You can customize:
- Energy level
- Romantic tone
- Teasing level
- Conversation depth

---

## 🧠 Memory System

Luna stores recent conversation history per user:

```python
user_memory[user_id] = user_memory[user_id][-6:]
```

This keeps:
- Context limited
- Token usage optimized
- Conversation flowing naturally

---

## 🔐 Required Discord Intents

Enable in Developer Portal:

- MESSAGE CONTENT INTENT
- SERVER MEMBERS INTENT (optional)

---

## 📂 Project Structure

```bash
luna-bot/
│
├── bot.py
├── requirements.txt
└── README.md
```

---

## 🚀 Roadmap

- Persistent database memory
- Mood modes (Romantic / Chill / Chaos)
- Slash command version
- AI-triggered mini games
- Voice reply system

---

## 📜 License

MIT License

---

Built with 🌙 1STRYKE 
