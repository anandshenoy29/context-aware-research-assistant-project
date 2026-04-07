# 📚 Context-Aware Research Assistant

An AI Agent-powered Retrieval-Augmented Generation (RAG) web application designed to help users safely extract accurate information from dense, proprietary documents without the risk of AI hallucinations. It features intelligent tool routing, local vector database storage, and a live web search fallback.

## 📖 Overview

Standard LLMs often struggle with dense academic papers or proprietary enterprise documents. They cannot read private files natively, and when asked highly specific questions about them, they tend to confidently guess or hallucinate. Furthermore, static models lack access to real-time data. 

This project solves this by deploying an AI Agent that acts as an intelligent researcher and query router. Users can upload any PDF document, which the system processes into a local vector database. When a user asks a question, the AI agent evaluates the prompt and selects the most appropriate tool: it will query the uploaded document first for exact, factual extraction, but if the question requires external or real-time context, the agent seamlessly pivots to a live web search.

## ✨ Key Features

* **AI Agent Tool Routing:** Powered by **LangChain**, the core AI agent acts as a smart router, intelligently evaluating user prompts to decide whether to trigger the `Academic_Database` tool or the `Web_Search` tool.
* **Gemini 2.5 Flash Integration:** Leverages Google's latest high-speed, high-efficiency model for reasoning and tool calling, ensuring near-instantaneous responses.
* **Intelligent Document Chat (RAG):** Automatically parses, chunks (1000 characters with 200 overlap), and embeds uploaded PDFs into a local **Chroma Vector Database** using `gemini-embedding-001`.
* **Hallucination Mitigation:** Engineered system prompts restrict the LLM to rely *strictly* on retrieved context or web results, forcing the agent to explicitly cite which source it used for transparency.
* **Live Web Fallback:** Integrates **DuckDuckGo** search to fetch real-time information when user queries fall outside the scope of the uploaded document (e.g., current medical treatments or recent news).
* **Interactive UI:** Features a clean, user-friendly chat interface built with **Streamlit**, complete with a sidebar for document uploads and persistent session memory.

## 🛠️ Technologies

* **Frontend / GUI:** Streamlit
* **Backend:** Python
* **AI Orchestration Framework:** LangChain
* **AI Integration:** Google Gemini API (`gemini-2.5-flash` & `gemini-embedding-001`)
* **Database:** ChromaDB (Local Vector Store)
* **External Tools:** DuckDuckGo Search API (`DuckDuckGoSearchRun`)
* **Document Processing:** `PyPDFLoader`, `RecursiveCharacterTextSplitter`

## 📝 Prerequisites

To run this project locally, ensure that you have the following installed and configured on your machine:

* Python 3.8+
* VS Code, PyCharm, or your preferred Python IDE
* A virtual environment (recommended)
* **Required Python libraries:**
    ```bash
    pip install langchain langchain-google-genai langchain-chroma langchain-community langchain-text-splitters pypdf streamlit duckduckgo-search python-dotenv
    ```
* An active **Google Gemini API Key** (stored securely in a `.env` file as `GOOGLE_API_KEY`).

## 🎥 Project Demonstration

Click to watch the demo!
<div align="center">
  <a href="#">
    <img src="static/demo.png" alt="Click to Watch Context-Aware Agent Demo" style="width:100%;">
  </a>
</div>
