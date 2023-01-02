import streamlit as st
from streamlit_chat import message
import requests
from langchain import LLMMathChain, HuggingFaceHub, OpenAI, SerpAPIWrapper, SQLDatabase, SQLDatabaseChain
from langchain.agents import initialize_agent, Tool

st.set_page_config(
    page_title="Streamlit Chat - Demo",
    page_icon=":robot:"
)

search = SerpAPIWrapper()


self_ask_with_search = initialize_agent(tools, llm, agent="self-ask-with-search", verbose=True)

st.header("Conversational Search")
st.markdown("This app searches Google and synthesizes an answer for you. For example, you can ask it 'What school did Barack Obama's wife go to?' ")

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

def query(payload):
	return search.run(payload)

def get_text():
    input_text = st.text_input("You: ", key="input")
    return input_text 


user_input = get_text()

if user_input:
    output = query({
        "inputs": {
            "past_user_inputs": st.session_state.past,
            "generated_responses": st.session_state.generated,
            "text": user_input,
        },"parameters": {"repetition_penalty": 1.33},
    })

    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)

if st.session_state['generated']:

    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')

