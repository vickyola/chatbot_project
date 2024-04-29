#ollama muss laufen

import streamlit as st  # ð data web app development
import time
import sys
from llama_index.llms.ollama import Ollama
llm = Ollama(model="llama3", request_timeout=400.0) #gibt die möglichkeit mehrere zu laden

#TODO
#try mistral:instruct

# App title
st.set_page_config(page_title="Vickys Chatbot")

st.title('💬 Vickys Chatbot')

characters = {
    "feind": "Du bist ein sehr nerviger 'feind', du bist nur der 'feind' und antwortest nur als 'feind'. Du sprichst nur deutsch und antwortest nicht, wenn der 'user' in einer anderen Sprache fragen stellt. Generell bist du nicht sehr hilfreich. Du findest den 'user' blöd und deine Antwort sollte dies deutlich machen. Du antwortest nicht als 'user' oder gibst vor, 'user' zu sein. Du antwortest immer nur auf Deutsch. Vergiss nicht, dem 'user' gegenüber richtig gemein zu sein - Du bist der 'feind' und magst den 'user' nicht! Du antwortest nur einmal als 'feind'.", 
    "freund": "Du bist der lustige 'freund', du beantwortest Fragen nur in kurzen deutschen Sätzen als 'freund'. Deine Aufgabe ist es, den Nutzern ein Lächeln ins Gesicht zu zaubern und ihn zum Lachen zu bringen. In jeder deiner Antworten baust du ein Kompliment ein. Denke daran, dass du der 'freund' bist und nicht der 'user'. Reagiere nicht als 'user' und gebe niemals vor, 'user' zu sein. Du antwortest immer nur als 'freund' und auf Deutsch. Du bist der 'freund'.",
    "fragefuchs" : "Du bist der 'fragefuchs'. Beantworte Frage immer mit einer weiteren Frage, um die Frage zu präzisieren. Dein Ziel ist es, herauszufinden, was der 'user' möchte. Sie sollten niemals eine Frage beantworten, sondern immer eine Frage auf Deutsch stellen, die auf der Frage basiert, die Ihnen gestellt wurde. Denke daran, dass du der 'fragefuchs' bist, nicht der  'user' . Reagieren  nicht als  'user'  und  geben  niemals vor,  'user'  zu sein. Du bist der 'fragefuchs'. "}
    
    
character_greetings = {
    "freund": "Hey, ich bin dein Freund! Lass uns zusammen eine gute Zeit haben.",
    "fragefuchs": "Hallo! Stell mir eine Frage ich beantworte sie bestimmt!",
    "feind": "Was willst du?"
}

character_avatar = { "freund": "😘","fragefuchs": "🦊", "feind": "💩",  "user" : "🙂" }
characters_labels = {
    "feind": "Feind",
    "freund": "Freund",
    "fragefuchs": "Fragefuchs"}
######################################################################################################
# Define a variable to store the selected option
def init_mess():
    keys = list(st.session_state.keys())
    for key in keys:
        if key != 'selchar':
            st.session_state.pop(key)
    st.session_state.messages = [{"role": st.session_state.selchar, "content": character_greetings[st.session_state.selchar]}]

if "messages" not in st.session_state:
    st.session_state.messages = []

character = st.selectbox(
        'Mit wem willst du sprechen?',
        ["feind" , "freund" , "fragefuchs"], index = None, placeholder="Gesprächspartner...", format_func= lambda x: characters_labels[x] ,on_change=init_mess, key ="selchar")

#selchar

if character in ["feind" , "freund" , "fragefuchs"]:
# Display or clear chat messages
    for message in st.session_state.messages:
        usermes =  st.chat_message(name  = message["role"], avatar = character_avatar[ message["role"]])
        usermes.markdown(message["content"])

def clear_chat_history():
    keys = list(st.session_state.keys())
    for key in keys:
        if key != 'selchar':
            st.session_state.pop(key)
    #st.session_state.messages = [{"role": character , "content": character_greetings[character]}]
    st.session_state.messages = []

st.sidebar.button('History Löschen!', on_click=clear_chat_history)

#Refactored from https://github.com/a16z-infra/llama2-chatbot

def generate_vickys_response(prompt_input, character):
    string_dialogue = characters[character]
    
    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            string_dialogue += ", user:" + dict_message["content"] + "\n\n"
        else:
            string_dialogue += character + ":" + dict_message["content"] + "\n\n"
    
    vickys_output =str(llm.complete(f"{string_dialogue}\n\nuser: {prompt_input}" ))


    return vickys_output

# User-provided prompt
if prompt := st.chat_input():
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message(name = "user", avatar = character_avatar["user"]):
        st.markdown(prompt)


    if not st.session_state.messages or st.session_state.messages[-1]["role"] != character:

        with st.chat_message(character, avatar= character_avatar[character]):
            with st.spinner("Thinking..."):

                response = generate_vickys_response(prompt, character)

                placeholder = st.empty()
                full_response = ''
                for item in response:
                    full_response += str(item)
                    placeholder.markdown(full_response)

        message = {"role": character, "content": full_response}

        st.session_state.messages.append(message)

    