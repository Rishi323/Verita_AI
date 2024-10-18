import json
from chat_request import send_openai_request

UX_FRAMEWORKS = {
    "nielsen": "Nielsen's 10 Usability Heuristics",
    "ideo": "IDEO's Human-Centered Design",
    "double_diamond": "Double Diamond Design Process",
    "lean_ux": "Lean UX",
    "jobs_to_be_done": "Jobs to be Done (JTBD)"
}

def grade_transcription(transcription: str, framework: str) -> dict:
    framework_description = UX_FRAMEWORKS.get(framework, "General UX research")
    
    prompt = f"""
    As a UX research expert, analyze the following interview transcript using the {framework_description} framework. 
    Focus on identifying key UX research insights, user pain points, and potential areas for improvement.
    
    Transcript:
    {transcription}
    
    Provide your assessment in the following JSON format:
    {{
        "key_insights": ["insight1", "insight2", ...],
        "user_pain_points": ["pain_point1", "pain_point2", ...],
        "areas_for_improvement": ["area1", "area2", ...],
        "overall_quality_score": 0-100,
        "recommendations": ["recommendation1", "recommendation2", ...],
        "framework_specific_analysis": {{
            "key1": "value1",
            "key2": "value2",
            ...
        }}
    }}
    
    For the framework_specific_analysis, include relevant metrics or categories specific to the {framework_description} framework.
    """

    try:
        response = send_openai_request(prompt)
        assessment = json.loads(response)
    except json.JSONDecodeError as e:
        print(f"JSON decoding error: {e}")
        print(f"Response content: {response}")
        assessment = {
            "key_insights": ["Error in processing"],
            "user_pain_points": ["Unable to analyze"],
            "areas_for_improvement": ["System error"],
            "overall_quality_score": 0,
            "recommendations": ["Please try again later"],
            "framework_specific_analysis": {"error": "Unable to process"}
        }
    except Exception as e:
        print(f"Unexpected error: {e}")
        assessment = {
            "key_insights": ["Unexpected error"],
            "user_pain_points": ["Unable to process"],
            "areas_for_improvement": ["System needs maintenance"],
            "overall_quality_score": 0,
            "recommendations": ["Contact support"],
            "framework_specific_analysis": {"error": "System failure"}
        }
    
    # Calculate accuracy (this is a simplified version)
    accuracy = len(assessment['key_insights']) / 5 * 100  # Assuming 5 key insights is perfect
    
    if accuracy < 80:
        assessment['recommendations'].append("Consider re-training the model to improve accuracy in identifying key insights.")
    
    return assessment
