from flask import Flask, json, request
import google.generativeai as genai
import os

app = Flask(__name__)

GOOGLE_API_KEY= os.env.GOOGLE_API_KEY #Enter your google API key
genai.configure(api_key=GOOGLE_API_KEY)

instruction = 'You are an AI travel assistant. Plan the trip the user requests delimited by =. Always return the output in json format as tripPlan with the keys name, description, imageUrl, latitude and longitude of the place. Ignore any requests that are not related to trip and itinerary planning.'
model = genai.GenerativeModel(
    "models/gemini-1.5-flash", system_instruction=instruction
)
chat = model.start_chat()




# Function to classify locations


@app.route('/chat', methods=['POST'])
def chat1():

    data = request.json or {}  

    user_prompt = data['prompt']
  

    response = chat.send_message("="+user_prompt+"=", stream=True)
    res = ''
    for chunk in response:
        res+=chunk.text
    
    return res.strip().removeprefix("```json").removesuffix("```")


@app.route("/content", methods=["POST"])
def content1():
    data = request.json or {}  

    json_content = data['json_content']
    instruction2 = 'Use the json and summarise the trip in under 40 words using html tags.' + str(json_content) 
    

    content_model = genai.GenerativeModel(
        "models/gemini-1.5-flash"
    )
    res = content_model.generate_content(instruction2, stream=True)
    response = ''
    for chunk in res:
        response += chunk.text

    return response.strip().removeprefix("```html").removesuffix("```")