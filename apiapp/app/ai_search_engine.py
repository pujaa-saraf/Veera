import os
import re
import time, logging, sys, numpy as np
import openai
import pickle
# from openai import OpenAI
from functools import lru_cache

from llama_index.schema import Document
from llama_index import VectorStoreIndex
from llama_index import ServiceContext
from llama_index.llms import OpenAI


# fetch_model_response(context, query)
# Define the file path where the pickled object is stored
file_path = 'retriever.pkl'


# from openai import OpenAI
OPEN_API_KEY = API_KEY
os.environ['OPENAI_API_KEY'] = OPEN_API_KEY

# Set the API key using the OpenAI class
client = OpenAI(api_key=API_KEY)

system_prompt="""You are a Q&A assistant. Your goal is to answer questions as accurately as possible based on the instructions and context provided."""
standard_output_format = f"""Provide a summarized answer for the given question under 500 words, maintain a simple, easy-to-understand language without redundancy with your answers"""

def set_prompt(context, query):
    search_prompt = f"""Use the context: {context}, to answer the question: {query} below"""
    prompt = system_prompt + search_prompt + standard_output_format
    return prompt

context = """
Bitcoin (BTC) is a cryptocurrency, a virtual currency designed to act as money and a form of payment outside the control of any one person, group, or entity, thus removing the need for third-party involvement in financial transactions. It is rewarded to blockchain miners for verifying transactions and can be purchased on several exchanges.

Bitcoin was introduced to the public in 2009 by an anonymous developer or group of developers using the name Satoshi Nakamoto.

It has since become the most well-known cryptocurrency in the world. Its popularity has inspired the development of many other cryptocurrencies.

Learn more about the cryptocurrency that started it all—the history behind it, how it works, how to get it, and what it can be used for.
"""

query = "what is a bitcoin?"

#initializing the vector query engine
documents = []
document = Document(text=context)
documents.append(document)

# gpt-4-1106-preview
# from openai import OpenAI
# client = OpenAI(api_key=API_KEY)
llm = OpenAI(model="gpt-3.5-turbo-instruct", temperature=0.1, api_key=API_KEY)
service_context = ServiceContext.from_defaults(
    llm=llm, embed_model="local:BAAI/bge-small-en-v1.5"
)

vector_index = VectorStoreIndex.from_documents(documents,
                                        service_context=service_context)
vector_query_engine = vector_index.as_query_engine()


# @lru_cache(maxsize=None)
def fetch_response(model_output):
    # Check if 'choices' attribute exists in the response object
    if hasattr(model_output, 'choices'):
        # Extract the list of choices
        choices = model_output.choices
        
        # Check if there are any choices available
        if choices:
            # Retrieve the first choice (assuming you're interested in the first completion)
            first_choice = choices[0]
            
            # Access the message attribute of the choice
            message = first_choice.message
            
            # Retrieve the content attribute from the message, which contains the completion text
            completion_text = message.content
            
            # Print or use the completion text as needed
            # print(completion_text)
            return completion_text
        else:
            print("No completion generated.")
    else:
        print("The 'choices' attribute is not found in the response object.")
    return 

from openai import OpenAI as GPT4
client_gpt4 = GPT4(api_key=OPEN_API_KEY)

@lru_cache(maxsize=None)
def fetch_model_response(context, query):
    model_output = client_gpt4.chat.completions.create(
    model="gpt-4-turbo-preview",
    messages=[
        {
        "role": "system",
        "content": "'You are a Q&A assistant. Your goal is to answer questions as accurately as possible based on the instructions and context provided.Provide a summarized answer for the given question under 500 words, maintain a simple, easy-to-understand language without redundancy with your answers'\n"
        },
        {
        "role": "user",
        "content": f"Use the context: \\n{context}\\n, to answer the question: {query} below"
        }
    ],
    temperature=1,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )

    response = fetch_response(model_output)
    return response


def load_retriever(file_path :str = 'retriever.pkl'):
    # Load the pickled object
    try:
        with open(file_path, 'rb') as f:
            retrieved_object = pickle.load(f)
        return retrieved_object
    except Exception:
        return


