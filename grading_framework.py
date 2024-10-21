import json
import logging
from chat_request import send_openai_request

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

UX_FRAMEWORKS = {
    "nielsen": "Nielsen's 10 Usability Heuristics",
    "ideo": "IDEO's Human-Centered Design",
    "double_diamond": "Double Diamond Design Process",
    "lean_ux": "Lean UX",
    "jobs_to_be_done": "Jobs to be Done (JTBD)",
    "jump_associates": "Jump Associates' UX Research Framework"
}

def grade_transcription(transcription: str, framework: str) -> dict:
    framework_description = UX_FRAMEWORKS.get(framework, "General UX research")
    
    # Check for empty or very short inputs
    if not transcription or len(transcription.split()) < 10:
        logger.warning(f"Short or empty input detected: {transcription}")
        return {
            "key_insights": ["Input too short for meaningful analysis"],
            "user_pain_points": ["Unable to identify pain points from short input"],
            "areas_for_improvement": ["Provide more detailed transcription for better analysis"],
            "overall_quality_score": 0,
            "recommendations": ["Ensure the transcription is complete and detailed enough for analysis"],
            "framework_specific_analysis": {"error": "Input too short for framework-specific analysis"}
        }
    
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
    Quote specific lines from the transcript to provide supporting evidence for framework_specific_analysis and include the exact timestamp from the transcript at which each line can be found.
    Do not paraphrase the lines you quote, they must match the transcript word for word.
    """

    try:
        logger.info(f"Sending request to OpenAI API for framework: {framework}")
        response = send_openai_request(prompt)
        response = response[response.find('```json')+7:]
        response = response[:response.find('```')]
        assessment = json.loads(response)
        logger.info("Successfully received and parsed OpenAI API response")
        
        # Validate the assessment structure
        required_keys = ["key_insights", "user_pain_points", "areas_for_improvement", "overall_quality_score", "recommendations", "framework_specific_analysis"]
        for key in required_keys:
            if key not in assessment:
                raise ValueError(f"Missing required key in assessment: {key}")
        
        # Ensure overall_quality_score is within the correct range
        assessment["overall_quality_score"] = max(0, min(100, assessment["overall_quality_score"]))
        
        return assessment
    except json.JSONDecodeError as e:
        logger.error(f"JSON decoding error: {e}")
        logger.error(f"Response content: {response}")
        return create_error_assessment("JSON parsing error")
    except ValueError as e:
        logger.error(f"Value error in assessment: {e}")
        return create_error_assessment(str(e))
    except Exception as e:
        logger.error(f"Unexpected error in grade_transcription: {e}")
        return create_error_assessment("Unexpected error")

def create_error_assessment(error_message: str) -> dict:
    return {
        "key_insights": [f"Error: {error_message}"],
        "user_pain_points": ["Unable to analyze due to error"],
        "areas_for_improvement": ["Improve system's error handling"],
        "overall_quality_score": 0,
        "recommendations": ["Please try again or contact support if the issue persists"],
        "framework_specific_analysis": {"error": error_message}
    }
