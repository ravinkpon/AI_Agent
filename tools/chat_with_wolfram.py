from langchain.memory import ConversationBufferMemory
from langchain_unify.chat_models import ChatUnify
from langchain.agents import ConversationalChatAgent, AgentExecutor,load_tools,AgentType
import os




class WolframAlpha:
    def __init__(self,llm_selected,provider_selected,unify_key,wolfram_app_id,messages):
        self.llm_selected = llm_selected
        self.provider_selected = provider_selected
        self.unify_key = unify_key
        self.wolfram = wolfram_app_id
        self.messages = messages
        os.environ["WOLFRAM_ALPHA_APPID"] = wolfram_app_id
        self.creat_agent()
        
    def creat_agent(self):
        self.llm = ChatUnify(endpoint=f"{self.llm_selected}@{self.provider_selected}", unify_api_key=self.unify_key)
        self.tools = load_tools(["wolfram-alpha"],self.llm)
        self.chat_agent = ConversationalChatAgent.from_llm_and_tools(llm=self.llm, tools=self.tools)
        self.memory=ConversationBufferMemory(
                return_messages=True, memory_key="chat_history", output_key="output"
            )
        self.executor = AgentExecutor.from_agent_and_tools(
                        agent=self.chat_agent,
                        AgentExecutor=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                        tools=self.tools,
                        #verbose=True,
                        memory=self.memory,
                        handle_parsing_errors=True,
                        return_intermediate_steps=True #testing retunring intermediate steps
                    )
            #return executor.invoke({"input":prompt})
    
    def run(self,prompt,**callbacks):
        response = self.executor.invoke({"input": prompt},callbacks)
        #print (response["output"])
        return response

if __name__ == "__main__":
    wolfram = WolframAlpha('llm_selected','provider',"unify key","wolfram_app_id")
    response = wolfram.run('prompt')


    # wolfram.creat_agent()
    # wolfram.run('Whats the weather in New York yesterday?')
    # wolfram.run('Whats the weather?')

# todo

#need to test with wolfram alpha 