import streamlit as st
import requests

# ==== Configuration ====
FASTAPI_URL = "http://127.0.0.1:8000"
UPLOAD_ENDPOINT = f"{FASTAPI_URL}/documents/upload"
ASK_ENDPOINT = f"{FASTAPI_URL}/ask/"
PDF_ENDPOINT = f"{FASTAPI_URL}/ask/pdf/"
SCRAPE_ENDPOINT = f"{FASTAPI_URL}/scrape-google/"
DOWNLOAD_AND_SUMMARIZE_ENDPOINT = f"{FASTAPI_URL}/download-and-summarize/"

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

# ==== Web Search ====
st.subheader("🌐 Search the Web")
search_query = st.text_input("Enter your search query", key="search_query")
if st.button("Search Web"):
    if search_query:
        with st.spinner("Searching the web..."):
            # Call the scrape endpoint
            response = requests.post(SCRAPE_ENDPOINT, json={"prompt": search_query})
            if response.status_code == 200:
                search_results = response.json().get("results", [])
                st.session_state.search_results = search_results
            else:
                st.error(f"Search failed: {response.text}")
    else:
        st.warning("Please enter a search query")

# Display search results
if "search_results" in st.session_state and st.session_state.search_results:
    st.subheader("🔍 Search Results")
    
    # Initialize pagination state
    if "search_page" not in st.session_state:
        st.session_state.search_page = 0
        
    # Constants
    RESULTS_PER_PAGE = 10
    total_results = len(st.session_state.search_results)
    total_pages = (total_results + RESULTS_PER_PAGE - 1) // RESULTS_PER_PAGE
    
    # Display current page
    start_idx = st.session_state.search_page * RESULTS_PER_PAGE
    end_idx = min(start_idx + RESULTS_PER_PAGE, total_results)
    current_page_results = st.session_state.search_results[start_idx:end_idx]
    
    # Show page info
    st.caption(f"Showing results {start_idx+1}-{end_idx} of {total_results}")
    
    # Display results for current page
    for i, result in enumerate(current_page_results):
        title = result.get("title", "No Title")
        link = result.get("link", "#")
        snippet = result.get("description", "No description available.")
        
        # Use a button to trigger the download and summarization for this link
        if st.button(f"📄 {title}", key=f"result_{start_idx+i}"):
            with st.spinner(f"Downloading and summarizing {title}..."):
                # Call the download-and-summarize endpoint
                summary_response = requests.post(DOWNLOAD_AND_SUMMARIZE_ENDPOINT, params={"url": link})
                if summary_response.status_code == 200:
                    summary = summary_response.json().get("summary", "No summary available.")
                    # Append the summary as an assistant message in the chat
                    st.session_state.chat_history.append({"role": "assistant", "content": summary})
                else:
                    st.error(f"Summarization failed: {summary_response.text}")
        
        st.caption(link)
        st.write(snippet)
        st.divider()
    
    # Pagination controls
    col1, col2, col3 = st.columns([1, 1, 1])
    if col1.button("⏮️ Previous", disabled=(st.session_state.search_page == 0)):
        st.session_state.search_page -= 1
        st.experimental_rerun()
    
    col2.write(f"Page {st.session_state.search_page+1} of {total_pages}")
    
    if col3.button("⏭️ Next", disabled=(st.session_state.search_page == total_pages - 1)):
        st.session_state.search_page += 1
        st.experimental_rerun()

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
