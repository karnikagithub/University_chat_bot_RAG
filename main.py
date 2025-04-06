from dotenv import load_dotenv
load_dotenv()
from typing import Set
import streamlit as st
from streamlit_chat import message
from backend.core import run_llm  # Assuming this is where your run_llm function is defined

st.set_page_config(
    page_title="University Bot",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Add these imports
from PIL import Image
import requests
from io import BytesIO

# Function to create a string for source URLs
def create_sources_string(source_urls: Set[str]) -> str:
    if not source_urls:
        return ""
    sources_list = list(source_urls)
    sources_list.sort()
    sources_string = "sources:\n"
    for i, source in enumerate(sources_list):
        sources_string += f"{i+1}. {source}\n"
    return sources_string

# Function to get a profile picture from Gravatar based on email
def get_profile_picture(email):
    gravatar_url = f"https://www.gravatar.com/avatar/{hash(email)}?d=identicon&s=200"
    response = requests.get(gravatar_url)
    img = Image.open(BytesIO(response.content))
    return img


st.markdown(
    """
<style>
    .stApp {
        background-color: #ffffff;
        color: #000000;
    }
    .stTextInput > div > div > input {
        background-color: #f0f0f0;
        color: #000000;
        border: 1px solid #cccccc;
    }
    .stButton > button {
        background-color: #4CAF50;
        color: #ffffff;
        border-radius: 5px;
        padding: 8px 16px;
        border: none;
    }
    .stSidebar {
        background-color: #f7f7f7;
        color: #000000;
    }
    .stMessage {
        background-color: #f9f9f9;
        color: #000000;
    }
    .css-1d391kg {  /* Chat message container */
        background-color: #f9f9f9 !important;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Sidebar for user profile information
with st.sidebar:
    st.title("User Profile")

    # Replace these with actual user data
    user_name = "Karnika Srinath"
    user_email = "karnika.Srinath@example.com"

    profile_pic = get_profile_picture(user_email)
    st.image(profile_pic, width=150)
    st.write(f"**Name:** {user_name}")
    st.write(f"**Email:** {user_email}")

# Main header for the application
st.header("🤖 University Info ChatBot")

# Initialize session state to store chat history
if "chat_answers_history" not in st.session_state:
    st.session_state["chat_answers_history"] = []
    st.session_state["user_prompt_history"] = []
    st.session_state["chat_history"] = []

# Create a more modern layout with two columns
col1, col2 = st.columns([2, 1])

with col1:
    # User input field for the prompt
    prompt = st.text_input("Prompt", placeholder="Enter your message here...")

with col2:
    # Submit button to send the user input
    if st.button("Submit", key="submit"):
        prompt = prompt or "Hello"  # Default message if input is empty

if prompt:
    with st.spinner("Generating response..."):
        # Call the run_llm function with the user query and chat history
        generated_response = run_llm(
            query=prompt, chat_history=st.session_state["chat_history"]
        )

        print(generated_response,'-----generated_response------')

        # Extract source URLs and format the response
        sources = set(doc.metadata["source"] for doc in generated_response["source_documents"])
        formatted_response = (
            f"{generated_response['result']} \n\n"
            "Thanks for asking!! Let me know if anything else is needed 😊\n\n"
            f"{create_sources_string(sources)}"
        )

        # Save user input and AI response in session state
        st.session_state["user_prompt_history"].append(prompt)
        st.session_state["chat_answers_history"].append(formatted_response)
        st.session_state["chat_history"].append(("human", prompt))
        st.session_state["chat_history"].append(("ai", generated_response["result"]))

# Display chat history
if st.session_state["chat_answers_history"]:
    for generated_response, user_query in zip(
        st.session_state["chat_answers_history"],
        st.session_state["user_prompt_history"],
    ):
        st.chat_message("user").write(user_query)
        st.chat_message("assistant").write(generated_response)

# Footer for the application
st.markdown("---")
st.markdown("Powered by LangChain | Google-Gemini | Streamlit")
