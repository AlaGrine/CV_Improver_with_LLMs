import streamlit as st

# LLM: openai
from langchain_openai import ChatOpenAI

# LLM: google_genai
from langchain_google_genai import ChatGoogleGenerativeAI

# dotenv and os
from dotenv import load_dotenv, find_dotenv
import os


def get_api_keys_from_local_env():
    """Get OpenAI, Gemini and Cohere API keys from local .env file"""
    try:
        found_dotenv = find_dotenv("keys.env", usecwd=True)
        load_dotenv(found_dotenv)
        try:
            openai_api_key = os.getenv("api_key_openai")
        except:
            openai_api_key = ""
        try:
            google_api_key = os.getenv("api_key_google")
        except:
            google_api_key = ""
        try:
            cohere_api_key = os.getenv("api_key_cohere")
        except:
            cohere_api_key = ""
    except Exception as e:
        print(e)

    return openai_api_key, google_api_key, cohere_api_key


def instantiate_LLM(
    LLM_provider, api_key, temperature=0.5, top_p=0.95, model_name=None
):
    """Instantiate LLM in Langchain.
    Parameters:
        LLM_provider (str): the LLM provider; in ["OpenAI","Google"]
        model_name (str): in ["gpt-3.5-turbo", "gpt-3.5-turbo-0125", "gpt-4-turbo-preview","gemini-pro"].
        api_key (str): google_api_key or openai_api_key
        temperature (float): Range: 0.0 - 1.0; default = 0.5
        top_p (float): : Range: 0.0 - 1.0; default = 1.
    """
    if LLM_provider == "OpenAI":
        llm = ChatOpenAI(
            api_key=api_key,
            model=model_name,
            temperature=temperature,
            model_kwargs={"top_p": top_p},
        )
    if LLM_provider == "Google":
        llm = ChatGoogleGenerativeAI(
            google_api_key=api_key,
            # model="gemini-pro",
            model=model_name,
            temperature=temperature,
            top_p=top_p,
            convert_system_message_to_human=True,
        )

    return llm


def instantiate_LLM_main(temperature, top_p):
    """Instantiate the selected LLM model."""
    try:
        if st.session_state.LLM_provider == "OpenAI":
            llm = instantiate_LLM(
                "OpenAI",
                api_key=st.session_state.openai_api_key,
                temperature=temperature,
                top_p=top_p,
                model_name=st.session_state.selected_model,
            )
        else:
            llm = instantiate_LLM(
                "Google",
                api_key=st.session_state.google_api_key,
                temperature=temperature,
                top_p=top_p,
                model_name=st.session_state.selected_model,
            )
    except Exception as e:
        st.error(f"An error occured: {e}")
        llm = None
    return llm
