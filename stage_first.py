from openai import OpenAI
from flask import Flask, request, jsonify

DEFAULT_PROMPT = "What is the main idea of these images?"

client = OpenAI()

app = Flask(__name__)

def get_openai_response(imageList, additionalInfo):
    content_partial = [{"type": "image", "url": image} for image in imageList]
    content_partial.append({"type": "text", "text": DEFAULT_PROMPT})
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

    return response.choices[0].message['content'][0]['text']

@app.route('/api/chat', methods=['POST'])
def chat():
    imageList = request.json.get('images')
    additionalInfo = request.json.get('additionalInfo')
    if not imageList:
        return jsonify({'error': 'Images are required'}), 400
    if not additionalInfo:
        return jsonify({'error': 'Additional information is required'}), 400
    
    # reformat image data to be compatible with OpenAI API
    # data:image/jpeg;base64,
    imageList = [f"data:image/jpeg;base64,{image}" for image in imageList]

    response = get_openai_response(imageList, additionalInfo)
    return jsonify({'response': response})