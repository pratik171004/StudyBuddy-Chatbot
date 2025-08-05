import streamlit as st
from modules import study_assistant

# Initialize the study assistant
study_bot = study_assistant.StudyAssistant()

st.set_page_config(page_title="StudyBuddy Bot", layout="centered")

st.title("🤖 StudyBuddy – Your AI Study Companion")
st.markdown("Ask study questions and get instant answers!")

st.subheader("📖 Ask a Study Question")

# Initialize history
if "history" not in st.session_state:
    st.session_state.history = []

# Define callback to handle submission
def handle_question():
    question = st.session_state.user_question
    if question.strip():
        answer = study_bot.get_response(question)
        st.session_state.history.append((question, answer))
        st.session_state.user_question = ""  # Reset input

# Input box with callback on change
st.text_input("Your Question", key="user_question")
st.button("Ask", on_click=handle_question)

# Display all Q&A pairs
for q, a in reversed(st.session_state.history):
    st.write(f"**You:** {q}")
    st.success(f"**Bot:** {a}")