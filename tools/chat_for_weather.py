from langchain.memory import ConversationBufferMemory
from langchain_unify.chat_models import ChatUnify
from langchain.agents import ConversationalChatAgent, AgentExecutor,load_tools
import os


class OpenWeatherMap:
    def __init__(self,llm_selected,provider_selected,unify_key,openweathermap_api_key):
        self.llm_selected = llm_selected
        self.provider_selected = provider_selected
        self.unify_key = unify_key
        #self.openweathermap_api_key = openweathermap_api_key
        os.environ["OPENWEATHERMAP_API_KEY"] = openweathermap_api_key
        self.create_agent()
        
    def create_agent(self):
        self.llm = ChatUnify(endpoint=f"{self.llm_selected}@{self.provider_selected}", unify_api_key=self.unify_key)
        self.tools = load_tools(["openweathermap-api"],self.llm)
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
    openweathermap = OpenWeatherMap('llm_selected','provider',"unify key","opw_api_key")
    # #openweathermap.creat_agent()
    # openweathermap.run('Whats the weather in New York yesterday?')
    # openweathermap.run('Whats the weather?')
    response = openweathermap.run('prompt')
    
# todo 

# need to update agent conversation chat agent is not performing well with openweather map