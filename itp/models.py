from django.db import models
from django.contrib.auth.models import User
from django.core import files
from django.utils.safestring import mark_safe
from PIL import Image

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    picture = models.ImageField(upload_to = 'profile_images', blank=True)
    title = models.CharField(max_length=10, blank = True)
    usertype = models.CharField(max_length=50, blank = True)
    occupation = models.CharField(max_length=50, blank = True)
    institution = models.CharField(max_length=100, blank = True)
    department = models.CharField(max_length=100, blank = True)
    research_field = models.CharField(max_length=100, blank = True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        SIZE = 50, 50
        
        if self.picture:
            pic = Image.open(self.picture.path)
            pic.thumbnail(SIZE, Image.LANCZOS)
            pic.save(self.picture.path)

    def __str__(self):
        return self.user.username

class Conference(models.Model):
    name = models.CharField(max_length=300, blank = True, unique=True)
    time = models.DateField()
    location = models.CharField(max_length=300, blank = True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=300, blank = True, unique=True)

    def __str__(self):
        return self.name

class Publication(models.Model):
    PTYPES = [
        ('Journal', 'Journal'),
        ('Conference', 'Conference'),
        ('Technical Reports', 'Technical Reports'),
    ]

    title = models.CharField(max_length=300, blank = True, unique=True)
    author = models.ManyToManyField(User, help_text='Use cmd to select multiple authors')
    type = models.CharField(max_length=300, blank = True, choices=PTYPES)
    year = models.IntegerField()
    magazine = models.CharField(max_length=300, blank = True)
    page = models.CharField(max_length=300, blank = True)
    doi = models.CharField(max_length=300, blank = True)
    conferenceid = models.ForeignKey(Conference, on_delete=models.CASCADE, blank = True, null=True, help_text=mark_safe("<button><a href='add_conference/'>Add A Conference</a></button>"))
    tag = models.ManyToManyField(Tag, blank=True, help_text=mark_safe("<button><a href='add_tag/'>Add A Tag</a></button>"))

    def all_authorself(self):
        return ",".join([str(p) for p in self.user.all()])

    def __str__(self):
        return self.title


#class Publication_Author(models.Model):
#    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
#    author = models.ForeignKey(User, on_delete=models.CASCADE)

#    class Meta:
#        unique_together = ('publication', 'author',)

#    def __str__(self):
#        return self.publication.title


class Event(models.Model):
    name = models.CharField(max_length=300, blank = True, unique=True)
    time = models.DateField()
    location = models.CharField(max_length=300, blank = True)
    type = models.CharField(max_length=300, blank = True)
    participant = models.CharField(max_length=300, blank = True)
    description = models.TextField(max_length=3000, blank = True)

    def __str__(self):
        return self.name
