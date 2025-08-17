from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph,START,END
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage,BaseMessage
from typing import TypedDict,List,Annotated
from dotenv import load_dotenv
import os
load_dotenv()

api_keys=[os.getenv('google'),os.getenv('mistral_ai')]

model=ChatGoogleGenerativeAI(api_key=api_keys[0],model='gemini-2.5-flash')
memory=InMemorySaver()

class CHATBOT(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def bot(state: CHATBOT) -> CHATBOT['messages']:
    response=model.invoke(state['messages'])
    return {'messages':[response]}
configuration={'configurable':{'thread_id':'1'}}
graph=StateGraph(CHATBOT)

graph.add_node('chat',bot)
graph.add_edge(START,'chat')
graph.add_edge('chat',END)
workflow=graph.compile(checkpointer=memory)
