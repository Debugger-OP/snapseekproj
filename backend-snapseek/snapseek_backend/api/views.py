from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ImageSerializer
from .models import Image
from .utils import generate_embedding, save_to_pinecone
from pinecone import Pinecone
from .utils import fetch_images_from_google
from decouple import config

class ImageUploadView(APIView):
    def post(self, request):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            image_instance = serializer.save()

            # Generate embedding (CLIP or AI model)
            vector = generate_embedding(image_instance.description)

            # Save to Pinecone
            pinecone_id = save_to_pinecone(image_instance.id, vector)

            # Save pinecone_id in model
            image_instance.pinecone_id = pinecone_id
            image_instance.save()

            return Response(ImageSerializer(image_instance).data, status=201)
        return Response(serializer.errors, status=400)


class ImageSearchView(APIView):
    def post(self, request):
        query = request.data.get("query")
        if not query:
            return Response({"error": "Query not provided"}, status=400)

        # Step 1: Get vector for the query
        query_vector = generate_embedding(query)

        # Step 2: Search Pinecone
        pc = Pinecone(api_key=config("PINECONE_API_KEY"))
        index = pc.Index("snapseek-images")
        results = index.query(
         vector=query_vector,
            top_k=5,
            include_values=False,
            include_metadata=False
)

# Set a threshold — typical cosine similarity ranges from 0.0 to 1.0
        MIN_SCORE = 0.80

# Filter out low-confidence results
        filtered_ids = [
        match['id']
        for match in results['matches']
        if match['score'] >= MIN_SCORE
]

        images = Image.objects.filter(pinecone_id__in=filtered_ids)

        if images.exists():
            return Response(ImageSerializer(images, many=True).data)

        # 🔁 Google fallback if no Pinecone matches
        fallback_images = fetch_images_from_google(query)

        return Response({
            "fallback": True,
            "images": fallback_images
        }, status=200)