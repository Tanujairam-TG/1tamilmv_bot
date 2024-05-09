import telebot
import requests
import re
from bs4 import BeautifulSoup

TOKEN = '6991880970:AAEGY_2pgNijHCHbkw2BRQlWUO0uxF432oA'  # Replace with your actual bot token

bot = telebot.TeleBot(TOKEN)

button1 = telebot.types.InlineKeyboardButton(text="⚡Powered by", url='https://t.me/heyboy2004')
button2 = telebot.types.InlineKeyboardButton(text="🔗 Gdrive channel", url='https://t.me/GdtotLinkz')
button3 = telebot.types.InlineKeyboardButton(text="📜 Status channel", url='https://t.me/TmvStatus')
keyboard = telebot.types.InlineKeyboardMarkup().add(button1, button2, button3)
keyboard2 = telebot.types.InlineKeyboardMarkup().add(button2, button3)

@bot.message_handler(commands=['start'])
def random_answer(message):
    bot.send_message(chat_id=message.chat.id, text=f"Hello👋 \n\n🗳Get latest Movies from 1Tamilmv\n\n⚙️*How to use me??*🤔\n\n✯ Please Enter */view* command and you'll get magnet link as well as link to torrent file 😌\n\nShare and Support💝", parse_mode='Markdown', reply_markup=keyboard)

@bot.message_handler(commands=['view'])
def start(message):
    bot.send_message(message.chat.id, text="*Please wait for 10 seconds*", parse_mode='Markdown')
    tamilmv()
    bot.send_message(chat_id=message.chat.id, text="Select a Movie from the list 🙂 :", reply_markup=makeKeyboard(), parse_mode='HTML')

@bot.callback_query_handler(func=lambda message: True)
def callback_query(call):
    bot.send_message(call.message.chat.id, text=f"Here's your Movie links 🎥 ", parse_mode='markdown')
    for key, value in enumerate(movie_list):
        if call.data == f"{key}":
            if movie_list[int(call.data)] in real_dict.keys():
                for i in real_dict[movie_list[int(call.data)]]:
                    bot.send_message(call.message.chat.id, text=f"{i}\n\n🤖 @Tamilmv_movie_bot", parse_mode='markdown')
    bot.send_message(call.message.chat.id, text=f"🌐 Please Join Our Status Channel", parse_mode='markdown', reply_markup=keyboard2)

def makeKeyboard():
    markup = telebot.types.InlineKeyboardMarkup()
    for key, value in enumerate(movie_list):
        markup.add(telebot.types.InlineKeyboardButton(text=value, callback_data=f"{key}"))
    return markup

def tamilmv():
    mainUrl = 'https://www.1tamilmv.yt/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'Connection': 'Keep-alive',
        'sec-ch-ua-platform': '"Windows"',
    }
    global movie_dict, real_dict, movie_list
    movie_dict = {}
    real_dict = {}
    movie_list = []
    web = requests.get(mainUrl, headers=headers)
    soup = BeautifulSoup(web.text, 'lxml')
    temps = soup.find_all('div', {'class': 'ipsType_break ipsContained'})
    for i in range(21):
        title = temps[i].find('a').text.strip()
        movie_dict[title] = None
        movie_list.append(title)
        link = temps[i].find('a')['href']
        html = requests.get(link)
        soup = BeautifulSoup(html.text, 'lxml')
        mag_links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith('magnet')]
        torrent_links = [a['href'] for a in soup.find_all('a', {"data-fileext": "torrent", 'href': True})]
        titles = [span.text[19:-8] for span in soup.find_all('span') if span.text.endswith('torrent')]
        for p in range(len(mag_links)):
            real_dict.setdefault(movie_list[i], []).append(f"*{titles[p]}* -->\n🧲 `{mag_links[p]}`\n🗒️->Torrent file")

def main():
    bot.infinity_polling(timeout=10, long_polling_timeout=5)

if __name__ == '__main__':
    main()
