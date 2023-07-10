import os
from dotenv import load_dotenv
import logging

from flask import Flask, request, jsonify, render_template

import openai

load_dotenv()

from ChuckNorris import ChuckNorris

app = Flask(__name__, template_folder='.')


cn = ChuckNorris()

def gpt(messages: list, functions: list = None) -> str:
    openai.api_key = os.getenv("OPENAI_KEY")
    if functions is None:   
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=messages
        )
    else:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=messages,
            functions=functions,
            function_call="auto"
        )
    logging.info("OpenAI Response:")
    logging.info(response)
    return response

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data['message']

    messages = [
        {"role": "system", "content": "Hello, this is a Chuck Norris Troll bot"},
        {"role": "user", "content": user_message}
    ]

    response = gpt(messages, cn.class_functions)
    response_message = response["choices"][0]["message"]
    function_call = response_message.get("function_call")

    if function_call:
        function_response = cn.executioner(function_call)
        logging.info("Function Response:")
        logging.info(function_response)
        messages.append(response_message)
        messages.append(
            {
                "role": "function",
                "name": function_call['name'],
                "content": '\n'.join(function_response),
            },
        )
        second_response = gpt(messages)
        response_msg = second_response["choices"][0]["message"]["content"]
        return jsonify({"response": response_msg})
    else:
        return jsonify({"response": "No comment."})

if __name__ == "__main__":
    app.run()