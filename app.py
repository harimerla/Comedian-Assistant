from langchain.llms import OpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage, BaseOutputParser
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
import streamlit as st

import os

from dotenv import load_dotenv

load_dotenv()

chat = ChatOpenAI(temperature=0.6)

if 'flowmessages' not in st.session_state:
    st.session_state['flowmessages'] = [
        SystemMessage(content='You are a comedian AI assistant')
    ]

def get_response_from_openai(question):
    try:
        st.session_state['flowmessages'].append(HumanMessage(content=question))
        answer = chat(st.session_state['flowmessages'])
        st.session_state['flowmessages'].append(AIMessage(answer.content))
        return answer.content
    except:
        return "Error encountered"

st.set_page_config(page_title='Q&A demo')
st.header('Comedian ChatBot')

def reset_conversation():
  st.session_state.conversation = None
  st.session_state.chat_history = None
  st.session_state['flowmessages'].clear()
st.button('Reset Chat', on_click=reset_conversation)

# submit = st.button("Ask a question")

try:

    for message in st.session_state['flowmessages']:
        if message.type=='system':
            continue
        role='assistant'
        if message.type=='human':
            role='user'
        with st.chat_message(role):
            st.markdown(message.content)

    if input := st.chat_input('Input: ', key='input'):
        with st.chat_message('user'):
            st.markdown(input)
        with st.chat_message('assistant'):
            response = get_response_from_openai(input)
            st.markdown(response)
            # st.subheader('The Response is')
            # st.write(response)

except:
    pass
