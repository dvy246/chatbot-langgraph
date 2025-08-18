import streamlit as st
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from backend import workflow
import uuid


def generate():
    """
    Generate a new thread_id using uuid.uuid4().
    
    Returns:
        uuid.UUID: The newly generated thread_id.
    """
    thread=uuid.uuid4()
    return thread
def reset_chat():

    """
    Reset the chat history and thread_id.

    This function clears the message history and generates a new thread_id. The new thread_id is then added to the chat_threads list.
    """
    st.session_state['message_history']=[]
    st.session_state['thread_id']=generate()
    add_thread(st.session_state['thread_id'])


def add_thread(thread_id):
    """
    Add a thread_id to the list of chat_threads.
    
    Args:
        thread_id (uuid.UUID): The thread_id to be added.

    If the thread_id is not already in the chat_threads list, it is added to the list.
    """
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def load_message(thread_id):
    """
    Load the message history from the given thread_id.

    This function retrieves the state of the workflow for the given thread_id and returns the message history stored in the state. If the state does not exist or the message history is not present in the state, an empty list is returned.

    Args:
        thread_id (uuid.UUID): The thread_id of the conversation.

    Returns:
        list[BaseMessage]: The message history of the conversation.
"""
    state = workflow.get_state(config={'configurable':{'thread_id':thread_id}})
    if state and state.values and 'messages' in state.values:
            return state.values['messages']
    return []

#st.session dict-> list of message history
if 'message_history' not in st.session_state:
    st.session_state['message_history']=[]

if 'thread_id' not in st.session_state:
    st.session_state['thread_id']=generate()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads']=[]

add_thread(st.session_state['thread_id'])

st.sidebar.title('Chatbot')
button=st.sidebar.button('New Chat')
st.sidebar.title("chats")

if button:
    reset_chat()


configuration={'configurable':{'thread_id':st.session_state['thread_id']}}

#loading the chat history from the thread ids and converting it into the session state format
for threads in st.session_state['chat_threads']:
    chat=st.sidebar.button(str(threads))
    if chat:
        st.session_state['thread_id'] = threads
        messages=load_message(thread_id=threads)
        temp_messages=[]
        for msg in messages:
            if isinstance(msg,HumanMessage):
                role='user'
            elif isinstance(msg,AIMessage):
                role='bot'
            temp_messages.append({'role':role,'content':msg.content})
        st.session_state['message_history']=temp_messages

# loading the conversation history       
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])
#user input
user_input=st.chat_input('Your message')

if user_input:
    #appending the user and bot message and showing them in the ui u
    st.session_state['message_history'].append({'role':'user ','content':user_input})
    with st.chat_message('user'):
        st.text(user_input)
    
    with st.chat_message('bot',avatar='🤖'):
        #streaning the response
        messages=[HumanMessage(content=user_input)]
        ai_message=st.write_stream(chunk.content for chunk,metadata in workflow.stream({"messages": messages}, config=configuration, stream_mode='messages'))
        st.session_state['message_history'].append({'role':'bot','content':ai_message})
