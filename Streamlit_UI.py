import streamlit as st
import utilities.config as config
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from tools.chat_with_ddgo import Duckduckgo
from tools.chat_for_weather import OpenWeatherMap
from tools.chat_with_wolfram import WolframAlpha
from tools.youtube_search_ import YouTubeSearch, VideoSummarizer

class StreamlitApp:
    def __init__(self):
        self.unify_key = None
        self.radio_options = ["DuckDuckGo", "YouTube","Wolfram Alpha", "OpenWeatherMap"]
        self.dropdown_dict = config.llms
        self.msgs = StreamlitChatMessageHistory()

        st.session_state.steps = {}
        self.llm_selected = None
        self.provider_selected = None
        self.service_selected = None
        

    def handle_radio_change(self):
        st.session_state.radio_selection = st.sidebar.radio(
            "Select an Agent:", 
            self.radio_options, 
            index=self.radio_options.index(st.session_state.radio_selection)
        )
        if self.service_selected != st.session_state.radio_selection:
            self.service_selected = st.session_state.radio_selection
            self.create_llm_engine()
        
    
    def handle_first_dropdown_change(self):
        st.session_state.first_dropdown_selection = st.sidebar.selectbox(
            "Select an option:", 
            list(self.dropdown_dict.keys()), 
            index=list(self.dropdown_dict.keys()).index(st.session_state.get('first_dropdown_selection', 
                                                                             list(self.dropdown_dict.keys())[0]))
        )
        if self.llm_selected != st.session_state.first_dropdown_selection:
            self.llm_selected = st.session_state.first_dropdown_selection
            self.create_llm_engine()

    def handle_second_dropdown_change(self):
        # Ensure the second dropdown is reset if the first dropdown selection changes
        selected_key = st.session_state.first_dropdown_selection
        if 'second_dropdown_selection' not in st.session_state or st.session_state.second_dropdown_selection not in self.dropdown_dict[selected_key]:
            st.session_state.second_dropdown_selection = self.dropdown_dict[selected_key][0]

        st.session_state.second_dropdown_selection = st.sidebar.selectbox(
            "Select a sub-option:", 
            self.dropdown_dict[selected_key],
            index=self.dropdown_dict[selected_key].index(st.session_state.second_dropdown_selection)
            )
        if self.provider_selected != st.session_state.second_dropdown_selection:
            self.provider_selected = st.session_state.second_dropdown_selection
            self.create_llm_engine()
            
            
    def display_yt_thumbnail(self, response):
        thumbnail_urls = response["output"]
        titles = response["title"]
        urls = response["url"]
        summarizer = VideoSummarizer(self.unify_key, self.llm_selected, self.provider_selected)

        for thumbnail, title, url in zip(thumbnail_urls, titles, urls):
            st.image(thumbnail, caption=title, width=300)
            #print("url", url)

            def summarize_and_display(url):  # Define a helper function
                st.write(f"fetching summary...{title}")
                #print("url123", url)
                summary = summarizer.summarize_from_url(url)
                #print("summary", summary)
                st.markdown(summary["video_length"])
                st.markdown(summary['output'])

            if st.button(title, key=f"summary_{title}", on_click=summarize_and_display, args=(url,)):  # Pass url as argument
            # Button click logic happens here (already defined in summarize_and_display)
            # Consider adding st.experimental_rerun() here if needed for caching issues
                summarize_and_display(url)
                #st.experimental_rerun()
                
   
     
    def display_input_text_area(self):
        avatars = {"human": "user", "ai": "assistant"}
        for msg in self.msgs.messages:
            with st.chat_message(avatars[msg.type]):

                st.write(msg.content)
                
        prompt = st.chat_input("Ask your question to the Agent")
        
        if prompt is not None:
            with st.chat_message(avatars["human"]):
                st.write(prompt)
            
            with st.chat_message("assistant"):
                response = self.agent.run(prompt)
                if self.service_selected == "YouTube":
                    self.display_yt_thumbnail(response)
                else: 
                    st.write(response["output"])
                    self.msgs.add_user_message(prompt)
                    self.msgs.add_ai_message(response["output"])
                
    def create_llm_engine(self):
        if self.service_selected == "DuckDuckGo":
            self.agent = Duckduckgo(self.llm_selected,self.provider_selected,self.unify_key)
        
        elif self.service_selected == "YouTube":
            self.agent = YouTubeSearch()
            
        elif self.service_selected == "Wolfram Alpha":
            self.agent = WolframAlpha(self.llm_selected,self.provider_selected,self.unify_key,"ETGVRJ-H6QTRWUAJ5")
            
        elif self.service_selected == "OpenWeatherMap":
            self.agent = OpenWeatherMap(self.llm_selected,self.provider_selected,self.unify_key,"0c19de4beefa6628948a7ffe529b240e")

    
    def run(self):
        #st.sidebar.title("Sidebar")
        self.unify_key = st.sidebar.text_input("Enter your UNIFY_KEY:", type="password",key="unify_key") # handle if key is not entered todo
        # Handle radio button change
        if 'radio_selection' not in st.session_state:
            st.session_state.radio_selection = self.radio_options[0]
        self.handle_radio_change()
        
        # Handle dropdown change
        if 'first_dropdown_selection' not in st.session_state:
            #print("prob****",list(self.dropdown_dict.keys())[0])
            model = list(self.dropdown_dict.keys())[0]
            provider= self.dropdown_dict[model]
            st.session_state.first_dropdown_selection = model
            st.session_state.second_dropdown_selection = provider
        self.handle_first_dropdown_change()
        self.handle_second_dropdown_change()
        
        if len(self.msgs.messages) == 0 or st.sidebar.button("Reset chat history"):
            self.msgs.clear()
            self.msgs.add_ai_message("How can I help you?")
            #self.msgs.add_user_message("get")
            st.session_state.steps = {}
        
        # Main area
        st.title("Chat with Agent")
        self.display_input_text_area()
    
        

# if __name__ == "__main__":
#     app = StreamlitApp()
#     app.run()


#todo

# need to handle unify key not entered
# need to handle if key is not entered
# bit slow in response
