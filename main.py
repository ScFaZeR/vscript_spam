import discord
import os
import asyncio
from discord.ext import tasks
from flask import Flask
from threading import Thread

# --- CONFIGURATION ---
# Le Token de ce NOUVEAU bot (Pinger)
DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN')

# L'ID du salon où il doit parler (Active le mode développeur sur Discord pour faire Clic Droit > Copier l'identifiant sur le salon)
CHANNEL_ID = 1462498355182571585  # ⚠️ REMPLACE ÇA PAR LE VRAI ID DU SALON (C'est un nombre entier, pas de guillemets)

# L'ID de ton bot principal VScript (pour le mentionner)
TARGET_BOT_ID = 1462260996482531380 # ⚠️ REMPLACE ÇA PAR LE VRAI ID DE TON BOT PRINCIPAL

# --- SERVEUR WEB (Pour Render) ---
app = Flask('')

@app.route('/')
def home():
    return "Pinger Bot est en ligne !"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- BOT DISCORD ---
intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'✅ Pinger Bot connecté en tant que {client.user}')
    # Démarre la boucle de 10 minutes
    ping_routine.start()

@tasks.loop(minutes=10)
async def ping_routine():
    # On attend que le bot soit bien prêt avant de commencer
    await client.wait_until_ready()
    
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        # Envoie le message avec la mention du bot principal
        await channel.send(f"<@{TARGET_BOT_ID}> Maintenance check ! ⏰")
        print("✅ Ping envoyé !")
    else:
        print(f"❌ Impossible de trouver le salon {CHANNEL_ID}")

# Lancement
keep_alive()
client.run(DISCORD_TOKEN)
