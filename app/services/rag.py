import os
import asyncio
from dotenv import load_dotenv
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from app.services.openai import openai_bot 

load_dotenv()

# Get API key and index name from environment variables
pinecone_api_key = os.getenv("PINECONE_API_KEY")
index_name = os.getenv("PINECONE_INDEX")
# TelepracticePro_ID = os.getenv("TELEPRACTICEPRO_ID")

# Ensure API key is set
if not pinecone_api_key:
    raise ValueError("PINECONE_API_KEY is not set in environment variables.")

# Initialize Pinecone client
pc = Pinecone(api_key=pinecone_api_key)

# Ensure the index exists before using it
if index_name not in [idx.name for idx in pc.list_indexes()]:
    raise ValueError(f"Pinecone index '{index_name}' does not exist. Create it first.")

# Connect to the Pinecone index
index = pc.Index(index_name)

# Use OpenAI for async embedding
vector_store = PineconeVectorStore(index, OpenAIEmbeddings(), text_key="text")

# -----------------------------------------------------------------------------------
async def retrieve_relevant_docs(
        user_query: str, 
        organization_id: str
    ):

    """Asynchronously fetch relevant documents from both the organization and global knowledge base."""
    try:
        # Generate query embedding
        query_embedding = await OpenAIEmbeddings().aembed_query(user_query)

        # Perform organization-specific search
        query_results_org = index.query(vector=query_embedding, top_k=2, namespace=organization_id, include_metadata=True)

        # Perform global search from telepractice-pro resources
        query_results_global = index.query(vector=query_embedding, top_k=2, namespace="global", include_metadata=True)
        
        # Combine results
        combined_results = query_results_org.get("matches", []) + query_results_global.get("matches", [])

        # Extract relevant document contents
        relevant_docs = [match["metadata"]["text"] for match in combined_results if "metadata" in match and "text" in match["metadata"]]

        return relevant_docs

    except Exception as e:
        print(f"Error retrieving documents: {e}")
        return []

async def generate_response(user_query: str, organization_id: str, user_id: str, assistant_session_id: str):
    """
    Asynchronously retrieves relevant docs and generates a chatbot response using OpenAI.
    Logs interaction with user/session metadata.
    """
    relevant_docs = await retrieve_relevant_docs(user_query, organization_id)

    if not relevant_docs:
        return "No relevant information found for this organization."

    # Instruction for response generation
    instruction = (
        "Your name is ."
        "You are a helpful assistant for  a telehealth platform for behavioural health services. "
        "You can answer questions about the platform and its services. "
        "If the user's question is about a specific organization, answer based on their documents. "
        "If it's about telehealth, answer based on the platform's knowledge base. "
        "If both, combine relevant details. "
        "Ensure you keep your answers clear and concise."
        "Do not answer any question outside of the scope of the platform."
    )

    # Combine context
    context = f"{instruction}\n\nRelevant Documents:\n" + "\n".join(relevant_docs)

    # Generate assistant reply
    response = await openai_bot(context, user_query)

    # Optional: log interaction
    # await log_assistant_interaction(
    #     user_id=user_id,
    #     session_id=assistant_session_id,
    #     organization_id=organization_id,
    #     query=user_query,
    #     response=response
    # )

    return response
