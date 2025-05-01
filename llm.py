import openai
import streamlit as st


openai.api_key ="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"
import chromadb

# Set your OpenAI API key

# Initialize the Chroma client
client = chromadb.PersistentClient(path="/Users/auritabytyqi/Desktop/91Life/ProductOpsRAG")

# Function to query OpenAI's GPT-3 model directly
def query_openai_gpt(query, context):
    # Constructing the full prompt by including the context from ChromaDB
    prompt = f"Context:\n{context}\n\nQuestion: {query}"
    # Query OpenAI GPT model with context
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # You can use gpt-3.5 or gpt-4 as needed
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        # max_tokens=100000000  # Adjust max tokens as needed
    )
    # Adjust max tokens as needed)
    return response['choices'][0]['message']['content'].strip()

# Function to query ChromaDB
def query_chromadb(query_text, n_results=20):
      # You can modify this to match your ChromaDB setup
    collection = client.get_or_create_collection("google_docs")  # Adjust collection name
    results = collection.query(query_texts=[query_text], n_results=n_results)

    # Print the raw structure of results for debugging
    print("ChromaDB Query Results:", results)

    # Assuming that each result in 'documents' is a list containing multiple pieces of information
    # If results['documents'] is a list of lists, flatten it
    context = "\n".join([str(item) for result in results['documents'] for item in result])  # Flatten if it's a list of lists
    return context

# Example query
st.title("Product Operations Automation")

# User input fields
query_text = st.text_input("Enter your query:")

# Button to query OpenAI
if st.button("Get Answer"):
    if query_text:
        with st.spinner('Querying...'):
            # Get response from OpenAI
            response = query_openai_gpt(query_text, query_chromadb(query_text))
            # Display the result
            st.subheader("Response:")
            st.write(response)
    else:
        st.warning("Please enter both query and context.")
