from flask import Flask, render_template, request, jsonify
import os
import openai

# Set up your OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

client = openai.OpenAI()

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.5
    )
    return response.choices[0].message.content

# Initialize Flask app
app = Flask(__name__)

# HTML template for the dream interpreter page
@app.route('/')
def index():
    return render_template('dream_interpreter1.html')

# Interpret dream description
@app.route('/interpret', methods=['POST'])
def interpret_dream():
    data = request.get_json()
    dream_description = data['dream']
    prompt = f"""
    Your task is to help a person to solve a dream he/she had.

    Write a dream interpretation based on the information provided in the Dream description delimited by triple backticks.
    
    The interpretation has to be in the same language as the Dream description is.
    The interpretation is intended for the dreamer, so should be personal in nature and focus on the details the dream is made of.
    The interpretation has to have 2 parts: Explanation and Suggestion. Each one of this two words is an header. Therefore, both words need to be delineated by *.
    On the Suggestion part try not to repeat what was written in the Explanation part.
    Each part in a seperated paragraph, no longer then 5 lines each.

    Dream description: ```{dream_description}```
    """

    # Call get_completion def to generate dream interpretation
    interpretation = get_completion(prompt)

    return jsonify({'interpretation': interpretation})

if __name__ == '__main__':
    app.run(debug=False)
