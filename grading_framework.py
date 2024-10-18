import json
from chat_request import send_openai_request

def grade_transcription(transcription: str) -> dict:
    prompt = f"""
    As a UX research expert, analyze the following interview transcript and provide an assessment. 
    Focus on identifying key UX research insights, user pain points, and potential areas for improvement.
    
    Transcript:
    {transcription}
    
    Provide your assessment in the following JSON format:
    {{
        "key_insights": ["insight1", "insight2", ...],
        "user_pain_points": ["pain_point1", "pain_point2", ...],
        "areas_for_improvement": ["area1", "area2", ...],
        "overall_quality_score": 0-100,
        "recommendations": ["recommendation1", "recommendation2", ...]
    }}
    """

    response = send_openai_request(prompt)
    assessment = json.loads(response)
    
    # Calculate accuracy (this is a simplified version)
    accuracy = len(assessment['key_insights']) / 5 * 100  # Assuming 5 key insights is perfect
    
    if accuracy < 80:
        assessment['recommendations'].append("Consider re-training the model to improve accuracy in identifying key insights.")
    
    return assessment
