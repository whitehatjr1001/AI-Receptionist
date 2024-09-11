import pinecone
import os
import json

# Initialize Pinecone
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')

pc = pinecone.Pinecone(api_key=PINECONE_API_KEY)

# Create index if it doesn't exist
index_name = "emergency-index"
if index_name not in pc.list_indexes():
    pc.create_index(
        name=index_name,
        dimension=1024,
        metric="cosine",
        spec=pinecone.ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )

# Load and upsert data
with open('emergencies.json') as json_file:
    data = json.load(json_file)

index = pc.Index(index_name)

upsert_data = []
for emergency in data['emergencies']:
    emergency_text = emergency['emergency']
    next_step = emergency['next_step']
    
    embedding_response = pc.inference.embed(
        model="multilingual-e5-large",
        inputs=[emergency_text],
        parameters={"input_type": "passage"}
    )
    
    vector = embedding_response[0]['values']

    upsert_data.append({
        "id": emergency_text,
        "values": vector,
        "metadata": {"next_step": next_step}
    })

index.upsert(vectors=upsert_data)

print("Database setup complete.")
