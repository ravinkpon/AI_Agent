import streamlit as st
import utilities.config as config
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_community.callbacks import StreamlitCallbackHandler
from tools.chat_with_ddgo import Duckduckgo
from tools.chat_for_weather import OpenWeatherMap
from tools.chat_with_wolfram import WolframAlpha
from tools.youtube_search_ import YouTubeSearch, VideoSummarizer
import requests

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
        print("msgs",self.msgs.messages)
        for idx, msg in enumerate(self.msgs.messages):
            print("msg",msg)
            with st.chat_message(avatars[msg.type]):
                # render the intermediate steps
                for step in st.session_state.steps.get(str(idx), []):
                    if step[0].tool == "_Exception":
                        continue
                    with st.expander(f"**{step[0].tool}**: {step[0].tool_input}"):
                        st.write(step[0].log)
                        st.write(f"**{step[1]}**")
                st.write(msg.content)
                
        prompt = st.chat_input("Ask your question to the Agent")
                
        if prompt is not None:
            with st.chat_message(avatars["human"]):
                st.write(prompt)
            
            with st.chat_message("assistant"):
                st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
                # cfg = RunnableConfig()
                # cfg["callbacks"] = [st_cb]
                response = self.agent.run(prompt,callbacks=[st_cb])
                if self.service_selected == "YouTube":
                    self.display_yt_thumbnail(response)
                else: 
                    st.write(response["output"])
                    self.msgs.add_user_message(prompt)
                    self.msgs.add_ai_message(response["output"])
                    st.session_state.steps[str(len(self.msgs.messages)-1)] = response["intermediate_steps"]
    
                
    def create_llm_engine(self):
        if self.service_selected == "DuckDuckGo":
            self.agent = Duckduckgo(self.llm_selected,self.provider_selected,self.unify_key,self.msgs)
        
        elif self.service_selected == "YouTube":
            self.agent = YouTubeSearch()
            
        elif self.service_selected == "Wolfram Alpha":
            self.agent = WolframAlpha(self.llm_selected,self.provider_selected,self.unify_key,st.secrets["wolfram_app_id"],self.msgs) #secret key for wolfram alpha

        elif self.service_selected == "OpenWeatherMap":
            self.agent = OpenWeatherMap(self.llm_selected,self.provider_selected,self.unify_key,st.secrets["openweathermap_api_key"]) #secret key for openweathermap    
            
    
    def validate_api_key(self, api_key):
        # Example URL and headers for the validation request
        url = "https://api.unify.ai/v0/get_credits"
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            st.sidebar.success(f"Valid API key Balance_Credits: {int(data['credits'])}")
            st.session_state.api_key_valid = True
            # print(f"Credits: {data['credits']}")
            # print(f"User ID: {data['id']}")           
            return True
        except requests.exceptions.RequestException as e:
            st.sidebar.error(f"API key validation failed: {e}")
            st.session_state.api_key_valid = False
            return False

    
    def run(self):
        #st.sidebar.title("Sidebar")
        self.unify_key = st.sidebar.text_input("Enter your UNIFY_KEY:", type="password",key="unify_key") 
        valid_key_button = st.sidebar.button("Validate UNIFY_KEY")
        if valid_key_button:
            if self.validate_api_key(self.unify_key):
                True
            else:
                False


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

# bit slow in response
