from flask import Flask, request, jsonify
from flask_cors import CORS
import openai

app = Flask(__name__)
CORS(app)

openai.api_key = ''

@app.route('/answer', methods=['POST'])
def answer_question():
    data = request.json
    context = data.get('context', '')
    question = data.get('question', '')

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that answers questions based on the provided context. If the question is not related to the context, respond with 'Please ask a question related to the document'."},
            {"role": "user", "content": f"Context: {context}\n\nQuestion: {question}"}
        ],
        max_tokens=150
    )

    answer = response.choices[0].message['content'].strip() 
    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(debug=True)