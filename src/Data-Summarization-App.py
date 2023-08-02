# Importing libraries
import pandas as pd

from langchain.chat_models import ChatOpenAI
from langchain.agents import create_pandas_dataframe_agent
from langchain.agents.agent_types import AgentType

import streamlit as st

# Streamlit framework
st.set_page_config(page_title='🦜🔗 Data Summarization App')
st.title('🦜🔗 Data Summarization App')

# Load CSV file
def load_csv(input_csv):
  df = pd.read_csv(input_csv)
  with st.expander('See DataFrame'):
    st.write(df)
  return df

# Generate LLM response
def generate_response(csv_file, input_query):
  # The language model we're going to use to control the agent
  llm = ChatOpenAI(model_name='gpt-3.5-turbo-0613', temperature=0.2, openai_api_key=openai_api_key)
  df = load_csv(csv_file)
  # Create Pandas DataFrame Agent
  agent = create_pandas_dataframe_agent(llm, df, verbose=True, agent_type=AgentType.OPENAI_FUNCTIONS)
  # Perform Query using the Agent
  response = agent.run(input_query)
  return st.success(response)

# Input widgets
uploaded_file = st.file_uploader('Upload a CSV file', type=['csv'])

question_list = [
  "How many rows are there?",
  "How many columns are there?",
  "Other"
  ]

query_text = st.selectbox('Select a query:', question_list, disabled=not uploaded_file)

# Application
if query_text is 'Other':
  query_text = st.text_input('Enter your query:', placeholder = 'Enter query here ...', disabled=not uploaded_file)

result = []
with st.form('myform', clear_on_submit=True):
    openai_api_key = st.text_input('OpenAI API Key', type='password', disabled=not (uploaded_file and query_text))
    submitted = st.form_submit_button('Submit', disabled=not(uploaded_file and query_text))
    if submitted and openai_api_key.startswith('sk-'):
        with st.spinner('Calculating...'):
            response = generate_response(uploaded_file, openai_api_key, query_text)
            result.append(response)
            del openai_api_key

if len(result):
    st.info(response)