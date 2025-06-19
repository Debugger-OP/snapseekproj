from django.db import models

class Image(models.Model):
    image = models.ImageField(upload_to='snapseek/')
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    pinecone_id = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Image {self.id} - {self.description[:30]}"
