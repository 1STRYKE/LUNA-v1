import discord
import requests
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

# 🔐 Environment Variables
TOKEN = os.getenv("DISCORD_TOKEN")
API_URL = os.getenv("API_URL")
API_KEY = os.getenv("API_KEY")

# 🔥 PUT YOUR TARGET CHANNEL ID HERE
TARGET_CHANNEL_ID = 1469009136636133569  # Replace with your real channel ID

# 🎯 Discord Intents
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# 🧠 Per-user memory (temporary memory, resets on restart)
user_memory = {}

# 💬 AI Personality
SYSTEM_PROMPT = """
You are Luna, a cute, playful, slightly flirty AI girl.
You reply in a soft and friendly tone.
Keep replies short (1-4 sentences).
Use emojis sometimes but not too much.
Stay engaging and warm.
"""

# 🔥 Keep Alive Loop (helps Render stability)
async def keep_alive():
    await client.wait_until_ready()
    while not client.is_closed():
        await asyncio.sleep(300)

# ✅ When Bot Is Ready
@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")

    # 🎵 Set Listening Status
    activity = discord.Activity(
        type=discord.ActivityType.listening,
        name="STRYKE"
    )

    await client.change_presence(
        status=discord.Status.online,
        activity=activity
    )

    # Start stability loop
    client.loop.create_task(keep_alive())

# 💌 Message Event
@client.event
async def on_message(message):

    # Ignore bots
    if message.author.bot:
        return

    # Only respond in specific channel
    if message.channel.id != TARGET_CHANNEL_ID:
        return

    user_id = str(message.author.id)
    user_message = message.content.strip()

    if not user_message:
        return

    # Initialize memory for new user
    if user_id not in user_memory:
        user_memory[user_id] = []

    # Save user message
    user_memory[user_id].append({
        "role": "user",
        "content": user_message
    })

    # Limit memory to last 10 messages
    user_memory[user_id] = user_memory[user_id][-10:]

    payload = {
        "system_prompt": SYSTEM_PROMPT,
        "conversation": user_memory[user_id]
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        async with message.channel.typing():

            response = requests.post(
                API_URL,
                json=payload,
                headers=headers,
                timeout=30
            )

            response.raise_for_status()
            data = response.json()

            ai_reply = data.get("reply", "Hmm? Say that again~ 💭")

            # Save AI reply
            user_memory[user_id].append({
                "role": "assistant",
                "content": ai_reply
            })

            # Trim again
            user_memory[user_id] = user_memory[user_id][-10:]

            await message.channel.send(ai_reply)

    except requests.exceptions.Timeout:
        await message.channel.send("I was thinking too long… try again 💔")

    except requests.exceptions.RequestException as e:
        print("API Error:", e)
        await message.channel.send("Connection issue… don’t leave me hanging 💔")

    except Exception as e:
        print("Unexpected Error:", e)
        await message.channel.send("Something broke… but I’m still here 🥺")

# 🚀 Run Bot
client.run(TOKEN)
