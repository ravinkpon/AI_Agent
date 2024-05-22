import streamlit as st 
import unify
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_unify.chat_models import ChatUnify
from langchain import hub
from langchain.agents import create_react_agent,AgentExecutor


# load_dotenv()

# look into caching again and also mp_fragment and load_llm and clear chat history 
# app should be fast
# context mode seems to be the best 


def reset():
    st.session_state.messages = []

st.title("Chat with Data")

api_key = st.sidebar.text_input("Unify AI Key",type="password")

def provider(model_name):
    dynamic = st.toggle("Dynamic Routing")
    if dynamic:
        providers = ["lowest-input-cost","lowest-output-cost","lowest-itl","lowest-ttft","highest-tks-per-sec"]
        provider_name = st.selectbox("Select a Provider",options=providers,index=1)
    else:
        provider_name = st.selectbox("Select a Provider",options=unify.list_providers(model_name))
    return provider_name

@st.experimental_fragment
def mp_fragment():
    model_name = st.selectbox("Select Model",options=unify.list_models(),index=7)
    provider_name = provider(model_name)
    return model_name,provider_name

@st.cache_resource
def load_agent(model_name,provider_name):
    llm = ChatUnify(endpoint=f"{model_name}@{provider_name}", unify_api_key=api_key, streaming=True,temperature=0)
    tools = [DuckDuckGoSearchRun(max_results=1, name="Intermediate Answer")]
    # Get the prompt to use - you can modify this!
    prompt = hub.pull("hwchase17/react")
    # Construct the ReAct agent
    agent = create_react_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    return agent_executor

with st.sidebar:
    model_name,provider_name = mp_fragment()
    agent_executor = load_agent(model_name,provider_name)
    st.sidebar.button("Clear Chat History",on_click=reset)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# if len(st.session_state.messages) == 0:
#     with st.chat_message("assistant"):
#         initial = " Follow this steps before asking questions about your data \n 1. Enter Unify API key \n 2. Select a Model and Provider using the sidebar \n 3. Upload a PDF file which is not encrypted \n 4. Any changes to sidebar will reset chat"
#         st.markdown(initial)
#         st.session_state.messages.append({"role": "assistant", "content": initial})

# Accept user input
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = st.write_stream(agent_executor.invoke(
            {"input": prompt}
        ))
        # response = st.write(response)
        st.session_state.messages.append({"role": "assistant", "content": response})