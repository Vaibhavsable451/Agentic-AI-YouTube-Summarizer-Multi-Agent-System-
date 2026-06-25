from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable,
)
from urllib.parse import urlparse, parse_qs
import re

# Exception names changed between library versions:
#   0.6.x -> TooManyRequests
#   1.x   -> RequestBlocked, IpBlocked
# Import all defensively so this works regardless of installed version.
try:
    from youtube_transcript_api._errors import RequestBlocked
except ImportError:
    RequestBlocked = None

try:
    from youtube_transcript_api._errors import IpBlocked
except ImportError:
    IpBlocked = None

try:
    from youtube_transcript_api._errors import TooManyRequests
except ImportError:
    TooManyRequests = None

# Tuple of "blocked" exceptions that actually exist in this install
_BLOCKED_EXCEPTIONS = tuple(
    exc for exc in (RequestBlocked, IpBlocked, TooManyRequests) if exc is not None
)


class TranscriptAgent:

    def get_video_id(self, url: str) -> str:

        # youtu.be/xxxx
        if "youtu.be" in url:
            return url.split("/")[-1].split("?")[0]

        # youtube.com/watch?v=xxxx
        parsed = urlparse(url)
        if parsed.hostname in ("www.youtube.com", "youtube.com", "m.youtube.com"):
            qs = parse_qs(parsed.query)
            if "v" in qs:
                return qs["v"][0]

        # fallback regex (also catches /shorts/xxxx)
        match = re.search(r"(?:v=|/shorts/|youtu\.be/)([0-9A-Za-z_-]{11})", url)
        if match:
            return match.group(1)

        raise ValueError("Invalid YouTube URL — could not extract video ID")

    def get_transcript(self, url: str) -> str:

        video_id = self.get_video_id(url)

        # current (v1.x) API — instance based, no more classmethod .get_transcript()
        ytt_api = YouTubeTranscriptApi()

        try:
            fetched = ytt_api.fetch(video_id, languages=["en", "hi"])

            # Older versions return list[dict] (item["text"]),
            # newer versions return FetchedTranscript of objects (item.text)
            pieces = []
            for item in fetched:
                if isinstance(item, dict):
                    pieces.append(item["text"])
                else:
                    pieces.append(item.text)

            return " ".join(pieces)

        except TranscriptsDisabled:
            raise RuntimeError(
                "Captions are disabled on this video. Try a different video."
            )

        except NoTranscriptFound:
            raise RuntimeError(
                "No transcript available in en/hi for this video."
            )

        except VideoUnavailable:
            raise RuntimeError(
                "This video is unavailable (private/deleted/region-locked)."
            )

        except _BLOCKED_EXCEPTIONS:
            raise RuntimeError(
                "YouTube blocked this request (rate-limit/IP block). "
                "Wait a bit and retry, or configure a proxy "
                "(see youtube_transcript_api.proxies.GenericProxyConfig)."
            )

        except Exception as e:
            # last resort — surfaces the real underlying error instead of
            # a confusing raw XML ParseError bubbling up to Streamlit
            raise RuntimeError(f"Transcript fetch failed: {e}")