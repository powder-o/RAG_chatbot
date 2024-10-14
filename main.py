import streamlit as st
from chain import Chain
from database import VectorStore
import warnings
from langchain._api import LangChainDeprecationWarning
warnings.simplefilter("ignore", category=LangChainDeprecationWarning)
import os
import concurrent.futures

# Function to process the PDF summary in parallel
def process_pdf_summary(file_path):
    try:
        vector_store = VectorStore(file_path)
        pages = vector_store.load_pdf()
        summary = chain.Summarize_chain(pages)
        st.session_state.vector_store = vector_store  # Store vector store after loading
        return summary
    except Exception as e:
        return f"An error occurred while processing the PDF: {e}"

def create_streamlit_app():
    st.title("Basic RAG Application")

    # Initialize session state variables if not already present
    if 'vector_store' not in st.session_state:
        st.session_state.vector_store = None
    if 'summary_future' not in st.session_state:
        st.session_state.summary_future = None
    if 'summary' not in st.session_state:
        st.session_state.summary = None
    if 'pdf_file_path' not in st.session_state:
        st.session_state.pdf_file_path = None

    # File uploader for both .pdf and .txt files
    uploaded_file = st.file_uploader("Upload a file (PDF or TXT)", type=["pdf", "txt"])

    if uploaded_file is not None:
        file_name = uploaded_file.name
        file_extension = file_name.split(".")[-1].lower()  # Get the file extension

        if file_extension == "pdf":
            st.write(f"Uploaded file is a PDF: {file_name}")
            directory = "C:/Users/Lenovo/Gen_AI/sec_insights/self2/files/"

            try:
                # Save the uploaded PDF file temporarily
                file_path = os.path.join(directory, f"temp_{file_name}")
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                # Store the file path in session state for later use
                st.session_state.pdf_file_path = file_path

                # Start processing the PDF summary asynchronously
                if st.session_state.summary_future is None:
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        st.session_state.summary_future = executor.submit(process_pdf_summary, file_path)
                    st.write("Processing summary in the background...")

            except Exception as e:
                st.error(f"An error occurred while saving or processing the PDF: {e}")

        elif file_extension == "txt":
            st.write(f"Uploaded file is a TXT: {file_name}")
            # Add TXT processing logic if needed

        else:
            st.error("Unsupported file format. Please upload either a PDF or TXT file.")

    # Check if the summary processing is done
    if st.session_state.summary_future and st.session_state.summary_future.done():
        st.session_state.summary = st.session_state.summary_future.result()
        st.write("Summary completed!")
        st.write(st.session_state.summary)

    # Real-time question input while PDF summary is processing
    st.write("You can ask questions while the summary is being processed.")
    question = st.text_input("Enter your question:")
    submit_button = st.button("Submit")

    if submit_button:
        try:
            # Check if the vector store exists or PDF file path is available
            if st.session_state.vector_store is None and st.session_state.pdf_file_path is not None:
                st.session_state.vector_store = VectorStore(st.session_state.pdf_file_path)
            
            if st.session_state.vector_store is None:
                st.error("Please upload and process a file first!")
            else:
                # Retrieve and respond to the question using the vector store
                retriever_results = st.session_state.vector_store.retriever(question)
                res = chain.response(question, retriever_results)
                st.write(res)

        except Exception as e:
            st.error(f"An error occurred while retrieving the answer: {e}")

    # Option to delete the uploaded PDF file
    delete_pdf = st.button("Delete")
    if delete_pdf and uploaded_file is not None:
        try:
            os.remove(st.session_state.pdf_file_path)
            st.success("PDF file deleted successfully!")
            st.session_state.pdf_file_path = None
            st.session_state.vector_store = None  # Reset the vector store after deletion
        except Exception as e:
            st.error(f"An error occurred while deleting the file: {e}")

if __name__ == "__main__":
    chain = Chain()  # Ensure the chain object is initialized correctly
    st.set_page_config(layout="wide", page_title="Basic RAG")
    create_streamlit_app()
