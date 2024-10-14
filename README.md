# RAG_chatbot using Langchain

This project is a Retrieval-Augmented Generation (RAG) chatbot that allows users to upload PDF files, instantly receive a summary, and interact with the document by asking questions. The application leverages LangChain for natural language processing, stores documents in a ChromaDB vector database, and has a frontend built with Streamlit.

## Feature-
PDF Upload: Users can upload any PDF file for analysis.
Summary Generation: As soon as a PDF is uploaded, the app generates a summary using the MapReduce method.
Interactive Q&A: Users can ask questions related to the uploaded PDF and receive answers based on the document content.
Document Storage: PDFs are stored in a ChromaDB vector database for efficient retrieval and processing.
Streamlit Frontend: The user interface is built with Streamlit, offering a simple and interactive experience.

## Technologies Used-
1. LangChain: For building the language model and handling document processing.
2. Groq API: To connect with LangChain's language model via an API.
3. ChromaDB: A vector database for storing and retrieving PDF documents.
4. Streamlit: A Python framework for building the web application frontend.

## Getting Started-
### Prerequisites
1. Python 3.7 or higher
2. A LangChain API key
3. ChromaDB set up
4. Streamlit installed

### Installation
1. Clone this repository
```bash
git clone <repository name>
```
2. install the required python packages
```bash
pip install -r requirements.txt
```
3. Setup GroqAPI credentials in .env file
4. Run the streamlit app
```bash
streamlit run main.py 
```
### Usage
1. Open the Streamlit app in your web browser.
2. Upload a PDF document.
3. Wait for the summary to be generated.
4. Begin asking questions related to the PDF content.

### Project Structure
main.py: The main application file containing the Streamlit interface.
chain.py: Contains the code for summarizing the PDF using MapReduce.
database.py: Handles the connection to ChromaDB for storing and retrieving PDF vectors.
requirements.txt: Lists all the dependencies for the project.
.env: contains the GroqAPI key

## Contributing
Contributions are welcome! Please open an issue or submit a pull request if you have suggestions for improving the project.
This project is still in its developmental stages.

## License
This project is licensed under the Apache License 2.0. See the LICENSE file for details.









