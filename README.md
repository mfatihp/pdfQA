# pdfQA
Q&A system for PDF files using lightweight local LLMs, vector search, and an Angular frontend. Includes full pipeline from document ingestion to answer generation, with FastAPI and Docker support.

## 🚀 Features

- 💬 **LLM-Powered Chat:** Interact with a large language model for instant Q&A and conversation.
- 📄 **PDF Upload & Preview:** Upload PDF files and preview them directly in the browser.
- 🔍 **PDF Querying:** Ask questions about the uploaded PDF and receive contextual answers.
- 🎯 **Clean UI:** Minimal and responsive interface for easy interaction.


## 📸 Screenshots

<table>
<tr>
<td><img src="docs/pdfQA_1.png" width="1000"></td>
</tr>
<tr>
<td><img src="docs/pdfQA_2.png" width="1000"></td>
</tr>
</table>

## 🛠️ Installation

1. Clone the repository:
    ```Bash
    git clone https://github.com/mfatihp/pdfQA.git
    ```
2. Navigate to the project backend directory:
    ```bash
    cd pdfQA/backend/
    ```
3. Create your own `.env` file and put inside Huggingface token as `HF_TOKEN="**********"`.

<p align="center">
<img src="docs/pdfQA_env.png" width="250">
</p>

4. Navigate back to the project directory:
    ```bash
    cd ..
    ```

5. Build docker container (Need nvidia packages(!Details will be given - work in progress)):
    ```bash
    sudo docker compose up --build
    ```

## 📈 How To Use

## 🛠️ Built With

