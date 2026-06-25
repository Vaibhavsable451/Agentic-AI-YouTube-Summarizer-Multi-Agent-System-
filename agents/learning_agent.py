from services.groq_service import ask_groq

class LearningAgent:

    def generate_learning_material(
        self,
        transcript
    ):

        prompt = f"""
        Create:

        1. Interview Questions
        2. Quiz Questions
        3. Important Notes

        Transcript:
        {transcript[:10000]}
        """

        return ask_groq(prompt)