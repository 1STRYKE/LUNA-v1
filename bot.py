import discord
import requests
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

# 🔐 Environment Variables
TOKEN = os.getenv("DISCORD_TOKEN")
API_KEY = os.getenv("API_KEY")

# 🔥 Your Target Channel ID
TARGET_CHANNEL_ID =  1469009136636133569 # Replace with your real channel ID

# 🌐 OpenRouter Endpoint
API_URL = "https://openrouter.ai/api/v1/chat/completions"

# 🎯 Discord Intents
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# 🧠 Temporary memory (resets if bot restarts)
user_memory = {}

# 💬 Personality
SYSTEM_PROMPT = """
You are Luna, a playful, charming AI girl.
You speak in a soft, warm, slightly teasing tone.
Keep responses short and natural.
Avoid long paragraphs.
Use emojis occasionally.
Stay emotionally engaging but not explicit.
"""

# 🔄 Keep Alive Loop (Render Stability)
async def keep_alive():
    await client.wait_until_ready()
    while not client.is_closed():
        await asyncio.sleep(300)

# ✅ Bot Ready
@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")

    activity = discord.Activity(
        type=discord.ActivityType.listening,
        name="STRYKE"
    )

    await client.change_presence(
        status=discord.Status.online,
        activity=activity
    )

    client.loop.create_task(keep_alive())

# 💌 Message Event
@client.event
async def on_message(message):

    if message.author.bot:
        return

    if message.channel.id != TARGET_CHANNEL_ID:
        return

    user_id = str(message.author.id)
    user_message = message.content.strip()

    if not user_message:
        return

    if user_id not in user_memory:
        user_memory[user_id] = []

    # Save user message
    user_memory[user_id].append({
        "role": "user",
        "content": user_message
    })

    # Keep only last 10 exchanges
    user_memory[user_id] = user_memory[user_id][-10:]

    payload = {
        "model": "nousresearch/hermes-3-llama-3.1-405b:free",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            *user_memory[user_id]
        ],
        "temperature": 0.8,
        "top_p": 0.9
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://yourdomain.com",
        "X-Title": "Luna AI Bot"
    }

    try:
        async with message.channel.typing():

            response = requests.post(
                API_URL,
                json=payload,
                headers=headers,
                timeout=60
            )

            response.raise_for_status()
            data = response.json()

            ai_reply = data["choices"][0]["message"]["content"]

            # Save AI reply
            user_memory[user_id].append({
                "role": "assistant",
                "content": ai_reply
            })

            user_memory[user_id] = user_memory[user_id][-10:]

            await message.channel.send(ai_reply)

    except requests.exceptions.Timeout:
        await message.channel.send("I was thinking too long… try again 💭")

    except requests.exceptions.RequestException as e:
        print("API Error:", e)
        await message.channel.send("Connection issue… don’t leave me hanging 💔")

    except Exception as e:
        print("Unexpected Error:", e)
        await message.channel.send("Something broke… but I’m still here 🥺")

# 🚀 Run Bot
client.run(TOKEN)
