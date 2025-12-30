import os
import glob
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

DATA_PATH = os.path.join("..", "scraper", "data")
ASSISTANT_ID = os.getenv("ASSISTANT_ID")

def run_rag_pipeline():
    """
    Automated Workflow: Upload files to OpenAI, create Vector Store, and attach to Assistant.
    """
    print("--- Starting Data Pipeline to OpenAI Vector Store ---")

    # Collect .md files generated from Scraper
    file_paths = glob.glob(os.path.join(DATA_PATH, "*.md"))
    
    if not file_paths:
        print(f"Error: No .md files found in {DATA_PATH}. Please run the scraper first.")
        return

    # Create a new Vector Store
    vector_store = client.beta.vector_stores.create(name="OptiSigns Knowledge Base")
    print(f"Created Vector Store ID: {vector_store.id}")

    # Upload files using the Batch mechanism (API-based upload)
    file_streams = [open(path, "rb") for path in file_paths]

    try:
        # Upload and wait for OpenAI processing (polling)
        file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
            vector_store_id=vector_store.id, 
            files=file_streams
        )

        # Log mandatory details as per test requirements
        print(f"Batch Status: {file_batch.status}")
        print(f"Total files processed: {len(file_paths)}")
        print(f"Embedding details (File counts): {file_batch.file_counts}")

    finally:
        for f in file_streams:
            f.close()

    # Attach the Vector Store to the Assistant created in Playground
    if ASSISTANT_ID:
        client.beta.assistants.update(
            assistant_id=ASSISTANT_ID,
            tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
        )
        print(f"Successfully updated Assistant {ASSISTANT_ID} with the new Vector Store.")
    else:
        print("Warning: ASSISTANT_ID not found in .env. Please update it manually in the Playground.")

    print("--- Pipeline completed successfully ---")

if __name__ == "__main__":
    run_rag_pipeline()