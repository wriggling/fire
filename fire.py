import os
import time
import discord
import asyncio
from datetime import datetime, timedelta
from rich.console import Console
from rich.color import Color
import shutil

console = Console()

# ─────────────────────────────────────────────────────────
# Utility functions
# ─────────────────────────────────────────────────────────

def gradient_text(text, start_color, end_color):
    start_rgb = Color.parse(start_color).triplet
    end_rgb = Color.parse(end_color).triplet

    def lerp(a, b, t):
        return int(a + (b - a) * t)

    result = ""
    length = max(len(text), 1)
    for i, char in enumerate(text):
        t = i / (length - 1) if length > 1 else 0
        r = lerp(start_rgb[0], end_rgb[0], t)
        g = lerp(start_rgb[1], end_rgb[1], t)
        b = lerp(start_rgb[2], end_rgb[2], t)
        result += f"[#{r:02x}{g:02x}{b:02x}]{char}"
    return result + "[/]"

def clear():
    return os.system('cls') if os.name == 'nt' else os.system('clear')

os.system('title [Fire : by @jc2 on cord]')

def print_centered_banner(banner, start_color="#800000", end_color="#ff6600"):
    columns = shutil.get_terminal_size((80, 20)).columns
    lines = banner.strip("\n").split("\n")
    for line in lines:
        padded_line = line.center(columns)
        console.print(gradient_text(padded_line, start_color, end_color))

# ─────────────────────────────────────────────────────────
# Banner art
# ─────────────────────────────────────────────────────────

BANNER = """
┏┓•      ┏┓            
┣ ┓┏┓┏┓  ┃ ┏┓┓┏┏┓╋┏┓┏┓ 
┻ ┗┛ ┗   ┗┛┗┛┗┻┛┗┗┗ ┛ •
-----------------------
"""

# ─────────────────────────────────────────────────────────
# Inputs (with clears between each step)
# ─────────────────────────────────────────────────────────

os.system("mode con cols=80 lines=25")
clear()
print_centered_banner(BANNER)
token = input('\n\nPlease Enter Your Token Here: ')

clear()
print_centered_banner(BANNER)
start_time = int(input("Enter start number: "))

clear()
print_centered_banner(BANNER)
start_keyword = input("Enter the start trigger word/message: ").lower()

interval = 3600  # 1 hour in seconds
counting = False  # track active countdown

# ─────────────────────────────────────────────────────────
# Discord Client Setup
# ─────────────────────────────────────────────────────────

client = discord.Client()

@client.event
async def on_ready():
    os.system(f'title [Fire : by @jc2 on cord] | Connected As: {client.user}')
    clear()
    print_centered_banner(BANNER)

@client.event
async def on_message(message):
    global counting

    if message.author != client.user:
        return

    if message.content.strip().lower() == start_keyword and not counting:
        counting = True

        console.print(gradient_text(f"\nCountdown started from {start_time} with an interval of {interval // 3600} hour(s).", "#00ffff", "#0000ff"))
        
        start_received_time = datetime.now()
        console.print(gradient_text(f"[{start_received_time.strftime('%Y-%m-%d %H:%M:%S')}] Start trigger received, countdown will begin in 1 hour.", "#00ffff", "#0000ff"))

        hours_passed = start_time + 1
        await asyncio.sleep(interval)

        while counting:
            clear()
            print_centered_banner(BANNER)

            message_to_send = f"{hours_passed}"
            start_time_sent = datetime.now()
            latency = round(client.latency * 1000)

            await message.channel.send(message_to_send)

            time_sent_str = start_time_sent.strftime('%Y-%m-%d %H:%M:%S')
            next_send_time = (start_time_sent + timedelta(seconds=interval)).strftime('%Y-%m-%d %H:%M:%S')
            log_message = f"[{time_sent_str}] Sent: {message_to_send} | Latency: {latency}ms | Next message at: {next_send_time}"

            console.print(gradient_text(log_message, "#ff00ff", "#800080"))
            hours_passed += 1
            await asyncio.sleep(interval)

    elif message.content.strip().lower() == ".end":
        if counting:
            counting = False
            await message.channel.send("Countdown has been stopped.")
            console.print(gradient_text("Countdown stopped.", "#ff0000", "#8b0000"))

# ─────────────────────────────────────────────────────────
# Start the bot
# ─────────────────────────────────────────────────────────

client.run(token)
