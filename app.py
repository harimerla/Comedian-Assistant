from langchain.llms import OpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage, BaseOutputParser
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
import streamlit as st

import os

from dotenv import load_dotenv

load_dotenv()

# Load the OpenAI API key from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize ChatOpenAI with the API key
chat = ChatOpenAI(temperature=0.6, openai_api_key=key)

if 'flowmessages' not in st.session_state:
    st.session_state['flowmessages'] = [
        SystemMessage(content='You are a comedian AI assistant')
    ]

# Ensure session state keys are initialized
if 'conversation' not in st.session_state:
    st.session_state['conversation'] = None
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = None

# Update error handling to log errors for debugging
def get_response_from_openai(question):
    try:
        st.session_state['flowmessages'].append(HumanMessage(content=question))
        answer = chat(st.session_state['flowmessages'])
        st.session_state['flowmessages'].append(AIMessage(content=answer.content))
        return answer.content
    except Exception as e:
        st.error(f"Error encountered: {e}")
        return "Error encountered"

st.set_page_config(page_title='Q&A demo')
st.header('Comedian ChatBot')

def reset_conversation():
  st.session_state.conversation = None
  st.session_state.chat_history = None
  st.session_state['flowmessages'].clear()
st.button('Reset Chat', on_click=reset_conversation)

try:
    for message in st.session_state['flowmessages']:
        if message.type == 'system':
            continue
        role = 'assistant' if message.type == 'ai' else 'user'
        with st.chat_message(role):
            st.markdown(message.content)

    if input := st.chat_input('Input: ', key='input'):
        with st.chat_message('user'):
            st.markdown(input)
        with st.chat_message('assistant'):
            response = get_response_from_openai(input)
            st.markdown(response)
except Exception as e:
    st.error(f"Unexpected error: {e}")
