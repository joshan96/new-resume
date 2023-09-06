# -*- coding: utf-8 -*-
"""Untitled4.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1qYvIZS6SXdx47vPgOO5YnsMSjvPt_rTa
"""

from google.colab import auth
import gspread
from google.auth import default #authenticating to google
auth.authenticate_user()
creds, _ = default()
gc = gspread.authorize(creds)

import pandas as pd #defining my worksheet
worksheet = gc.open('Joshan_Chatbot').sheet1 #get_all_values gives a list of rows
rows = worksheet.get_all_values() #Convert to a DataFrame
df = pd.DataFrame(rows)

#creating columns name
df.columns = df.iloc[0]
df = df.iloc[1:]

df

pip install openai

import openai

# Set your API key
api_key = "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"
openai.api_key = api_key

qa_dict = df.set_index("Question").to_dict()["Answer"]

qa_dict

import spacy

# Load spaCy model for NER
nlp = spacy.load("en_core_web_sm")

def chatbot_response(question, qa_dict):
    prompt = ("You are Joshan's assistant. Your job is to answer questions that people ask about Joshan. This is the only information that you know about Joshan - " + qa_dict + "." +
                " When someone asks a question, please give an accurate or precise response." +
                " Someone has asked this question - " + question + ". Please give your reply. "
             )
    response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=500,
            temperature=0.45,
        )
    print("Question - ",question, "\n qa_dict - ",qa_dict, "\n Prompt - ",prompt,"\n Response - ",response)
    return response.choices[0].text
    # if question in qa_dict:
    #     return qa_dict[question]
    # else:
    #     # Use spaCy for named entity recognition
    #     doc = nlp(question)
    #     for ent in doc.ents:
    #         if ent.text == "Joshan":
    #             return "Yes, Joshan has worked in B2C companies in the past."
    #     # If no specific answer found, use ChatGPT
    #     return "Checking GPT..."
    #     response = openai.Completion.create(
    #         engine="text-davinci-002",
    #         prompt=question,
    #         max_tokens=50,
    #         temperature=0.7,
    #     )
    #     return response.choices[0].text

def chat35bot_response(question, qa_dict):
    message_list = [
        {
            "role": "system",
            "content": "You are Joshan's assistant. Your job is to answer questions that people ask about Joshan. This is the only information that you know about Joshan - " + qa_dict + "."
        },
        {
            "role": "user",
            "content": question
        }
        ]
    response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=message_list,
            max_tokens=500,
            temperature=0.45,
        )
    print("Question - ",question, "\n qa_dict - ",qa_dict, "\n Message - ",message_list,"\n Response - ",response)
    return response.choices[0].message.content

user_question = "What is a good salary for Joshan?"
answer = chat35bot_response(user_question, str(qa_dict))
print(answer)

df



