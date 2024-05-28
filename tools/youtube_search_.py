from langchain_community.tools import YouTubeSearchTool
from langchain_unify.chat_models import ChatUnify
from langchain_community.document_loaders import YoutubeLoader
from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate
from datetime import timedelta
import ast



class YouTubeSearch:
    def __init__(self):
        self.api = YouTubeSearchTool()

    def run(self, query):
        results = self.api.run(f"{query},3")
        list_results = ast.literal_eval(results)
        list_thumbnail_url=[]
        list_title=[]
        for url in list_results:
            loader = YoutubeLoader.from_youtube_url(url, add_video_info=True)
            result = loader.load()
            if result:
                thumbnail_url = result[0].metadata.get("thumbnail_url")
                title = result[0].metadata.get("title")
                print(title, thumbnail_url)
                list_thumbnail_url.append(thumbnail_url)
                list_title.append(title)
            else:
                print(f"No video found for the URL: {url}")
        return {"output":list_thumbnail_url,"title":list_title,"url":list_results}
        

        

class VideoSummarizer:
    def __init__(self, unify_api_key, llm_selected, provider_selected):
        
        self.unify_api_key = unify_api_key
        self.llm_selected = llm_selected
        self.provider_selected = provider_selected

    def summarize_from_url(self,url):
        loader = YoutubeLoader.from_youtube_url(url, add_video_info=True)
        result = loader.load()

        llm = ChatUnify(endpoint=f"{self.llm_selected}@{self.provider_selected}", unify_api_key=self.unify_api_key, streaming=True)

        prompt_template = """Write a concise summary of the following text delimited by triple backquotes.
                          Return your response in bullet points which covers the key points of the text.
                          ```{text}```
                          BULLET POINT SUMMARY:
                          """
        prompt = PromptTemplate(template=prompt_template, input_variables=["text"])

        chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt)
        summary = chain.invoke(result)
        summarized_content = summary['output_text']
        
        #video length
        video_length = timedelta(seconds=result[0].metadata['length'])
        vid_len=f"Found video from {result[0].metadata['author']} that {video_length} is long "
        # print(vid_len)
        # print (summarized_content)
        return {"output": summarized_content, "video_length": vid_len}

url = None
api_key = None
llm_selected = None
provider_selected = None


if __name__ == "__main__":
    summarizer = VideoSummarizer( api_key, llm_selected, provider_selected) 
    Yt = YouTubeSearch()
    Yt.run("prompt")
    #print(Yt.run("How to make a cake"))


#todo
#
# need to add memory to the agent 
#It cant handle to long video summaries
#if video is doesnt have thumbnail it will not display