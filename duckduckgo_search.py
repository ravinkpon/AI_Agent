from langchain_community.tools import DuckDuckGoSearchRun

class DuckDuckGoSearch:
    def __init__(self):
        # Create an instance of duckduckgo_search
        self.tool = DuckDuckGoSearchRun()

    def execute_search(self, query):
        # Use a try-except block to handle potential errors during the search
        try:
            # Run the tool with the search query
            results = self.tool.run(query)
            # Return the results of the search
            return results
        except Exception as e:
            # Print an error message if an exception occurs
            print(f"An error occurred: {e}")
            return None
        
        
# # import asyncio
# # import sys
# from langchain_community.tools import DuckDuckGoSearchRun

# # Set the event loop policy to handle asyncio compatibility on Windows
# # if sys.platform == 'win32':
# #     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# # Initialize the DuckDuckGo search
# search = DuckDuckGoSearchRun()

# # Run a search query
# result = search.run("Obama's first name?")
# print(result)