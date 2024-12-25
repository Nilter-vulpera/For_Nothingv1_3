import random
import json
import pickle

# from django.http import JsonResponse
from django.shortcuts import render
# from numpy import array
# import numpy as np
# import nltk
# from nltk.stem import WordNetLemmatizer
# import os
# # from tensorflow.keras.models import load_model
# import re
# from .models import predict
from .forms import MessageFormForBot

# lemmatizer = WordNetLemmatizer()
# intents = json.loads(open('NeuraChatBot/intents.json').read())
#
# words = pickle.load(open('NeuraChatBot/words.pkl', 'rb'))
# classes = pickle.load(open('NeuraChatBot/classes.pkl', 'rb'))
# model = load_model('NeuraChatBot/chat_model.h5')
#
# def clean_up_sentence(sentence):
#     sentence_words = nltk.word_tokenize(sentence)
#     sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
#     return sentence_words
#
# def bag_of_words(sentence):
#     sentence_words = clean_up_sentence(sentence)
#     bag = [0] * len(words)
#     for w in sentence_words:
#         for i, word in enumerate(words):
#             if word == w:
#                 bag[i] = 1
#     return array(bag)
#
# def predict_class(sentence):
#     bow = bag_of_words(sentence)
#     res = model.predict(np.array([bow]))[0]
#     ERROR_THRESHOLD = 0.25
#     results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
#
#     results.sort(key=lambda x: x[1], reverse=True)
#     return_list = []
#     for r in results:
#         return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
#     return return_list
#
# def get_response(intents_list, intents_json):
#     tag = intents_list[0]['intent']
#     list_of_intents = intents_json['intents']
#     for i in list_of_intents:
#         if i['tag'] == tag:
#             result = random.choice(i['responses'])
#             break
#     return result
#
# print('Go, bot is running!')
# from .utils import get_gpt4_response
from .services import model,to_markdown

def chat(request):
    response = None
    if request.method == 'POST':
        form = MessageFormForBot(request.POST)
        if form.is_valid():
            promp = form.cleaned_data['message_to_chat_bot_text']
            # context = form.cleaned_data['context_field']
            # question = form.cleaned_data['question_field']
            try:
                response = model.generate_content(promp).text
                # response = get_gpt4_response(promp)

            except Exception as e:
                response = f"Ошибка: {str(e)}"
        else:
            response = "Некорректное заполнение формы."
    else:
        form = MessageFormForBot()

    return render(request, 'flatpages/chatbot/chatbot.html', {"response": response, "form": form})






