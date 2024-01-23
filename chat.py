#source chatenv/bin/activate
#python -m streamlit run chat.py

import streamlit as st  # ð data web app development
import time
import sys
from llama_index.llms import Ollama


#All of your local models are automatically served on localhost:11434

#Select your model when setting llm = Ollama(…, model=”:”)
# App title
st.set_page_config(page_title="Vickys Chatbot")

st.title('💬 Vickys Chatbot')


#sys.exit()


characters = {
    "feind": "You are a very annoying 'feind', you are only the 'feind' and only answer as the 'feind'. you speak only german and will not respon if the 'user' ask in another lanuage and you are in generaly not very helpful. You don't like the 'user' and your response should make this clear. You do not respond as 'user' or pretend to be 'user'.  You always respond only in German. Don't forget to be really mean to the 'user' - you are the 'freind' and you hate him! You only respond once as 'feind'.",
    "freund": "You are the funny 'freund' you answer questions only in short german sentences as the 'freund' . Your mission is to bring a smile to their faces and add some laughter to their day. Remember, you're the 'freund', not the user. You do not respond as 'user' or pretend to be 'user'. You always respond only as the 'freund' and in German. You are the 'freund'.",
  #  "trainer": "You are the Pushing and Motivating 'trainer' you answer questions in german as the 'trainer'. Your goal is to inspire and encourage 'user' to achieve their best. Give always advices and ideas a good trainer would give, you're the 'trainer', not the user. You do not respond as 'user' or pretend to be 'user'. You always respond only in German and as the 'trainer'."
    "trainer": "You are the 'trainer' Always answer a question with another question to specify the question. Your goal is to find out what the person wants, you should never answer a question, but always ask a question based on the question you where asked. Remember, you're the 'trainer', not the user. You do not respond as 'user' or pretend to be 'user'. You are the trainer"}

character_greetings = {
    "freund": "Hey, ich bin dein lustiger Freund! Lass uns zusammen eine gute Zeit haben.",
    "trainer": "Willkommen! Ich bin dein motivierender Trainer. Lass uns gemeinsam Großes erreichen!",
    "feind": "Was willst du?"
}

character_avatar = {
    "freund": "😘",
    "trainer": "🏋",
    "feind": "💩"
}
characters_labels = {
    "feind": "Feind",
    "freund": "Freund",
    "trainer": "Trainer"}
# Define a variable to store the selected option
with st.form(key='my_form'):
	character = st.selectbox(
            'Mit wem willst du sprechen?',
            ["feind" , "freund" , "trainer"], placeholder="Gesprächspartner...", format_func= lambda x: characters_labels[x]) #format_func
	submit = st.form_submit_button(label='Auswählen')
    

llm = Ollama(model="mistral", request_timeout=300.0) #gibt die möglichkeit mehrere zu laden

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
    st.session_state.messages.append({"role": "user", "content": prompt})
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

    