from services.groq_service import ask_groq

class SummaryAgent:

    def summarize(self, transcript):

        prompt = f"""
        Summarize this transcript.

        Provide:

        1. Executive Summary
        2. Detailed Summary
        3. Key Takeaways

        Transcript:
        {transcript[:10000]}
        """

        return ask_groq(prompt)