# gpt-4-1106-preview
# llm = OpenAI(model="gpt-3.5-turbo-instruct", temperature=0.1, api_key=API_KEY)
# service_context = ServiceContext.from_defaults(
#     llm=llm, embed_model="local:BAAI/bge-small-en-v1.5"
# )

def refine_vector_query_engine(context):

    # for context in parsed_documents:
    #     try:
    #         document = Document(text=context)
    #         documents.append(document)
    #     except Exception:
    #         logging.error(f"{context=}")
    #         logging.exception("error traceback as follows...")
    
    #tocheck if we can update index with only new documents.
    print(f"{len(documents)=}, before adding context")
    try:
        document = Document(text=context)
        documents.append(document)
    except Exception:
        print(f"error for {context=}")
        logging.exception("error traceback as follows...")
    
    vector_index = VectorStoreIndex.from_documents(documents,
                                        service_context=service_context)
    vector_query_engine = vector_index.as_query_engine()
    
    print(f"vector index refined...")
    return vector_query_engine, vector_index, documents



def set_documents_from_each_context(context: list):
    # Assuming 'context' is your string
    flattened_list = re.split('[,;\\n]', context)

    flattened_list = [s for s in flattened_list if s!='']
    documents = [Document(text=f) for f in flattened_list]
    return documents


# def query_retriever(query: str):
#     response = query+" (Answer this only if you have relevant context, if there is no context return 'False')"
#     logging.debug(f"{query=}, {response=}")
#     return response


def update_retriever(vector_query_engine):
    # Pickle dump the object
    try:
        with open('retriever.pkl', 'wb') as f:
            pickle.dump(vector_query_engine, f)
            logging.info(f"updated vector_query_engine to retriever.pkl")
        return True
    except Exception:
        logging.error(f"vector_query_engine to retriever.pkl")
        return False

import re

def extract_first_500_words(context: str) -> str:
    # Define a regular expression pattern to match words
    word_pattern = re.compile(r'\b\w+\b')
    
    # Find all words in the context
    words = re.findall(word_pattern, context)
    
    # Join the first 500 words together
    first_500_words = ' '.join(words[:500])
    
    
    return str(first_500_words)

# Example usage:

# shorter_context = extract_first_500_words(parsed_documents[0]['full_document'])
# shorter_context = shorter_context.strip()

def fetch_answer(search_query: str, full_context: str):
    answer = "This is a dummy placeholder text"
    answer_count = 0
    # context = full_context.split()
    context = extract_first_500_words(full_context)
    print(f"after trimming, {context=}, {len(context)=}")
    
    if len(context) < 10:
        return "False"
    # for context in parsed_documents:
    print(f"searching with context: {type(context)=}")
    vector_query_engine, vector_index, documents = refine_vector_query_engine(context)
    print(f"{len(documents)=}, after context update")
    update_retriever(vector_query_engine)
    print(f"update_retriever...")
    print(f"querying search engine - {search_query=}")
    answer = vector_query_engine.query(search_query+" (Answer this only if you have relevant context, if there is no context return 'False')")
    # answer = query_retriever(search_query)
    print(f"{search_query=}, with current updated context, {answer=}")
    return str(answer)

# @lru_cache(maxsize=None)
def process_query(search_query, parsed_documents):
    answer = "This is a dummy placeholder text"
    answers_with_sources = []
    answer_count = 0
    print("test...")
    print(f"{len(parsed_documents)=}, {type(parsed_documents)=}")
    for doc in parsed_documents:
        print(f"{doc=}")
        for key in ['highlighted_paragraph', 'full_document']: # , 'full_document', 'highlighted_text', 
            print(f"{doc.keys()=}, {doc.get(key)=}")
            if doc.get(key):
                print(f"fetch answer using {search_query=}, {key=}\n{doc[key]=}")
                answer = fetch_answer(search_query, doc[key])
            if answer != "False":
                answer_count += 1
            if answer_count == 2:
                break
    return answer