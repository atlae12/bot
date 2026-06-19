import os
import requests
import asyncio
from aiogram import Bot, Dispatcher

# Получаем данные из настроек Railway (Variables)
BOT_TOKEN = os.getenv('8955345740:AAEt69mAui7qxvXXzQnGkfplIorLc_Qne9k')
STEAM_API_KEY = os.getenv('27579EE501C27E2A27CC3F63B8CE7884')
YOUR_CHAT_ID = os.getenv('7764466097')
# ID друзей через запятую в одной строке в настройках
FRIENDS_STEAM_IDS = os.getenv('76561199853757393').split(',')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Хранилище статусов
last_statuses = {steam_id: None for steam_id in FRIENDS_STEAM_IDS}

async def check_steam_status():
    ids_string = ",".join(FRIENDS_STEAM_IDS)
    url = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_API_KEY}&steamids={ids_string}"
    
    try:
        response = requests.get(url, timeout=10).json()
        players = response['response']['players']
        
        for player in players:
            steam_id = player['steamid']
            current_status = player.get('personastate', 0)
            
            if last_statuses[steam_id] is not None and current_status != last_statuses[steam_id]:
                name = player.get('personaname', 'Друг')
                # 0 - оффлайн, 1 - онлайн
                status_text = "в сети" if current_status != 0 else "вышел из сети"
                await bot.send_message(chat_id=YOUR_CHAT_ID, text=f"🎮 {name} {status_text}")
            
            last_statuses[steam_id] = current_status
            
    except Exception as e:
        print(f"Ошибка: {e}")

async def main():
    while True:
        await check_steam_status()
        await asyncio.sleep(120)

if __name__ == "__main__":
    asyncio.run(main())
