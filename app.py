from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# OpenAI API anahtarınızı buraya ekleyin veya ortam değişkeninden alın
def get_openai_api_key():
    return os.getenv('OPENAI_API_KEY', 'YOUR_OPENAI_API_KEY')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    user_message = data.get('message', '')
    openai.api_key = get_openai_api_key()
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]            
        )
        answer = response.choices[0].message['content'].strip()
        return jsonify({'answer': answer})
    except Exception as e:
        return jsonify({'answer': f'Hata: {str(e)}'}), 500

@app.route('/')
def serve_index():
    return app.send_static_file('index.html')

@app.route('/<path:path>')
def serve_static(path):
    return app.send_static_file(path)

if __name__ == '__main__':
    # Flask'ın statik dosya klasörünü mevcut dizin olarak ayarla
    app.static_folder = '.'
    app.run(debug=True)
