import streamlit as st
from unify import Unify
import config
from youtube_search import YouTubeSearch
from wolfram_alpha import WolframAlphaSearch
from openweathermap import OpenWeatherMapSearch
# from duckduckgo_search import DuckDuckGoSearch

def main():
    st.title("Interface")

    # Input for UNIFY_KEY
    with st.sidebar:
        unify_key = st.text_input("Enter your UNIFY_KEY:", type="password")
        
        # Dropdown for choosing LLM
        llms = (config.llms)

        # Dropdown for choosing LLM
        llm_selected = st.selectbox("Choose an LLM:", list(llms.keys()))

        # Dropdown for choosing provider based on selected LLM
        available_providers = llms[llm_selected]
        provider_selected = st.selectbox("Choose a provider:", available_providers)
        
        # Wolfarm app id
        wolfarm_app_id = st.text_input("Enter your Wolfarm App ID:", type="password")
        
        # opw api key
        opw_api_key = st.text_input("Enter your OpenWeatherMap API Key:", type="password")

    with st.form(key="prompt_form"):
        # Input for entering prompt
        user_prompt = st.text_area("Enter your prompt:")
        submitted = st.form_submit_button("Submit")
        
    if submitted:
        if unify_key and user_prompt:
            # Initialize Unify with provided key, model, and provider
            unify = Unify(api_key=unify_key, model=llm_selected, provider=provider_selected)
            # Generate response using provided prompt
            response = unify.generate(user_prompt=user_prompt)
            # Display response
            st.write("Response:")
            st.write(response)

        # if user_prompt:
        #     st.write("DuckDuckGo Search Results:")
        #     st.write(DuckDuckGoSearch().execute_search(user_prompt))
            
        if wolfarm_app_id and user_prompt:
            wolfram_search = WolframAlphaSearch(wolfarm_app_id)
            st.write("Wolfram Alpha Search Results:")
            st.write(wolfram_search.execute_query(user_prompt))

        if user_prompt:
            st.write("YouTube Search Results:")
            st.write(YouTubeSearch().execute_search(user_prompt))

        if opw_api_key and user_prompt:
            open_weather_search = OpenWeatherMapSearch(openweathermap_api_key=opw_api_key)
            st.write("Open Weather Map Search Results:")
            st.write(open_weather_search.execute_query(user_prompt))
            
            
        if not user_prompt:
            st.warning("Please enter a prompt.")



if __name__ == "__main__":
    main()

