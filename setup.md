Set Up Virtual Environment (optional but recommended): This keeps your project dependencies isolated.

Navigate to your project folder (or create one):
mkdir ProductOpsRAG
cd ProductOpsRAG

Create a virtual environment:
python3 -m venv venv


Activate the virtual environment:
source venv/bin/activate

Install Required Packages: While the virtual environment is active, install the necessary Python packages:
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib


Google Drive API: https://console.cloud.google.com/apis/api/drive.googleapis.com/metrics?project=arhm-dev&inv=1&invt=AbwLFg

Google Docs API: https://console.cloud.google.com/apis/api/docs.googleapis.com/metrics?project=arhm-dev&inv=1&invt=AbwLFg

Install Dependencies: pip install -r requirements.txt


pip install chromadb sentence-transformers






