from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Value(models.Model):
    name = models.CharField(max_length = 100)
    experiences = models.ManyToManyField('Experience', blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['name']
        
    def __str__(self):
        return(self.name)

class Skill(models.Model):
    name = models.CharField(max_length = 100)
    experiences = models.ManyToManyField('Experience', blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['name']
        
    def __str__(self):
        return(self.name)
        
class Experience(models.Model):
    name = models.CharField(max_length = 100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['name']
        
    def __str__(self):
        return(self.name)