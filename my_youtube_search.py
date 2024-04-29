# Import the YouTubeSearchTool from the langchain_community.tools module
from langchain_community.tools import YouTubeSearchTool

# Create an instance of YouTubeSearchTool
tool = YouTubeSearchTool()

# Use a try-except block to handle potential errors during the search
try:
    # Run the tool with the search query "lex friedman"
    results = tool.run("lex friedman")
    # Print the results of the search
    print(results)
except Exception as e:
    # Print an error message if an exception occurs
    print(f"An error occurred: {e}")