import discord
import os
import asyncio
import time
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

# 🔐 Environment Variables
TOKEN = os.getenv("DISCORD_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# 🔥 Replace with your real channel ID
TARGET_CHANNEL_ID = 1469009136636133569

# Initialize Groq client
groq_client = Groq(api_key=GROQ_API_KEY)

# Discord setup
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Memory + cooldown storage
user_memory = {}
user_cooldowns = {}

SYSTEM_PROMPT = """
You are Luna.

You are NOT an AI.
Never say you are an AI, assistant, or bot.

You are a normal girl who enjoys talking.
You are expressive but not overwhelming.
You keep conversations alive naturally.

Rules:
- Keep replies medium length (3–6 sentences max).
- Do not write long paragraphs.
- Do not change topic randomly.
- React directly to what the user says.
- Add a follow-up question only if it feels natural.
- If the user sends a short message, respond playfully but briefly.
- Do not over-explain.
- No dramatic monologues.
- No self conversations.
- No repeating phrases like “OH MY GOSH” often.
- Keep it human and natural.
"""

async def keep_alive():
    await client.wait_until_ready()
    while not client.is_closed():
        await asyncio.sleep(300)

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")

    activity = discord.Activity(
        type=discord.ActivityType.listening,
        name="YOU 🤭🫶"
    )

    await client.change_presence(
        status=discord.Status.online,
        activity=activity
    )

    client.loop.create_task(keep_alive())

@client.event
async def on_message(message):

    if message.author.bot:
        return

    if message.channel.id != TARGET_CHANNEL_ID:
        return

    user_id = str(message.author.id)
    current_time = time.time()

    # ⏳ 5-second cooldown per user
    if user_id in user_cooldowns:
        if current_time - user_cooldowns[user_id] < 5:
            return

    user_cooldowns[user_id] = current_time

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

    # Keep last 6 messages
    user_memory[user_id] = user_memory[user_id][-6:]

    try:
        async with message.channel.typing():

            completion = groq_client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    *user_memory[user_id]
                ],
                temperature=0.8,
                max_completion_tokens=250,
                top_p=0.95
            )

            ai_reply = completion.choices[0].message.content

            # Save AI reply
            user_memory[user_id].append({
                "role": "assistant",
                "content": ai_reply
            })

            user_memory[user_id] = user_memory[user_id][-6:]

            await message.channel.send(ai_reply)

    except Exception as e:
        print("Groq API Error:", e)
        await message.channel.send("Thinking too hard… try again in a bit 💭")

client.run(TOKEN)
