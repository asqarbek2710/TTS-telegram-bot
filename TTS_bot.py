#new one                                                                                                                                                                            import telebot
from telebot import telebot, types
from gtts import gTTS
from deep_translator import GoogleTranslator

TELEGRAM_BOT_TOKEN = 'MY_telegram_bot_token'
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
user_data = {}

@bot.message_handler(commands=['start'])
def start_command(message):
    greeting_text = "Welcome! I am a Telegram bot designed by Asqarbek. I am capable of translating and vocalizing text in various languages."
    bot.send_message(message.chat.id, greeting_text)
    select_language(message)

def select_language(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('English', 'Russian')
    bot.send_message(message.chat.id, 'Please select the language:', reply_markup=markup)
    user_data[message.chat.id] = {}
    bot.register_next_step_handler(message, input_text)

def input_text(message):
    chat_id = message.chat.id
    if message.text in ['English', 'Russian']:  # Check if the user selected a valid language
        selected_language = 'en' if message.text == 'English' else 'ru'
        user_data[chat_id]['language'] = selected_language
        bot.send_message(chat_id, 'Enter the words or a sentence you want to translate:')
        bot.register_next_step_handler(message, translate_and_speak)
    else:
        bot.send_message(chat_id, 'Please select a valid language.')
        select_language(message)

def translate_and_speak(message):
    chat_id = message.chat.id
    text = message.text
    language = user_data[chat_id]['language']
    translated_text = translate_text(text, language)
    bot.send_message(chat_id, translated_text)
    mp3_file = text_to_speech(translated_text, language)
    with open(mp3_file, 'rb') as audio_file:
        bot.send_audio(chat_id, audio_file)
    
    ask_next_step(message)

def translate_text(text, target_lang):
    translation = GoogleTranslator(source='auto', target=target_lang).translate(text)
    return translation

def text_to_speech(text, language):
    tts = gTTS(text, lang=language)
    mp3_file = "output.mp3"
    tts.save(mp3_file)
    return mp3_file

def ask_next_step(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('Input New Text', 'Select Language', 'Exit')
    bot.send_message(message.chat.id, 'What would you like to do next?', reply_markup=markup)
    bot.register_next_step_handler(message, handle_next_step)

def handle_next_step(message):
    chat_id = message.chat.id
    if message.text == 'Input New Text':
        bot.send_message(chat_id, 'Enter the words or a sentence you want to translate:')
        bot.register_next_step_handler(message, translate_and_speak)
    elif message.text == 'Select Language':
        select_language(message)
    elif message.text == 'Exit':
        bot.send_message(chat_id, 'Thank you for using the translation service. Goodbye! To continue, press /start.')
    else:
        bot.send_message(chat_id, 'Invalid option. Please select a valid action.')
        ask_next_step(message)

bot.polling()
