from django.db import models

# Create your models here.
class Expense(models.Model):
    
    def __str__(self):
        return self.name
    name=models.CharField(max_length=100)
    amount=models.IntegerField()
    category=models.CharField(max_length=400)
    date=models.DateTimeField(auto_now=True)
    