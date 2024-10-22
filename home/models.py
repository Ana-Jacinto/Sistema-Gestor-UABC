from django.db import models

# Create your models here.

class ContentType(models.Model):
    name = models.CharField(max_length=124)
    def __str__(self):
        return self.name

class Repository(models.Model):
    name = models.CharField(max_length=124)
    location = models.CharField(max_length=124)

    def __str__(self):
        return self.name

class Area(models.Model):
    name = models.CharField(max_length=124)

    def __str__(self):
        return self.name

class Author(models.Model):
    first_name = models.CharField(max_length=124)
    last_name = models.CharField(max_length=124)

class Item(models.Model):
    title = models.CharField(max_length=200)
    year = models.IntegerField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    authors = models.ManyToManyField(Author, through='AuthorItem')
    pdf = models.FileField(upload_to='pdfs/', null=True, blank=True)

class AuthorItem(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)