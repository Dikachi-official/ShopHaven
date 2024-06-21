from django.db import models
from userapp.models import User
from storeapp.models import Product

# Create your models here.
class Conversation(models.Model):
    members = models.ManyToManyField(User, related_name="conversations")
    product = models.ForeignKey(Product, related_name="conversations", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-modified_at',)


class ConversationMessage(models.Model):
    conversation = models.ForeignKey(Conversation, related_name="messages", on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name="created_messages",on_delete=models.CASCADE)