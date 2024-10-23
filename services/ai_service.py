from openai import OpenAI
from config import Config

class AIService:
    def __init__(self):
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
    
    def generate_discussion_guide(self, study):
        prompt = self._create_guide_prompt(study)
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "system", "content": prompt}]
        )
        return response

    # New AI Features:
    # - generate_discussion_guide()
    # - analyze_session()
    # - moderate_session()
