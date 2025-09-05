import json
import random


TOPICS = {
    'мифы': 'myths.json',
    'история': 'historyquiz.json',
    'география': 'geographie.json',
    'информатика часть 1': 'programming.json',
    'геометрия': 'geometry.json',
    'Англ.Яз': 'english.json',
    'информатика2': 'programming2.json',
    'Физика': 'physics.json',
    'информатика3': 'programming3.json'
}


def get_quiz_data(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data['quizzes']


def select_random_question(questions_list):
    question_data = random.choice(questions_list)
    questions_list.remove(question_data)
    return question_data

def format_question_text(question_data):
    options = question_data['options']
    random.shuffle(options)
    
    formatted_text = f"**{question_data['question']}**\n\n"
    for i, option in enumerate(options, 1):
        formatted_text += f"{i}. {option}\n"
        
    return formatted_text, options

def check_answer(user_answer, options, correct_answer):
    user_answer_index = int(user_answer) - 1
    return options[user_answer_index] == correct_answer