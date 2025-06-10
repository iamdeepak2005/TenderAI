import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.title("Tender RAG Assistant")

# Upload Section
with st.form("upload_form"):
    uploaded_files = st.file_uploader("Upload Tender Documents", accept_multiple_files=True)
    submit = st.form_submit_button("Upload & Index")
    if submit and uploaded_files:
        files = [("files", (f.name, f.read(), f.type)) for f in uploaded_files]
        res = requests.post(f"{API_URL}/upload/", files=files)
        st.success(res.json().get("message"))

# Chat Section
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.markdown("---")
st.subheader("Chat with Tender Documents")

query = st.text_input("Ask a question...")
if st.button("Ask") and query:
    st.session_state.chat_history.append((query, []))
    container = st.empty()
    section_results = []

    with requests.post(f"{API_URL}/ask/", data={"question": query}, stream=True) as r:
        response_buffer = ""
        for chunk in r.iter_lines(decode_unicode=True):
            if chunk:
                response_buffer += chunk + "\n"
                section_results.append(chunk)
                container.markdown(f"**You:** {query}\n\n**Bot:**\n\n" + "\n\n".join(section_results))

    st.session_state.chat_history[-1] = (query, section_results)

# Display chat history
for q, a_chunks in reversed(st.session_state.chat_history):
    st.markdown(f"**You:** {q}")
    st.markdown(f"**Bot:**\n\n" + "\n".join(a_chunks))


