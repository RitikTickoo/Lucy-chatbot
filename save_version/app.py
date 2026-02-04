from flask import Flask,request,jsonify,render_template
from openai import OpenAI
from flask_cors import CORS
import os
app=Flask(__name__)
CORS(app)
conversation_memory=[]
Last_N=6
client=OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def generate_reply(user_message,conversation_memory):
    recent_memory=conversation_memory[-Last_N:]
    print('recent memory is',recent_memory)
    response=client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {'role':'system','content':'You are lucy , a helpful chatbot'},
            {'role':'user','content':user_message}
        ]
    ) 
    return response.choices[0].message.content
@app.route('/hello')

def hello():
    return "Hello, I am your chatbot. How can i help you today?"


@app.route('/')
def Home():
    return render_template('index.html')

@app.route('/chat',methods=['POST'])
def chat():
    user_message=request.json.get('message','').lower()
    conversation_memory.append(user_message)

    reply=generate_reply(user_message,conversation_memory)

    return jsonify({'response':reply})
if __name__ == '__main__':
    app.run()