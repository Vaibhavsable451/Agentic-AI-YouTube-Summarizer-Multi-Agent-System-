from agents.transcript_agent import TranscriptAgent
from agents.analyzer_agent import AnalyzerAgent
from agents.summary_agent import SummaryAgent
from agents.learning_agent import LearningAgent


class YouTubeAgentPipeline:

    def __init__(self):
        self.transcript_agent = TranscriptAgent()
        self.analyzer_agent = AnalyzerAgent()
        self.summary_agent = SummaryAgent()
        self.learning_agent = LearningAgent()

    def run(self, youtube_url):

        transcript = (
            self.transcript_agent
            .get_transcript(youtube_url)
        )

        analysis = (
            self.analyzer_agent
            .analyze(transcript)
        )

        summary = (
            self.summary_agent
            .summarize(transcript)
        )

        learning = (
            self.learning_agent
            .generate_learning_material(transcript)
        )

        return {
            "transcript": transcript,   # raw output of TranscriptAgent — now exposed to UI
            "analysis": analysis,       # raw output of AnalyzerAgent
            "summary": summary,         # raw output of SummaryAgent
            "learning": learning        # raw output of LearningAgent
        }