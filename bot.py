import telebot
from config import *
import random
import telebot
from logic2 import get_quiz_data, select_random_question, format_question_text, check_answer, TOPICS
import os

user_data = {}

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def handle_start(message):
    text = "Привет! 👋 Я бот-викторина. Выбери тему, чтобы начать:\n\n"
    for topic_name in TOPICS.keys():
        text += f"- /{topic_name}\n"
    bot.reply_to(message, text)

@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.chat.id, "Доступные команды:  ...")
    # Допиши команды бота
    bot.send_message(message.chat.id, "/quiz - викторина")

@bot.message_handler(commands=list(TOPICS.keys()))
def start_quiz(message):
    topic = message.text[1:]
    questions = get_quiz_data(TOPICS[topic])
    
    user_data[message.chat.id] = {
        'questions': questions,
        'correct_answers': 0,
        'total_questions': 0
    }
    
    send_next_question(message)

def send_next_question(message):
    chat_id = message.chat.id
    user_info = user_data[chat_id]
    
    question_data = select_random_question(user_info['questions'])
    formatted_text, options = format_question_text(question_data)
    
    user_info['current_question'] = {
        'options': options,
        'answer': question_data['answer']
    }
    user_info['total_questions'] += 1
    bot.send_message(chat_id, formatted_text)

@bot.message_handler(func=lambda m: m.chat.id in user_data)
def handle_answer(message):
    chat_id = message.chat.id
    user_info = user_data[chat_id]
    current_question = user_info['current_question']
    
    if check_answer(message.text, current_question['options'], current_question['answer']):
        bot.send_message(chat_id, "✅ Правильно!")
        user_info['correct_answers'] += 1
    else:
        bot.send_message(chat_id, f"❌ Неправильно. Правильный ответ: **{current_question['answer']}**")
    user_info['current_question'] = None
    if not user_info['questions']:
        final_text = f"Викторина завершена! 🎉\n" \
                     f"Ваш результат: {user_info['correct_answers']} из {user_info['total_questions']}"
        bot.send_message(chat_id, final_text)
        del user_data[chat_id]
    else:
        send_next_question(message)

if __name__ == '__main__':
    bot.polling(none_stop=True)



