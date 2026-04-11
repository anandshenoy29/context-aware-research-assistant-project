from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

def build_research_agent(retriever):
    
    @tool("Context_Database")
    def retriever_tool(query: str) -> str:
        """Use this tool FIRST to find answers inside the uploaded PDF document."""
        docs = retriever.invoke(query)
        return "\n\n".join([doc.page_content for doc in docs])
    
    web_search_tool = DuckDuckGoSearchRun(
        name="Web_Search",
        description="Use this tool to search the internet ONLY if the answer cannot be found in the Context_Database."
    )
    
    tools = [retriever_tool, web_search_tool]
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system",
         """You are a helpful research assistant who will only try to respond an appropriate answer to the question.
         Always try to answer using the Context_Database tool first.
         If the info isn't there, use the Web_Search tool. 
         Always mention which source you used whether its Context_Database or Web_Search tool.
         If you found the input not appropriate then kindly respond in a polite manner and tell the user to describe properly."""),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"), 
    ])
    
    agent = create_tool_calling_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True)
