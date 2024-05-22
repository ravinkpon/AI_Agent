from langchain_community.tools import YouTubeSearchTool

class YouTubeSearch:
    def __init__(self):
        # Create an instance of YouTubeSearchTool
        self.tool = YouTubeSearchTool()

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