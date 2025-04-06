from dotenv import load_dotenv
load_dotenv()

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from typing import Any, Dict, List
from langchain import hub
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

# from consts import INDEX_NAME

# gemini-2.0-flash-exp
def run_llm(query: str, chat_history: List[Dict[str, Any]] = []):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    # Use FAISS for local storage (similar to Pinecone)
    # docsearch = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    docsearch = FAISS.load_local(r"D:\University_Bot\University_Bot_faiss\faiss_index\index.faiss", embeddings, allow_dangerous_deserialization=True)
    chat = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", temperature=0)

    rephrase_prompt = hub.pull("langchain-ai/chat-langchain-rephrase")

    retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
    stuff_documents_chain = create_stuff_documents_chain(chat, retrieval_qa_chat_prompt)

    history_aware_retriever = create_history_aware_retriever(
        llm=chat, retriever=docsearch.as_retriever(), prompt=rephrase_prompt
    )
    qa = create_retrieval_chain(
        retriever=history_aware_retriever, combine_docs_chain=stuff_documents_chain
    )

    
    result = qa.invoke(input={"input": query, "chat_history": chat_history})

    new_result = {
        "query": result['input'],
        "result": result['answer'],
        "source_documents": result['context'],
    }
    # print(new_result,'--------new_result RUN_LLM--------')
    return new_result



# print(run_llm("what is the university of chicago?"))

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


# def run_llm2(query: str, chat_history: List[Dict[str, Any]] = []):
#     embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
#     docsearch = FAISS.load_local("faiss_index", embeddings)
#     chat = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0)

#     rephrase_prompt = hub.pull("langchain-ai/chat-langchain-rephrase")

#     retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")

#     rag_chain = (
#         {
#             "context": docsearch.as_retriever() | format_docs,
#             "input": RunnablePassthrough(),
#         }
#         | retrieval_qa_chat_prompt
#         | chat
#         | StrOutputParser()
#     )

#     retrieve_docs_chain = (lambda x: x["input"]) | docsearch.as_retriever()

#     chain = RunnablePassthrough.assign(context=retrieve_docs_chain).assign(
#         answer=rag_chain
#     )

#     result = chain.invoke({"input": query, "chat_history": chat_history})
#     return result
