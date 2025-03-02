from django.shortcuts import render
from django.http import JsonResponse
from transformers import AutoModelForCausalLM, AutoTokenizer
#import torch
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


#import tensorflow as tf
import numpy as np
#from transformers import pipeline
# Загрузка модели
# model = tf.keras.models.load_model('NeuraChatBot/chat_model.h5')



# Загрузка модели
# qa_pipeline = pipeline("question-answering", model="bert-base-multilingual-cased")

# def predict(question, context):
#     result = qa_pipeline(question=question, context=context,)
#     return result['answer']


class message_to_chat_bot(models.Model):
    message_to_chat_bot_text = models.TextField(max_length=100)
    name = models.CharField(max_length=100)
