import streamlit as st
import requests

# ==== Configuration ====
FASTAPI_URL = "http://127.0.0.1:8000"
UPLOAD_ENDPOINT = f"{FASTAPI_URL}/documents/upload"
ASK_ENDPOINT = f"{FASTAPI_URL}/ask/"
PDF_ENDPOINT = f"{FASTAPI_URL}/ask/pdf/"

# ==== Page Setup ====
st.set_page_config(page_title="Tender AI Assistant", page_icon="📄💬")
st.title("📄 Tender AI Assistant")

# ==== File Upload ====
st.subheader("📤 Upload Tender PDF")
uploaded_files = st.file_uploader("Upload one or more PDF files", type=["pdf"], accept_multiple_files=True)

if uploaded_files:
    with st.spinner("Uploading and processing documents..."):
        files = [("files", (file.name, file.read(), "application/pdf")) for file in uploaded_files]
        response = requests.post(UPLOAD_ENDPOINT, files=files)

    if response.status_code == 200:
        st.success("✅ Files processed successfully.")
    else:
        st.error(f"❌ Upload failed: {response.text}")

# ==== Chat UI ====
st.subheader("💬 Chat with Tender AI")

# Store chat messages
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display previous messages
for msg in st.session_state.chat_history:
    st.chat_message(msg["role"]).markdown(msg["content"])

# Input + Type selector
with st.form("chat_form"):
    col1, col2 = st.columns([4, 1])
    with col1:
        user_query = st.text_input("Ask a question about the tender...")
    with col2:
        qtype = st.selectbox("Type", ["Chat", "Summary PDF", "Detail PDF"])
    submit_btn = st.form_submit_button("Send")

if submit_btn and user_query:
    # Show user input
    st.chat_message("user").markdown(user_query)
    st.session_state.chat_history.append({"role": "user", "content": user_query})

    if qtype == "Chat":
        # Streaming Chat Response
        response_container = st.chat_message("assistant")
        full_response = ""
        with st.spinner("Thinking..."):
            try:
                placeholder = response_container.empty()
                with requests.post(ASK_ENDPOINT, data={"question": user_query}, stream=True) as res:
                    if res.status_code == 200:
                        for chunk in res.iter_lines(decode_unicode=True):
                            if chunk:
                                full_response += chunk + "\n"
                                placeholder.markdown(full_response)
                    else:
                        full_response = f"❌ Error: {res.text}"
            except Exception as e:
                full_response = f"⚠️ Exception: {str(e)}"
                placeholder.markdown(full_response)

        st.session_state.chat_history.append({"role": "assistant", "content": full_response})

    else:
        # PDF Download
        qtype_param = "summary" if "Summary" in qtype else "detail"
        with st.spinner("Generating PDF..."):
            res = requests.post(PDF_ENDPOINT, data={"question": user_query, "qtype": qtype_param})
            if res.status_code == 200:
                st.success("✅ PDF generated!")
                st.download_button(
                    label=f"📄 Download {qtype}",
                    data=res.content,
                    file_name=f"tender_{qtype_param}.pdf",
                    mime="application/pdf"
                )
            else:
                st.error(f"❌ Failed to generate PDF: {res.text}")






# import streamlit as st
# import requests

# # ==== Configuration ====
# FASTAPI_URL = "http://127.0.0.1:8000"
# UPLOAD_ENDPOINT = f"{FASTAPI_URL}/documents/upload"
# ASK_ENDPOINT = f"{FASTAPI_URL}/ask/"

# # ==== Page Setup ====
# st.set_page_config(page_title="Tender AI Assistant", page_icon="📄💬")
# st.title("📄 Tender AI Assistant")

# # ==== File Upload ====
# st.subheader("📤 Upload Tender PDF")
# uploaded_files = st.file_uploader("Upload one or more PDF files", type=["pdf"], accept_multiple_files=True)

# if uploaded_files:
#     with st.spinner("Uploading and processing documents..."):
#         files = [("files", (file.name, file.read(), "application/pdf")) for file in uploaded_files]
#         response = requests.post(UPLOAD_ENDPOINT, files=files)

#     if response.status_code == 200:
#         st.success("✅ Files processed successfully.")
#     else:
#         st.error(f"❌ Upload failed: {response.text}")

# # ==== Chat UI ====
# st.subheader("💬 Chat with Tender AI")

# # Store chat messages
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []

# # Display previous messages
# for msg in st.session_state.chat_history:
#     st.chat_message(msg["role"]).markdown(msg["content"])

# # Input message
# user_query = st.chat_input("Ask a question about the tender...")

# if user_query:
#     # Show user message
#     st.chat_message("user").markdown(user_query)
#     st.session_state.chat_history.append({"role": "user", "content": user_query})

#     # Stream LLM response
#     # Stream LLM response
#     response_container = st.chat_message("assistant")
#     full_response = ""
#     with st.spinner("Thinking..."):
#         try:
#             placeholder = response_container.empty()
#             with requests.post(ASK_ENDPOINT, data={"question": user_query}, stream=True) as res:
#                 if res.status_code == 200:
#                     for chunk in res.iter_lines(decode_unicode=True):
#                         if chunk:
#                             full_response += chunk + "\n"
#                             placeholder.markdown(full_response)  # Update only the new chunk
#                 else:
#                     full_response = f"❌ Error: {res.text}"
#         except Exception as e:
#             full_response = f"⚠️ Exception: {str(e)}"
#             placeholder.markdown(full_response)

#     st.session_state.chat_history.append({"role": "assistant", "content": full_response})
