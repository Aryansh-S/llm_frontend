from flask import Flask, render_template, request, jsonify
import openai

app = Flask(__name__)

# Set up OpenAI API key
openai.api_key = open('api_key', 'r').read().rstrip('\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_prompt', methods=['POST'])
def get_prompt():
    try:
        user_input = request.json['input']
        print('User input received:', user_input)  # Debugging log
        
        bot_response = get_chatbot_response(user_input)
        
        response = {
            'user_prompt': user_input,
            'bot_response': bot_response
        }
        print('Response to be sent:', response)  # Debugging log
        return jsonify(response)
    except Exception as e:
        print('Error:', e)  # Debugging log
        return jsonify({'error': str(e)}), 500

def generate_user_prompt(user_input):
    return user_input

def get_chatbot_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # You can choose the appropriate engine
        messages=[{"role": "system", "content": prompt}],
        max_tokens=150
    )
    return response.choices[-1].message.content

if __name__ == '__main__':
    app.run(debug=True)

