from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ImageSerializer
from .models import Image
from .utils import generate_embedding, save_to_pinecone

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
