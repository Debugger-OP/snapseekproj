# api/utils.py

import torch
from transformers import CLIPProcessor, CLIPModel
from pinecone import Pinecone
import requests

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

GOOGLE_API_KEY = "AIzaSyARx048uN7_UFyO1OWXUHi9sB5sKvG0Qkk"
GOOGLE_CX = "669231d6dcaba4e38"

def fetch_images_from_google(query, num_results=3):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": GOOGLE_API_KEY,
        "cx": GOOGLE_CX,
        "q": query,
        "searchType": "image",
        "num": num_results
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return [item['link'] for item in data.get('items', [])]
    return []