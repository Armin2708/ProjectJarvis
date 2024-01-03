import asyncio
import threading
import discord
from discord import Intents
from flask import Flask, request, jsonify

app = Flask(__name__)
intents = Intents.default()
client = discord.Client(intents=intents)

# Replace 'YOUR_DISCORD_BOT_TOKEN' with your bot's token
TOKEN = 'MTE4NjgyNDUzOTk2ODExMDYwMw.GNBqz6.lAN_V3uxuZtPEhBO9VNQwCQrSJSR6xM6XFi1Wg'  # Replace with your bot token

# Replace 'YOUR_CHANNEL_ID' with the ID of the channel you want to post messages in
CHANNEL_ID = 1186852607113834616


@app.route('/post_message', methods=['POST'])
def post_message():
    data = request.json
    print(f"Received data: {data}")
    message = data.get('message')
    if not message:
        print("No message found in request data")
        return jsonify({'status': 'Error', 'message': 'No message found in request data'})
    asyncio.run_coroutine_threadsafe(send_message(message), client.loop)
    return jsonify({'status': 'Message sent'})


async def send_message(message):
    print(f"Attempting to send message: {message}")
    try:
        channel = client.get_channel(CHANNEL_ID)
        if channel is None:
            print(f"Cannot find the channel with ID: {CHANNEL_ID}")
        else:
            await channel.send(message)
    except Exception as e:
        print(f"An error occurred: {e}")



@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    await client.get_channel(CHANNEL_ID).send("Quiz Bot Running")
    await client.get_channel(CHANNEL_ID).send(file=discord.File('burgerkingguy.gif'))
    server = threading.Thread(target=app.run, kwargs={'port':2345})  # Flask server in different thread
    server.start()

if __name__ == '__main__':
    client.run(TOKEN)  # Blocking call that starts the event loop