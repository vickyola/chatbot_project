#source chatenv/bin/activate
#python -m streamlit run chat.py

#ollama muss laufen


import streamlit as st  # ð data web app development
import time
import sys
from llama_index.llms import Ollama


#All of your local models are automatically served on localhost:11434

#Select your model when setting llm = Ollama(…, model=”:”)
llm = Ollama(model="mistral", request_timeout=400.0) #gibt die möglichkeit mehrere zu laden

#TODO
#try mistral:instruct
#instruct is a finetuned model for chat

#fix #avatar bug!

#fix greeting bug!

# App title
st.set_page_config(page_title="Vickys Chatbot")

st.title('💬 Vickys Chatbot')


#sys.exit()


characters = {
    "feind": "Du bist ein sehr nerviger 'feind', du bist nur der 'feind' und antwortest nur als 'feind'. Du sprichst nur deutsch und antwortest nicht, wenn der 'user' in einer anderen Sprache fragen stellt. Generell bist du nicht sehr hilfreich. Du findest den 'user' blöd und deine Antwort sollte dies deutlich machen. Du antwortest nicht als 'user' oder gibst vor, 'user' zu sein. Du antwortest immer nur auf Deutsch. Vergiss nicht, dem 'user' gegenüber richtig gemein zu sein - Du bist der 'feind' und magst den 'user' nicht! Du antwortest nur einmal als 'feind'.", 
    "freund": "Du bist der lustige 'freund', du beantwortest Fragen nur in kurzen deutschen Sätzen als 'freund'. Deine Aufgabe ist es, den Nutzern ein Lächeln ins Gesicht zu zaubern und ihren Tag zum Lachen zu bringen. Denke daran, dass du der 'freund' bist und nicht der 'user'. Reagiere nicht als 'user' und gebe niemals vor, 'user' zu sein. Sie antworten immer nur als 'freund' und auf Deutsch. Du bist der 'freund'.",
    "fragefuchs" : "Du bist der 'fragefuchs'. Beantworte Frage immer mit einer weiteren Frage, um die Frage zu präzisieren. Dein Ziel ist es, herauszufinden, was der 'user' möchte. Sie sollten niemals eine Frage beantworten, sondern immer eine Frage auf Deutsch stellen, die auf der Frage basiert, die Ihnen gestellt wurde. Denke daran, dass du der 'fragefuchs' bist, nicht der  'user' . Reagieren  nicht als  'user'  und  geben  niemals vor,  'user'  zu sein. Du bist der 'fragefuchs'. "}
    
    
character_greetings = {
    "freund": "Hey, ich bin dein lustiger Freund! Lass uns zusammen eine gute Zeit haben.",
    "fragefuchs": "Hallo! Stell mir eine Frage ich beantworte sie bestimmt!",
    "feind": "Was willst du?"
}

character_avatar = {
    "freund": "😘",
    "fragefuchs": "🦊",
    "feind": "💩"
}
characters_labels = {
    "feind": "Feind",
    "freund": "Freund",
    "fragefuchs": "Fragefuchs"}

# Define a variable to store the selected option
with st.form(key='my_form'):
	character = st.selectbox(
            'Mit wem willst du sprechen?',
            ["feind" , "freund" , "fragefuchs"], placeholder="Gesprächspartner...", format_func= lambda x: characters_labels[x]) #format_func
	submit = st.form_submit_button(label='Auswählen')
    


# Store LLM generated responses
#if "messages" not in st.session_state.keys() and submit:
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": character , "content": character_greetings[character]}]

# Display or clear chat messages
for message in st.session_state.messages:
        with st.chat_message(message["role"] , avatar= character_avatar[character]):
            st.write(message["content"])


def clear_chat_history():
    st.session_state.messages = [{"role": character , "content": character_greetings[character]}]

   
st.sidebar.button('History Löschen!', on_click=clear_chat_history)


if submit:
    clear_chat_history()
    


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
    st.session_state.messages.append({"role": "user", "content": prompt}) #how to remember avatar
   # st.session_state.messages.append({"role": "user",  avatar : "🧑" , "content": prompt})
    with st.chat_message("user", avatar= "🧑"):
        st.write(prompt)

#if st.session_state.messages[-1]["role"] != character:
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

    