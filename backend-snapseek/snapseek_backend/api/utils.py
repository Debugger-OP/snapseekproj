# api/utils.py

import torch
from transformers import CLIPProcessor, CLIPModel
from pinecone import Pinecone

# Initialize HuggingFace CLIP model
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# Initialize Pinecone (new style)
pc = Pinecone(api_key="pcsk_4dq4hH_MM1L4WzbhMUis1XgtNUvFH9bMnwK2nka5wMV7vF4wfh4ARBucGW6YDb74BqQ9Ct")
index = pc.Index("snapseek-images")


def generate_embedding(text):
    inputs = processor(text=[text], return_tensors="pt", padding=True)
    with torch.no_grad():
        outputs = model.get_text_features(**inputs)
    vector = outputs[0].tolist()
    return vector


def save_to_pinecone(image_id, vector):
    pinecone_id = f"img-{image_id}"
    index.upsert(vectors=[
        {
            "id": pinecone_id,
            "values": vector,
        }
    ])
    return pinecone_id
