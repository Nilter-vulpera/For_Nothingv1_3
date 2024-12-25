from transformers import AutoModelForCausalLM, AutoTokenizer
from huggingface_hub import login
from django.conf import settings
# class LLaMAService:
#     def __init__(self, model_name):
#         token = settings.HUGGINGFACE_TOKEN
#         login(token=token)
#         self.tokenizer = AutoTokenizer.from_pretrained(model_name, token=token,trust_remote_code=True)
#         self.model = AutoModelForCausalLM.from_pretrained(model_name, token=token)
#
#     def generate_text(self, prompt, max_length=300):
#         inputs = self.tokenizer(prompt, return_tensors='pt')
#         outputs = self.model.generate(inputs['input_ids'], max_length=max_length)
#         return self.tokenizer.decode(outputs[0], skip_special_tokens=True)


#
# from chatterbot import ChatBot
# from chatterbot.trainers import ChatterBotCorpusTrainer
#
# chatbot = ChatBot('SocialNetworkBot')
#
# trainer = ChatterBotCorpusTrainer(chatbot)
# trainer.train("chatterbot.corpus.russian")

import pathlib
import textwrap

import google.generativeai as genai


from IPython.display import Markdown

model = genai.GenerativeModel('gemini-1.5-flash')

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))