# -*- coding: utf-8 -*-
"""

"""
#This embedding uses text splitter and chunking
# start qdrant in docker

from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Qdrant
#from qdrant_client import QdrantClient
import qdrant_client
# Split the text into smaller chunks
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Initialize the embedding model
embedding_model = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")


# Initialize Qdrant client (assuming Qdrant is running locally)
vectordb_url = "http://localhost:6333"
qdrant = qdrant_client.QdrantClient(host='localhost', port=6333)
collection_name = "supplier_risks" 


def embed_and_store_data(collection_name, combined_text):

    # Ensure collection exists
    try:
        qdrant.get_collection(collection_name)
    except:
        qdrant.recreate_collection(
            collection_name=collection_name,
            vectors_config={"size": 384, "distance": "Cosine"}
        )


    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, chunk_overlap=100)
    chunks = splitter.split_text(combined_text)

    # Store in Qdrant
    vectorstore = Qdrant.from_texts(
        chunks, embedding_model, url = vectordb_url, collection_name=collection_name)
    print("Data has been successfully embedded and injected into Qdrant.")
    
    
 # Function to retrieve top K most relevant news articles based on PO embedding


def retrieve_similar_articles(collection_name, search_string, k=5):
     
    query_embedding = embedding_model.embed_query(search_string)
     # Perform similarity search in the Qdrant collection
    result = qdrant.search(
         collection_name = collection_name,  # Specify the collection of news articles
         query_vector=query_embedding,  # The embedding of the PO or related data
         limit=k,  # Limit to top K results
         query_filter=None,  # Optional: apply filters like date, supplier, etc.
         )

    return result   
    
    