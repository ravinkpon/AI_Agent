from langchain_community.utilities import OpenWeatherMapAPIWrapper

class OpenWeatherMapSearch:
    def __init__(self, openweathermap_api_key):
        self.api_key = openweathermap_api_key
        # Create an instance of OpenWeatherMapAPIWrapper
        self.opw = OpenWeatherMapAPIWrapper(openweathermap_api_key=self.api_key)

    def execute_query(self, query):
        try:
            # Try to run the query with opw
            results = self.opw.run(query)
            # Return the results of the query
            return results
        except Exception:
            # If a NotFoundError is raised, print an error message
            return f"Sorry Unable to find the resource for your query '{query}'."