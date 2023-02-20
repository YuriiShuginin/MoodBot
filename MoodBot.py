import telebot
import config
import pymorphy2
from random import randint
# from telebot import apihelper


# apihelper.proxy = {'https': '{}'.format(config.proxy)}
bot = telebot.TeleBot(config.access_token)


def input_dict():
    file = open('./dictionary.txt', 'r', encoding='utf-8')
    for line in file:
        key_words = line.split(', ')
    file.close()
    for i in range(len(key_words)):
        key_words[i] = change(key_words[i])
    return list(set(key_words))


def input_qs():
    questions = []
    file = open('./questions.txt', 'r', encoding='utf-8')
    for line in file:
        line = line.replace('\n','')
        questions.append(line)
    file.close()
    return questions


def input_ans():
    answers = []
    file = open('./answers.txt', 'r', encoding='utf-8')
    for line in file:
        line = line.replace('\n','')
        answers.append(line)
    file.close()
    return answers


def choose_qs():
    num = randint(1, 19)
    while num in used_num:
        num = randint(1, 19)
    used_num.append(num)
    return num


def choose_ans():
    counter = 0
    for word in dictionary:
        for msg in msgs:
            if word in msg:
                counter += 1
    if counter <= 2:
        return 0
    elif 3 <= counter <= 4:
        return 1
    elif 5 <= counter <= 6:
        return 2
    elif 7 <= counter <= 8:
        return 3
    elif 9 <= counter <= 11:
        return 4
    else:
        return 5


def form(word, morph = pymorphy2.MorphAnalyzer()):
    ''' Возвращает начальную форму полученного слова '''
    p = morph.parse(word)[0]
    return(p.normal_form)


alph = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ '
def change(string):
    clean = []
    new = string.split(' ')
    for word in new:
        word = ''.join(sym for sym in word if sym in alph)
        if word:
            clean.append(word)
    for i in range(len(clean)):
        clean[i] = form(clean[i])
    return ' '.join(clean)


dictionary = input_dict()
questions = input_qs()
answers = input_ans()
msgs = []
used_num = []


@bot.message_handler(commands=['start'])
def get_start(message):
    bot.send_message(message.chat.id, questions[0])


@bot.message_handler(content_types=['text'])
def read(message):
    if change(message.text) == '':
        bot.send_message(message.chat.id, questions[20] + '\n' + questions[21])
    else:
        msgs.append(change(message.text))
    if len(msgs) < 5:
        bot.send_message(message.chat.id, questions[choose_qs()])
    else:
        bot.send_message(message.chat.id, '{}\nБыло приятно пообщаться! Хорошего дня :)'.format(answers[choose_ans()]))
        msgs.clear()
        used_num.clear()


if __name__ == '__main__':
    bot.polling(none_stop=True)