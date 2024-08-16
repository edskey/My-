import requests
from telegram import Update
from telegram.ext import Application, CommandHandler
import nest_asyncio
import asyncio

TOKEN = '7248397126:AAGKNkasnJNJbHJBJkNKjpvgmk4QTFUHH5wU'
CHAT_ID = '111234521318'

def get_solana_price():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        'ids': 'solana',
        'vs_currencies': 'usd'
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
       
        print("API Response:", data)  
        
        if 'solana' in data and 'usd' in data['solana']:
            return data['solana']['usd']
        else:
            print("Ошибка: данные для 'solana' не найдены")
            return None
    except Exception as e:
        print(f"Ошибка при запросе к API: {e}")
        return None

async def send_message(application: Application, text: str):
    await application.bot.send_message(chat_id=CHAT_ID, text=text)


async def check_price(application: Application):
   
    current_price = get_solana_price()
    
    if current_price is None:
        return  
    
    if current_price >= 14:
        await send_message(application, f"Цена SOLANA поднялась до ${current_price}!")


async def price(update: Update, context) -> None:
    current_price = get_solana_price()
    if current_price is not None:
        await update.message.reply_text(f"Текущая цена SOLANA: ${current_price}")
    else:
        await update.message.reply_text("Не удалось получить текущую цену SOLANA.")


async def main():
    
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("price", price))

    async def periodic_check():
        while True:
            await check_price(application)
            await asyncio.sleep(60) 

    await application.initialize()
    asyncio.create_task(periodic_check()) 
    await application.run_polling()  
    await application.shutdown()

if __name__ == '__main__':
    nest_asyncio.apply()  
    asyncio.run(main())