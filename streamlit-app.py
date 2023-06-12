
import streamlit as st
import openai 
import os
from presentation.presentation import Presentation


st.title('''Step 1: Lets generate your script''')

script_output = st.empty()
    

if "input" not in st.session_state:
    st.session_state["input"] = ""
if "temp" not in st.session_state:
    st.session_state["temp"] = ""
if "presentation" not in st.session_state:
    st.session_state['presentation'] = Presentation()



def clear_text():
    st.session_state["temp"] = st.session_state["input"]
    st.session_state["input"] = ""


# Define function to get user input
def get_text():
    """
    Get the user input text.

    Returns:
        (str): The text entered by the user
    """
    input_text = st.text_input("You: ", st.session_state["input"], key="input", 
                            placeholder="What would you like to change about the script?", 
                            on_change=clear_text,    
                            label_visibility='hidden')
    input_text = st.session_state["temp"]
    return input_text


with st.sidebar.form("Input"):

    api_key_input = st.text_input(
        "OpenAI API Key",
        type="password",
        placeholder="Paste your OpenAI API key here (sk-...)",
        help="You can get your API key from https://platform.openai.com/account/api-keys.",  # noqa: E501
        value=st.session_state.get("OPENAI_API_KEY", ""),
    )

    if api_key_input:
        st.session_state["api_key_configured"] = True
        openai.api_key = api_key_input


    st.markdown('----------------')

    topic = st.text_input(
        label='Presentation Topic:',
        value='Weekly product update',
        placeholder='e.g Weekly product update',
        help='What is the topic of your presentation'
    )

    audience = st.text_input(
        label='Audience:',
        value='Whole company',
        placeholder='e.g Whole company',
        help='Who is the audience?'
    )

    length = st.text_input(
        label='Length:',
        value='5 slides',
        placeholder='e.g 3-5 slides',
        help='Approximately how long do you want the presentation to be?'
    )

    goal = st.text_input(
        label='Goal:',
        value='''Inform the company on what we've worked on for the past week''',
        placeholder='''e.g Inform the company on what we've worked on for the past week''',
        help='What is your goal for the presentation'
    )

    important_points = st.text_area(
        label='Important points:',
        value='''
            * We finished the PoC for the VBA project
            * We started an AB test of our Autopilot project
            * We refactored the main landing page
        ''',
        help='What is your goal for the presentation'
    )
    
    btnResult = st.form_submit_button('Run')



if btnResult:
    if not st.session_state.get("api_key_configured"):
        st.error("Please configure your OpenAI API key!")
    else:
        st.session_state['presentation'].generate_script(topic, audience, length, goal, important_points)
        script_output.write(st.session_state['presentation'].get_whole_script())
        

user_input = get_text()

if user_input:
    if not st.session_state.get("api_key_configured"):
        st.error("Please configure your OpenAI API key!")
    else: 
        st.session_state['presentation'].update_script(user_input)
        script_output.write(st.session_state['presentation'].get_whole_script())

