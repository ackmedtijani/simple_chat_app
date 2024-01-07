from django.db import models
import uuid

# Create your models here.

from account.models import User

class Room(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length = 255 , blank = True , null = True)
    participitants = models.ManyToManyField(User)
    date_created = models.DateTimeField(auto_now_add = True)

class Message(models.Model):
    body = models.TextField()
    room = models.ForeignKey(Room , related_name = "room_messages",
                                null=True , blank = True, 
                                on_delete = models.SET_NULL)
    sent_by = models.ForeignKey(User , related_name = "sent_by",
                                null=True , blank = True, 
                                on_delete = models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add = True)
    created_by = models.ForeignKey(User , related_name = "created_at",
                                null=True , blank = True, 
                                on_delete = models.SET_NULL)
    delivered = models.BooleanField(default = False)
    seen = models.BooleanField(default = False)
    
    class Meta:
        ordering = ("created_at",)

    def __str__(self) -> str:
        return f"Message sent by: {self.sent_by}"
    


    
      