import streamlit as st
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from backend import workflow,configuration

#st.session dict-> list of message history
if 'message_history' not in st.session_state:
    st.session_state['message_history']=[]

#loading the message history
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
    
    response=workflow.invoke({'messages':HumanMessage(content=user_input)},config=configuration)
    ai=response['messages'][-1].content
    st.session_state['message_history'].append({'role':'bot ','content':ai})
    with st.chat_message('bot'):
        st.text(ai)