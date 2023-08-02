# Importing libraries
from langchain.llms import OpenAI
from langchain import PromptTemplate

import streamlit as st

# Streamlit framework
st.set_page_config(page_title="🦜🔗 Blog Generator App")
st.title('🦜🔗 Blog Generator App')

# Generate LLM response
def generate_response(topic):
  llm = OpenAI(model_name='text-davinci-003', openai_api_key=openai_api_key)
  # Prompt
  template = 'As an experienced data scientist and technical writer, generate an outline for a blog about {topic}.'
  prompt = PromptTemplate(input_variables=['topic'], template=template)
  prompt_query = prompt.format(topic=topic)
  # Run LLM model and print out response
  response = llm(prompt_query)
  return st.info(response)

# Application
topic_text = st.text_input('Enter your keyword', '')

result = []
with st.form('myform', clear_on_submit=True):
    openai_api_key = st.text_input('OpenAI API Key', type='password')
    submitted = st.form_submit_button('Submit')
    if submitted and openai_api_key.startswith('sk-'):
        with st.spinner('Calculating...'):
            response = generate_response(topic_text)
            result.append(response)
            del openai_api_key

if len(result):
    st.info(response)