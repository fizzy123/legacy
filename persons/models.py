from django.db import models

class Person(models.Model):
    user = models.CharField(max_length=200, primary_key=True)
    upvotes = models.ManyToManyField('Comment', related_name='upvoters')
    downvotes = models.ManyToManyField('Comment', related_name='downvoters')
    
class Comment(models.Model):
    owner = models.ForeignKey(Person)
    text = models.TextField()
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    
