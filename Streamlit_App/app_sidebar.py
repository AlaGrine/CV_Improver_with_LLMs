import streamlit as st

from app_constants import list_Assistant_Languages, list_LLM_providers


def expander_model_parameters(
    LLM_provider="OpenAI",
    text_input_API_key="OpenAI API Key - [Get an API key](https://platform.openai.com/account/api-keys)",
    list_models=["gpt-3.5-turbo-0125", "gpt-3.5-turbo", "gpt-4-turbo-preview"],
    openai_api_key="",
    google_api_key="",
):
    """Add a text_input (for the API key) and a streamlit expander with models and parameters."""

    st.session_state.LLM_provider = LLM_provider

    if LLM_provider == "OpenAI":
        st.session_state.openai_api_key = st.text_input(
            text_input_API_key,
            value=openai_api_key,
            type="password",
            placeholder="insert your API key",
        )

    if LLM_provider == "Google":
        st.session_state.google_api_key = st.text_input(
            text_input_API_key,
            type="password",
            value=google_api_key,
            placeholder="insert your API key",
        )

    with st.expander("**Models and parameters**"):
        st.session_state.selected_model = st.selectbox(
            f"Choose {LLM_provider} model", list_models
        )
        # model parameters
        st.session_state.temperature = st.slider(
            "temperature",
            min_value=0.1,
            max_value=1.0,
            value=0.7,
            step=0.1,
        )
        st.session_state.top_p = st.slider(
            "top_p",
            min_value=0.1,
            max_value=1.0,
            value=0.95,
            step=0.05,
        )


def sidebar(openai_api_key, google_api_key, cohere_api_key):
    """Create the sidebar."""

    with st.sidebar:
        st.caption(
            "🚀 A resume scanner powered by 🔗 Langchain, OpenAI and Google Generative AI"
        )
        st.write("")

        llm_chooser = st.radio(
            "Select provider",
            list_LLM_providers,
            captions=[
                "[OpenAI pricing page](https://openai.com/pricing)",
                "Rate limit: 60 requests per minute.",
            ],
        )

        st.divider()
        if llm_chooser == list_LLM_providers[0]:
            expander_model_parameters(
                LLM_provider="OpenAI",
                text_input_API_key="OpenAI API Key - [Get an API key](https://platform.openai.com/account/api-keys)",
                list_models=[
                    "gpt-3.5-turbo-0125",
                    "gpt-3.5-turbo",
                    "gpt-4-turbo-preview",
                ],
                openai_api_key=openai_api_key,
                google_api_key=google_api_key,
            )

        if llm_chooser == list_LLM_providers[1]:
            expander_model_parameters(
                LLM_provider="Google",
                text_input_API_key="Google API Key - [Get an API key](https://makersuite.google.com/app/apikey)",
                list_models=["gemini-pro"],
                openai_api_key=openai_api_key,
                google_api_key=google_api_key,
            )

        # Cohere API Key
        st.write("")
        st.session_state.cohere_api_key = st.text_input(
            "Coher API Key - [Get an API key](https://dashboard.cohere.com/api-keys)",
            type="password",
            value=cohere_api_key,
            placeholder="insert your API key",
        )

        # Assistant language
        st.divider()
        st.session_state.assistant_language = st.selectbox(
            f"Assistant language", list_Assistant_Languages
        )
