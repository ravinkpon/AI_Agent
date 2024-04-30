from langchain_community.utilities.wolfram_alpha import WolframAlphaAPIWrapper

class WolframAlphaSearch:
    def __init__(self,appid):
        # Create an instance of WolframAlphaAPIWrapper
        self.wolfram = WolframAlphaAPIWrapper(wolfram_alpha_appid=appid)

    def execute_query(self, query):
        # Run the query with Wolfram Alpha
        results = self.wolfram.run(query)
        # Return the results of the query
        return results