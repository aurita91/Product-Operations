from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import chromadb
from googleapiclient.errors import HttpError

# OAuth2 Scopes for accessing Google Docs and Drive
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly', 'https://www.googleapis.com/auth/documents.readonly']

# Authenticate and create service
def authenticate():
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)  # Triggers OAuth flow
    
    drive_service = build('drive', 'v3', credentials=creds)
    docs_service = build('docs', 'v1', credentials=creds)
    return drive_service, docs_service

# Retrieve all files and their parent folder information
def get_all_files_and_folders(drive_service):
    files = []
    page_token = None

    while True:
        results = drive_service.files().list(
            pageSize=100,  
            fields="nextPageToken, files(id, name, parents)",
            pageToken=page_token
        ).execute()

        files.extend(results.get('files', []))
        page_token = results.get('nextPageToken', None)

        if not page_token:
            break  # No more pages, stop the loop

    return files

# Extract text from Google Docs file
def extract_text_from_doc(docs_service, doc_id):
    doc = docs_service.documents().get(documentId=doc_id).execute()
    text = []
    for element in doc.get('body', {}).get('content', []):
        if 'paragraph' in element:
            for run in element['paragraph'].get('elements', []):
                part = run.get('textRun', {}).get('content')
                if part:
                    text.append(part)
    return ''.join(text)

# Store documents in ChromaDB
def store_in_chromadb(docs_content):
    client = chromadb.PersistentClient(path="/Users/auritabytyqi/Desktop/91Life/ProductOpsRAG")
    collection = client.create_collection(name="google_docs")

    for doc_name, doc_text in docs_content.items():
        collection.add(
            documents=[doc_text],  # Text of the document
            metadatas=[{"name": doc_name}],  # Metadata (for example, file name)
            ids=[doc_name]  # Use the document name as the ID
        )

# Query ChromaDB for a document by name
def query_chromadb(query_text):
    client = chromadb.PersistentClient(path="/Users/auritabytyqi/Desktop/91Life/ProductOpsRAG")
    collection = client.get_collection(name="google_docs")

    query_results = collection.query(
        query_texts=[query_text],  # The query text (e.g., "LRH Discovery")
        n_results=1  # Limit to 1 result
    )

    return query_results['documents'][0] if query_results['documents'] else None

# Main execution
if __name__ == '__main__':
    drive_service, docs_service = authenticate()
    
    # Get all files and their parent folder IDs
    files = get_all_files_and_folders(drive_service)
    
    # Store documents in ChromaDB
    docs_content = {}
    for file in files:
        file_name = file['name']
        file_id = file['id']
        parents = file.get('parents', [])
        
        if parents:
            try:
                doc_text = extract_text_from_doc(docs_service, file_id)
                docs_content[file_name] = doc_text
            except HttpError:
                continue  # Skip if there's an error extracting text from a doc

    if docs_content:
        store_in_chromadb(docs_content)
    
    # Query the vector database for a specific document (e.g., "LRH Discovery")
    document = query_chromadb("LRH Discovery")  # Change query text as needed
    
    # If document is found, return its content
    if document:
        print(document)
