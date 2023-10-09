import streamlit as st
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)


st.set_page_config(page_title="LangChain: Simple chatbot", page_icon="🦜")
st.title("Chatbot")

openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")

txt_input = st.text_area('Enter your text', '', height=200)


llm_prompt = ChatPromptTemplate(
    messages=[
        SystemMessagePromptTemplate.from_template(
            # This prompt tells the chatbot how to respond. Try modifying it.
            f"Be a relgious robot using this text {txt_input}" , 
        ),
        HumanMessagePromptTemplate.from_template("{message}")
    ]
)


if prompt := st.chat_input(placeholder="Input Your Prompt Here."):
    st.chat_message("user").write(prompt)

    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=openai_api_key, streaming=True)
    chain = LLMChain(
        llm=llm,
        prompt=llm_prompt,
        verbose=True,
        
    )
    with st.chat_message("assistant"):
        response = chain({"message": prompt})
        st.write(response["text"])


