import telebot
from constants import TELEGRAM_API_KEY
import y2audio as y2
from datetime import datetime
from background import keep_alive

# Initialize the Telegram bot
bot = telebot.TeleBot(TELEGRAM_API_KEY)


# Default Start Welcome User
@bot.message_handler(commands=['start'])
def start(message):
  # Send a welcome message
  bot.reply_to(
    message, f'''
    👋 Welcome to the bot, {message.chat.first_name}! Just send me link for the youtube video.
    ''')


# Handling Any message trying to get a youtube link
@bot.message_handler(func=lambda message: True)
def handle_message(message):
  ytb_link = message.text.strip()
  msg = bot.send_message(message.chat.id, '⚙️ Processsing the video...')
  msg = msg.message_id
  bot.send_chat_action(message.chat.id, 'typing')

  try:
    file_path = y2.download_audio_from_youtube(ytb_link)
    data = y2.get_data_from_youtube(ytb_link)
    audio = open(rf'{file_path}', 'rb')
    bot.send_audio(message.chat.id, audio)
    bot.send_message(message.chat.id,
                     f'''
🎥 {data["title"]};
😎 <b>Channel:</b>  <a href="{data["channel_url"]}">{data["author"]}</a>;
📆 <b>Publish Date:</b> {datetime.strftime(data["publish_date"], "%m/%d/%Y")};
''',
                     parse_mode='html')
    bot.send_message(message.chat.id,
                     f''' 
<code>🃏 Summary: </code>
{data["content"]}
''',
                     parse_mode='html')
    audio.close()
  except Exception as e:
    print("An error occurred:", str(e))
    bot.send_message(
      message.chat.id,
      '⚠️ Sorry, something went wrong! You have an error in request!')
  finally:
    y2.delete_audio_file(file_path)
    if msg:
      bot.delete_message(message.chat.id, msg)


# Remove Webhook & Keeping Bot Alive on the Server
bot.remove_webhook()
keep_alive()

# Bot running..
bot.polling()
