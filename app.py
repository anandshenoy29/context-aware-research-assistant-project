import os
import base64
import datetime
import tempfile
import streamlit as st
from dotenv import load_dotenv
from document_processor import process_document_to_retriever
from agent_builder import build_research_agent

def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return ""

load_dotenv()

st.set_page_config(page_title="Context-Aware Research Assistant", page_icon="logo.png", layout="centered")

st.markdown(
    f"""
    <style>
    div[data-testid="stChatInput"] {{
        padding-bottom: 0.3rem !important;
    }}
    
    div[data-testid="stChatInput"]::after {{
        content: "Copyright © {datetime.date.today().year} Anand Shenoy. All Rights Reserved.";
        display: block;
        width: 100%;
        text-align: center;
        color: gray;
        font-size: 0.8em;
        margin-top: 15px;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    div[data-testid="stElementContainer"]:has(.sticky-header-wrapper) {
        position: sticky;
        top: 2.875rem; 
        z-index: 999;
        background-color: white !important;
    }
    
    .sticky-header-wrapper {
        background-color: white;
        padding-top: 15px;
        padding-bottom: 15px;
        border-bottom: 1px solid #e6e6e6;
        margin-bottom: 0;
        width: 100%;
    }
    
    h1.main-title {
        margin-bottom: 0 !important;
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }
    </style>
    
    <div class="sticky-header-wrapper">
        <h1 class="main-title">Context-Aware Research Assistant</h1>
        <p style="color: gray; font-size: 0.9em; margin-top: 5px; margin-bottom: 0;">🚀 Powered by Gemini & LangChain</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "agent_executor" not in st.session_state:
    st.session_state.agent_executor = None

with st.sidebar:
    st.header("⚙️ Configuration")
    uploaded_file = st.file_uploader("Upload your PDF Document", type="pdf")
    
    if uploaded_file is None and st.session_state.agent_executor is not None:
        st.session_state.agent_executor = None
        st.session_state.messages = []  
        st.rerun()  

    st.markdown("---")
    st.markdown("### 💡 How it works")
    st.markdown("- **Upload:** Provide a PDF document.\n- **Process:** The AI reads and embeds the text.\n- **Ask:** Chat with the document directly!")

if uploaded_file and st.session_state.agent_executor is None:
    with st.spinner("Processing document and initializing AI... ⏳"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name

        st.session_state.agent_executor = build_research_agent(process_document_to_retriever(tmp_file_path))
        st.sidebar.success("✅ Document processed successfully!")
        os.unlink(tmp_file_path)

        st.session_state.messages = [] 

welcome_placeholder = st.empty() 

if len(st.session_state.messages) == 0:
    with welcome_placeholder.container():
        if st.session_state.agent_executor is None:
            st.info("👋 Welcome! Please upload a PDF in the sidebar to start asking questions.")
        else:
            st.info("✨ Document loaded and ready! Ask your first question below.")
        
        logo_base64 = get_base64_image("logo.png")
        
        st.markdown(
            f"""
            <style>
            .watermark-container {{
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                margin-top: 0vh; 
            }}
            .watermark-logo {{
                width: 200px;
                opacity: 0.15;
                margin-top: 0rem;
                margin-bottom: 0rem;
            }}
            </style>
            
            <div class="watermark-container">
                {f'<img src="data:image/png;base64,{logo_base64}" class="watermark-logo">' if logo_base64 else ''}
            </div>
            """,
            unsafe_allow_html=True
        )

for message in st.session_state.messages:
    avatar = "🧑‍💻" if message["role"] == "user" else "🤖"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a question about the document..."):
    welcome_placeholder.empty() 

    st.chat_message("user", avatar="🧑‍💻").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    if st.session_state.agent_executor is None:
        error_msg = "⚠️ **Oops!** Please upload a PDF document in the sidebar first so that I have something to search through."
        
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(error_msg)
        st.session_state.messages.append({"role": "assistant", "content": error_msg})
        
    else:
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Thinking... 💭"):
                response = st.session_state.agent_executor.invoke({"input": prompt})
                raw_output = response["output"]
                
                if isinstance(raw_output, list):
                    clean_text = "".join([
                        item["text"] if isinstance(item, dict) and "text" in item else str(item) 
                        for item in raw_output
                    ])
                else:
                    clean_text = str(raw_output)
                
                st.markdown(clean_text)
                st.session_state.messages.append({"role": "assistant", "content": clean_text})
