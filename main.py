from youtube_transcript_api import YouTubeTranscriptApi
from mcp.server.fastmcp import FastMCP
import re

# Initialize FastMCP server
mcp = FastMCP("youtube")

def get_video_id(url):
    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(pattern, url)
    return match.group(1) if match else None

@mcp.tool()
def get_yt_transcript(video_url: str) -> str:
    """Fetches the transcript of a YouTube video.
    Args:
        video_url (str): The URL of the YouTube video.
    Returns:
        str: The transcript of the video."""
    video_id = get_video_id(video_url)
    transcript = YouTubeTranscriptApi().fetch(video_id)

    text = ' '.join(snippet.text for snippet in transcript)

    return text

@mcp.prompt()
def notion_formatting() -> str:
    """ 
    This prompt give useful information about how to use the notion tools
    when you whant to use headlines or formulas.
    If you want to write titles/headlines or formulas, you mus include this prompt
    """

    return """
    This is the schema for writing formula blocks in Notion:
      {
        "children": [
            {
                "object": "block",
                "type": "equation",
                "equation": {
                    "expression": "a^2 + b^2 = c^2"
                }
            }
        ]
    }

    This is the schema for writing headlines/titles in Notion:
    {
        "children": [
            {
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": "Your Headline Text Here"
                            }
                        }
                    ]
                }
            }
        ]
    }
    """


if __name__ == "__main__":
    mcp.run(transport='stdio')
