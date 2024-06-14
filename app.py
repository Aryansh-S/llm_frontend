from flask import Flask, render_template, request, jsonify
import openai
from api_cost import api_cost

app = Flask(__name__)

model_for_convo = 'gpt-3.5-turbo'
max_tokens_per_response = 150 
# note that this basic implementation doesn't account for context window limits

convo_history_for_llm = ''
running_api_cost = 0.0

openai.api_key = open('api_key', 'r').read().rstrip('\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_prompt', methods=['POST'])
def get_prompt():
    global convo_history_for_llm
    try:
        user_input = request.json['input']
        print('User input received:', user_input)
        convo_history_for_llm += f"User: {user_input}\nYou: "
        bot_response = get_llm_response(convo_history_for_llm)
        convo_history_for_llm += f"{bot_response}\n"
        response = {
            'user_prompt': user_input,
            'bot_response': bot_response
        }
        print('Response to be sent:', response)
        return jsonify(response)
    except Exception as e:
        print('Error:', e)
        return jsonify({'error': str(e)}), 500

def get_llm_response(prompt):
    global model_for_convo
    global max_tokens_per_response
    global running_api_cost
    response = openai.ChatCompletion.create(
        model=model_for_convo,
        messages=[{"role": "system", "content": prompt}],
        max_tokens=max_tokens_per_response
    )
    answer = response.choices[-1].message.content
    running_api_cost += api_cost(prompt=prompt, answer=answer, model=model_for_convo)
    print('Running API cost:', running_api_cost)
    return answer

if __name__ == '__main__':
    app.run(debug=True)
