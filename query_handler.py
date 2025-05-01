
from langchain.chains import RetrievalQA

def run_query(qa_chain, query):
    """
    This function takes the qa_chain and a query,
    then runs the query through the chain and returns the result.
    """
    return qa_chain.run(query)
