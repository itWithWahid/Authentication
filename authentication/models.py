from django.db import models

class User(models.Model):
    
    membership_number = models.CharField(max_length=255)
    name = models.CharField(max_length=255)  
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    image_path = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
