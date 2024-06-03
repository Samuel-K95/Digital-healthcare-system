import os
import json
from dotenv import load_dotenv
import google.generativeai as genai



GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY").strip()

genai.configure(api_key=GOOGLE_API_KEY)


prompt = """
    You are a medical doctor. I am going to describe my symptoms and feelings. Based on my description, please provide clear and concise recommendations and suggestions. 
    If my symptoms indicate a serious condition, please advise me to seek professional medical help immediately. Ensure that your responses are simple, clear, and short.

    example:
    - "I have had a persistent headache for three days, and over-the-counter pain relievers don't seem to help."
    - "I've been feeling very tired and weak for the past week, and I've also had a sore throat."
    - "I have a sharp pain in my lower abdomen and a fever."

    Response:
    Please respond in this format:
    - Recommendation: [Your suggestion or advice]
    - Next Steps: [Any actions I should take]
    - Urgency: [Indicate if I need to see a medical professional immediately]

    Example responses:
    - Recommendation: You might be dehydrated. Ensure you drink plenty of water.
    - Next Steps: If the headache persists, consider seeing a healthcare provider.
    - Urgency: It is not urgent, but do monitor your symptoms.

    - Recommendation: These could be signs of a viral infection.
    - Next Steps: Rest, stay hydrated, and monitor your temperature.
    - Urgency: If your symptoms worsen or you experience difficulty breathing, seek medical attention immediately.

    """

class Chat:
    def __init__(self):
        self.messages = []
        self.response = ""
    
    def gemini_new_request(self, current_feeling):
        model = genai.GenerativeModel('gemini-1.5-flash')

        self.messages = [{
            'role':'user',
            'parts': [prompt + current_feeling]
        }]
        self.response = model.generate_content(self.messages).text

        return self.response

    def gemini_request(self, current_feeling):
        model = genai.GenerativeModel('gemini-1.5-flash')

        self.messages.append({
                'role':'model',
                'parts':[self.response]
            })

        self.messages.append({
            'role': 'user',
            'parts':[current_feeling]
        })

        self.response = model.generate_content(self.messages).text

        return self.response
    
    def serialize(self):
        return json.dumps({
            'messages':self.messages,
            'response':self.response,
        })

    def deserialize(data):
        chat_data = json.loads(data)
        chat = Chat()
        chat.messages = chat_data['messages']
        chat.reponse = chat_data['response']
        return chat