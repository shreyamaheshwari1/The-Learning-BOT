
#  Tosha the learning chatbot

# the chatbot in your code integrates the embedchain library to understand and respond to user queries
#  based on the provided URLs. The chatbot accesses and processes these URLs and generates responses 
# using a combination of pre-trained models and natural language understanding techniques. 
# The conversation history is tracked and displayed in a chat-like format using Streamlit components. 
# The specifics of how the chatbot works under the hood are determined by the embedchain library and the models
#  it employs.



# First import all the dependencies 

import streamlit as st
from streamlit_chat import message
# start the app
from embedchain import OpenSourceApp
import os
from get_api_key import get_api_key
api_key = get_api_key()

# Set your OpenAI API key and organization ID
os.environ["OPENAI_API_KEY"] =api_key 
# Create a Streamlit app title and description

st.title("Meet Tosha The Learning BOT")

st.write("Just enter multiple URL links and ask questions to Her")

# Creating an instance for Tosha
zuck_bot = OpenSourceApp()

#This code allows the user to input a number of URLs and collects them into the url_inputs list.
num_links = st.number_input("Enter the number of URLs:",min_value=1,value=1,step=1)

url_inputs = []
for i in range(num_links):
    url = st.text_input(f"Enter URL {i+1}:",key=f'url_{i}')
    url_inputs.append(url)
# Add URLs to the Chatbot Instance:

for url in url_inputs:
    if url:
        zuck_bot.add("web_page",url)

# These functions define the chat functionality and initialize the session state, including history and past chat messages.
def conversation_chat(query):
    # This line calls the query method on the zuck_bot object, which is an instance of the OpenSourceApp. 
    # The query method is likely part of your chatbot's API, and it's used to get a response to the 
    # user's question. The response is stored in the result variable.
    result = zuck_bot.query(query)

    # This line appends a tuple containing the user's question (query) and the chatbot's response (result) 
    # to the 'history' list in the Streamlit session state. This keeps a record of the chat history.
    st.session_state['history'].append((query,result))
    return result

def intialize_session_state():
    # This line checks if the 'history' key is not already present in Streamlit's 
    # session state. If it's not present, it means this is the first time the app 
    # is run, and you need to initialize the 'history' list.
    if "history" not in st.session_state:
        st.session_state['history'] = []
    if 'generated' not in st.session_state:
        st.session_state['generated'] = ["Hello! Ask me anything about"]
    if "past" not in st.session_state:
        st.session_state['past'] = ['Hey!']

# Similar logic is applied to 'generated' and 'past', where you check if these keys 4
# are present in the session state and initialize them with default values if they're not.
# Basically these functions are to just initialize the different variables in case of a new session
def display_chat_histroy():
    reply_container = st.container()
    container =st.container()
    
    with container:
        # This code sets up a form with a text input field where the user can type their question. 
        # The clear_on_submit=True option clears the input field after submission. When the user clicks the 
        # "send" button, the form is submitted.
        with st.form(key='my_form',clear_on_submit=True):
            user_input = st.text_input("Question:",placeholder="Ask me about resources",key='input')
            submit_button = st.form_submit_button(label='send')
        
        if submit_button and user_input:
            output = conversation_chat(user_input)
            st.session_state['past'].append(user_input)
            st.session_state['generated'].append(output)
    
    if st.session_state['generated']:
        with reply_container:
            for i in range(len(st.session_state["generated"])):
                message(st.session_state['past'][i],is_user=True,key=str(i)+"_user",avatar_style="thumbs")
                message(st.session_state['generated'][i],key=str(i),avatar_style="fun-emoji")
#initialize the session_state
intialize_session_state()

#Display the chat history
display_chat_histroy()

