import chromadb

# Initialize ChromaDB client
client = chromadb.PersistentClient(path="/Users/auritabytyqi/Desktop/91Life/ProductOpsRAG")

# Get the collection where documents are stored (assuming you've already created it)
collection = client.get_collection(name="google_docs")

# Perform a query to retrieve relevant documents (e.g., search for 'LRH Discovery')

results = collection.query(query_texts=["How does BardyDx work?"], n_results=4)
# print(results)

for result in results["metadatas"][0]:
    print("Matched file:", result["name"])
 # This will print out the documents that match the query
