from langchain.llms import OpenAI
import os
import streamlit as st

from dotenv import load_dotenv

load_dotenv()

def get_response_from_openai(question):
    llm = OpenAI(openai_api_key=os.getenv('OPENAI_API_KEY'), temperature=0.6, model='gpt-3.5-turbo-instruct')
    response = llm.predict(question)
    return response

st.set_page_config(page_title='Q&A demo')
st.header('LangChain Application')

input = st.text_input('Input: ', key='input')
response = get_response_from_openai(input)

submit = st.button("Ask a question")

if submit:
    st.subheader('The Response is')
    st.write(response)