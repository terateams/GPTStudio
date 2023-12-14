import os
from typing import List

import chromadb
from llama_index import ServiceContext, VectorStoreIndex, SimpleDirectoryReader, Document
from llama_index.embeddings import OpenAIEmbedding
from llama_index.storage.storage_context import StorageContext
from llama_index.vector_stores import ChromaVectorStore
from llama_index.text_splitter import SentenceSplitter
from libs import get_data_dir


def get_llama_memary_index(texts: List[str]):
    documents = [Document(text=text) for text in texts]
    # define a text splitter and embedding model
    text_splitter = SentenceSplitter(chunk_size=1024, chunk_overlap=10)
    embed_model = OpenAIEmbedding(embed_batch_size=42)
    # define a service context
    service_context = ServiceContext.from_defaults(
        embed_model=embed_model,
        text_splitter=text_splitter
    )
    storecontext = StorageContext.from_defaults()
    # load your index from stored vectors
    return VectorStoreIndex.from_documents(
        documents,
        service_context=service_context,
        storage_context=storecontext,
        show_progress=True
    )


def get_llama_store_index(dbname, collection):
    """
    Constructs a VectorStoreIndex from a given database and collection.

    Args:
        dbname (str): The name of the database.
        collection (str): The name of the collection.

    Returns:
        VectorStoreIndex: The constructed VectorStoreIndex object.
    """
    # get a vector store
    db = chromadb.PersistentClient(path=os.path.join(get_data_dir(), dbname))
    # get or create a collection
    chroma_collection = db.get_or_create_collection(collection)
    # define a vector store
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    # define a storage context
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    # define a text splitter and embedding model
    text_splitter = SentenceSplitter(chunk_size=1024, chunk_overlap=10)
    embed_model = OpenAIEmbedding(embed_batch_size=42)
    # define a service context
    service_context = ServiceContext.from_defaults(
        embed_model=embed_model,
        text_splitter=text_splitter
    )
    # load your index from stored vectors
    return VectorStoreIndex.from_vector_store(
        vector_store,
        service_context=service_context,
        storage_context=storage_context,
    )


def create_document_index(srcdir, dbname, collection):
    """
    Create a document index using the given source directory, database name, and collection name.

    Parameters:
        srcdir (str): The source directory containing the documents.
        dbname (str): The name of the database to store the index.
        collection (str): The name of the collection to store the index.

    Returns:
        None

    """
    # load your documents from a directory
    documents = SimpleDirectoryReader(srcdir).load_data()
    # get an index
    vindex = get_llama_store_index(dbname, collection)
    # define a text splitter
    text_splitter = SentenceSplitter(chunk_size=1024, chunk_overlap=10)
    # process nodes from documents
    nodes = text_splitter.get_nodes_from_documents(documents, show_progress=True)
    # insert nodes into index
    vindex.insert_nodes(nodes, show_progress=True)


def create_document_index_by_texts(texts: List, dbname, collection):
    """
    Create a document index using the given text list, database name, and collection name.

    Parameters:
        texts (List[str]): The source directory containing the documents.
        dbname (str): The name of the database to store the index.
        collection (str): The name of the collection to store the index.

    Returns:
        None

    """
    # load your documents from a directory
    documents = [ Document(text=t) for t in texts]
    # get an index
    vindex = get_llama_store_index(dbname, collection)
    # define a text splitter
    text_splitter = SentenceSplitter(chunk_size=1024, chunk_overlap=10)
    # process nodes from documents
    nodes = text_splitter.get_nodes_from_documents(documents, show_progress=True)
    # insert nodes into index
    vindex.insert_nodes(nodes, show_progress=True)


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.abspath(".."), ".env"))
    create_document_index(
        os.path.join(os.path.abspath("."), "assets/test"),
        "radiusrfc.chroma.db",
        "radiusrfc"
    )
    index = get_llama_store_index("radiusrfc.chroma.db", "radiusrfc")
    query = index.as_query_engine()
    resp = query.query("Radius")
    print(resp)
