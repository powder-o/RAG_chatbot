import os
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain.chains.summarize import load_summarize_chain

from dotenv import load_dotenv

load_dotenv()
secret_key = os.getenv('GROQ_API_TOKEN')

class Chain:
    def __init__(self):
        self.llm = ChatGroq(temperature=0, groq_api_key=secret_key, model_name="llama3-70b-8192")

    def Summarize_chain(self, article_chunks):
        chain = load_summarize_chain(
            llm=self.llm,
            chain_type="map_reduce"
            # chain_type="stuff"
        )
        article_summary = chain.run(article_chunks)
        return article_summary

    def response(self, question, retriever_results):
        context = "\n\n".join([doc for doc in retriever_results])
        prompt = PromptTemplate.from_template(
            """
            ### INSTRUCTION:
            Answer the Following question. You may refer the context below to answer more accurately. 
            If the context does not provide a direct answer, rely on your own knowledge. Do not speculate or make up information. 
            
            ### CONTEXT:
            {context}

            ### QUESTION:
            {question}

            ### ANSWER (NO PREAMBLE):
            """
        )
        llm_chain = prompt | self.llm | StrOutputParser()
        # res = chain_extract.invoke(input={"page_data": cleaned_text})
        # rag_chain = {"context": context, "question": RunnablePassthrough()} | llm_chain
        rag_chain = {
            "context": RunnablePassthrough(), 
            "question": RunnablePassthrough()
        } | llm_chain
        # res = rag_chain.invoke(question)
        res = rag_chain.invoke({"context": context, "question": question})

        return res

    
