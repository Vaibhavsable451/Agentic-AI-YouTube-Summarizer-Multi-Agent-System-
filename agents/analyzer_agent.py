from services.groq_service import ask_groq

class AnalyzerAgent:

    def analyze(self, transcript):

        prompt = f"""
        Analyze this transcript.

        Give:
        1. Main topic
        2. Keywords
        3. Concepts

        Transcript:
        {transcript[:6000]}
        """

        return ask_groq(prompt)