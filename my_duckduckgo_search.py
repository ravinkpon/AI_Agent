import asyncio
import sys
from langchain_community.tools import DuckDuckGoSearchRun

# Set the event loop policy to handle asyncio compatibility on Windows
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Initialize the DuckDuckGo search
search = DuckDuckGoSearchRun()

# Run a search query
result = search.run("Obama's first name?")
print(result)
