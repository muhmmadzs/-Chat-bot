# GPT‑Powered Chatbot Tool

This repository contains a simple yet extensible web application that allows a company to deploy a GPT‑powered chatbot for internal or customer‑facing use.  The chatbot is built around the OpenAI Chat API and demonstrates best practices for conversation management, security, and customization.  It can serve as a starting point for building more sophisticated chat assistants on your own data or business processes.

## Features

* **Web‑based interface** – A lightweight Flask application provides a chat UI that runs in any modern browser.  Messages are exchanged asynchronously with the server using JSON.
* **Conversation memory** – The application maintains a short history of the conversation to provide context for the model.  This helps the assistant answer follow‑up questions coherently.
* **Configurable system prompt** – The default system prompt sets the assistant’s tone and company‑specific guidance.  You can adjust the prompt to make the assistant more formal, friendly, or domain‑specialised.
* **Environment variables for secrets** – The OpenAI API key is loaded from an environment variable (`OPENAI_API_KEY`) so secrets are never hard‑coded.  You can optionally set `MODEL_NAME` to select a different ChatCompletion model (for example `gpt‑3.5‑turbo` or `gpt‑4o`).
* **Error handling** – The server reports errors from the API back to the client so users receive a graceful message rather than a crash.
* **Extensibility** – You can customise the frontend or backend to integrate company data (via embeddings and retrieval) or authentication.  See the notes below for guidance.

## Quick Start

1. **Prerequisites**

   * Python 3.8 or higher
   * An OpenAI API key

2. **Install dependencies**

   In the project root, create a virtual environment and install the required packages:

   ```bash
   cd gpt_chatbot_tool
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Set environment variables**

   Export your API key as an environment variable before running the server.  You can also set the model name here:

   ```bash
   export OPENAI_API_KEY="sk-..."      # required
   export MODEL_NAME="gpt-4o"          # optional, defaults to gpt-3.5-turbo
   ```

4. **Run the application**

   Start the Flask server:

   ```bash
   python app.py
   ```

   Then open your browser to `http://127.0.0.1:5000` and begin chatting.

## Customisation

### Adjusting the system prompt

The `system_prompt` variable in `app.py` defines how the assistant should behave.  It currently reads:

```python
system_prompt = (
    "You are a helpful assistant for ExampleCorp. \n"
    "You follow company policies, answer accurately, and maintain a polite, professional tone.\n"
    "If you don't know an answer, say you are unsure rather than guessing."
)
```

Replace `ExampleCorp` with your company name and modify the tone or policies as needed.  To keep conversations concise, avoid extremely long system prompts – a few sentences are usually sufficient.

### Increasing conversation memory

The application stores the last 10 messages when calling the model.  You can adjust this by changing `history_length` in `app.py`.  Remember that larger contexts consume more tokens and will increase API costs.

### Integrating your own knowledge base

Large language models like GPT have limited knowledge of proprietary or recent information.  To build a chatbot that can answer questions about your own documents, product manuals, or policies, you can augment the model with a retrieval pipeline:

1. **Generate embeddings** – Convert your documents into vector embeddings.  OpenAI’s embedding API or open‑source models such as SBERT (Sentence‑BERT) can do this.  Each chunk of text is represented as a high‑dimensional vector that captures semantic meaning【619114781588450†L260-L278】.
2. **Store embeddings in a vector database** – Use a specialised database such as Pinecone, Weaviate or Milvus to store and query these vectors【619114781588450†L327-L334】.  When the user asks a question, compute the embedding of the query and search for the most relevant chunks.
3. **Retrieve and compose context** – Fetch the top‑N matching text chunks and include them in the prompt sent to the model.  This provides the model with authoritative information and reduces hallucinations【619114781588450†L224-L257】.
4. **Control the tone with prompts** – To ensure the chatbot responds appropriately, tune the prompt with examples of the desired tone and content (few‑shot prompting)【619114781588450†L348-L369】.  Use a respectful, security‑minded tone as recommended by UX best practices【750107192801164†L124-L143】.

There are many frameworks (such as LangChain) that can help orchestrate retrieval and chat generation.  Integrating them into this codebase is a recommended next step for advanced users.

### Respectful and secure interactions

When deploying chatbots in a company setting, it’s essential to prioritise respect, privacy, and security.  Always explain what data is collected and why.  Limit the model’s responses to avoid sharing sensitive or personal information.  Provide an explicit opt‑out option for users if personal data is involved.  If your chatbot handles private data (such as HR or healthcare information), consult your legal and compliance teams to ensure GDPR and other regulations are followed.


## Limitations

* The demo uses OpenAI’s API.  Without an API key, the application cannot generate responses.
* The conversation history is stored only in memory.  If the server restarts, all conversations are lost.  For production deployments, integrate persistent storage and user authentication.
* The system does not include retrieval from custom documents.  You need to implement embeddings and vector search to enable knowledge base queries.
* Ensure you remain within your company’s data usage and privacy policies when collecting conversation logs.

## Acknowledgements

This project draws on best practices from public guides on building chatbots and generative AI. 
