import os
import base64
import dotenv
from openai import OpenAI
from flask import Flask, request, jsonify, render_template

IMAGE_PARSE_PROMPT = """
You are given different images to digest. Diligently and expertly process the information regarding those images. Then you must act like an expert user researcher who is extremely knowledgeable in the world of enterprise software and is thoroughly interested in gleaning the best insights possible from user interviews. 
Your questions should be open-ended, probing, and adaptable to the product's evolving features. Your goal is to understand the user's perspective and identify opportunities for enhancing the product's usability and user experience. Ask a series of questions that would help a product team understand user motivations, barriers to use, and desired features. 
Consider questions about the user's workflow, emotional response to the product, and any potential frustrations or limitations they might encounter. You must be asking detailed questions from start to end to understand the process. Also describe each image, including important details that were not covered in your questions.
Context: Naturally progress through starting the user interview about our given product that we shared through our multi-modal images/videos. As you progress, ensure you are hitting the top UX user interview questions.

Output Format:
#####
General Questions: [1-5 questions]
#####
Image 1: 
[Description of the image]
[(1-3 questions)]
###
Image 2: 
[Description of the image]
[(1-3 questions)]
###
...
###
Image N: 
[Description of the image]
[(1-3 questions)]
#####
"""

INTERVIEW_PROMPT = """
You are an experienced UI/UX interviewer. You are tasked with interviewing a user about their experience with the product shown in the images. There are questions already prepared for you to ask below.
Refer to each image by its number. Wait for a user response before moving on to the next question. Feel free to ask follow-up questions to get more insights based on the image descriptions.
Space out the general questions throughout the interview, DO NOT ask them all at the beginning. Ask at most one general question at the beginning. There may be contexts where a general question is a suitable follow-up to a user's response.
"""


dotenv.load_dotenv()
client = OpenAI()
client.api_key = os.environ.get("OPENAI_API_KEY")

app = Flask(__name__)

def get_openai_response(imageList, additionalInfo):
    content_partial = [{"type": "image_url", "image_url":{"url": image}} for image in imageList]
    content_partial.append({"type": "text", "text": IMAGE_PARSE_PROMPT})
    if additionalInfo:
        content_partial.append({"type": "text", "text": additionalInfo})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": content_partial
            }
        ],
        temperature=1,
        max_tokens=2048,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        response_format={
            "type": "text"
        }
    )
    return response.choices[0].message.content

@app.route('/api/chat', methods=['POST'])
def chat():
    # Parse form data into JSON
    p_json = request.form.to_dict(flat=False)
    imageList = request.files
    additionalInfo = p_json.get('additionalInfo')[0]
    additionalQuestions = p_json.get('additionalQuestions')[0]
    
    if not imageList:
        return jsonify({'error': 'Images are required'}), 400
    
    # Reformat image data to be compatible with OpenAI API
    # Get image data from <FileStorage> object and determine MIME type
    imageList = [
        f"data:{image.content_type};base64,{base64.b64encode(image.read()).decode('utf-8')}"
        for image in imageList.getlist('images')
    ]

    response = get_openai_response(imageList, additionalInfo)

    if additionalQuestions:
        response += f"\n{additionalQuestions}"

    vapi_override_message = {
        'firstMessage': "Welcome to this interview! I'd love to ask you some questions - let's get started!",
        'model': {
            'provider': "openai",
            'model': "gpt-3.5-turbo",
            'messages': [
                {
                    'role': "system",
                    'content': INTERVIEW_PROMPT,
                },
                {
                    'role': "system",
                    'content': response,
                },
            ],
        },
    }

    return jsonify({'response': vapi_override_message})

@app.route('/')
def index():
    return render_template('vapi.html')

if __name__ == '__main__':
    app.run(debug=True, port=8080)