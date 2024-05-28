from langchain.memory import ConversationBufferMemory
from langchain_unify.chat_models import ChatUnify
from langchain.agents import ConversationalChatAgent, AgentExecutor
from langchain_community.tools import DuckDuckGoSearchRun


class Duckduckgo:
    def __init__(self,llm_selected,provider_selected,unify_key):
        self.llm_selected = llm_selected
        self.provider_selected = provider_selected
        self.unify_key = unify_key
        self.creat_agent()
        
        
    def creat_agent(self):
        self.llm = ChatUnify(endpoint=f"{self.llm_selected}@{self.provider_selected}", unify_api_key=self.unify_key)
        self.tools = [DuckDuckGoSearchRun(name="Search")]
        self.chat_agent = ConversationalChatAgent.from_llm_and_tools(llm=self.llm, tools=self.tools)
        self.memory=ConversationBufferMemory(
                return_messages=True, memory_key="chat_history", output_key="output"
            )
        self.executor = AgentExecutor.from_agent_and_tools(
                        agent=self.chat_agent,
                        tools=self.tools,
                        #verbose=True,
                        memory=self.memory,
                        handle_parsing_errors=True,
                    )
            #return executor.invoke({"input":prompt})
    
    def run(self,prompt):
        response = self.executor.invoke({"input": prompt})
        return response
    
    

if __name__ == "__main__":
    duckduckgo = Duckduckgo('llm_selected', 'provider_selected', 'unify_key')
    response = duckduckgo.run('prompt')



# # Invoking the executor with the user prompt
# response = executor.invoke({"input": prompt})
    
# # Displaying the response in the Streamlit app
# st.chat_message("assistant").write(response["output"])

#todo

#performing well with duckduckgo
# may be some minor changes needed



