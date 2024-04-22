import streamlit as st
from unify import Unify
import config


def main():
    st.title("Interface")

    # Input for UNIFY_KEY
    with st.sidebar:
        unify_key = st.text_input("Enter your UNIFY_KEY:", type="password")
        
        # Dropdown for choosing LLM
        llms = (config.llms)

        # Dropdown for choosing LLM
        llm_selected = st.selectbox("Choose an LLM:", list(llms.keys()))

        # Dropdown for choosing provider based on selected LLM
        available_providers = llms[llm_selected]
        provider_selected = st.selectbox("Choose a provider:", available_providers)
        

    with st.form(key="prompt_form"):
        # Input for entering prompt
        user_prompt = st.text_area("Enter your prompt:")
        submitted = st.form_submit_button("Submit")

    
    if submitted:
        if unify_key:
            if user_prompt:
                # Initialize Unify with provided key, model, and provider
                unify = Unify(api_key=unify_key, model=llm_selected, provider=provider_selected)
                # Generate response using provided prompt
                response = unify.generate(user_prompt=user_prompt)
                # Display response
                st.write("Response:")
                st.write(response)
            else:
                st.warning("Please enter a prompt.")
        else:
            st.error("Please enter your UNIFY_KEY.")


if __name__ == "__main__":
    main()


        