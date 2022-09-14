from django import forms
from django.contrib.auth.models import User
from itp.models import Conference, Publication, Tag, UserProfile, Event
import os
from django.core.exceptions import ValidationError
from django.forms import FileField, Form


class UserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email =  forms.EmailField
    password = forms.CharField(widget=forms.PasswordInput())


    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password',)
        

class UserProfileForm(forms.ModelForm):
    title = forms.CharField(widget=forms.Select(choices= [
    (' ', '---'),
    ('dr', 'Dr.'),
    ('mr', 'Mr.'),
    ('ms', 'Ms.'),
    ('mrs', 'Mrs.'),
    ('miss', 'Miss.'),
    ]))
    usertype = forms.CharField(widget=forms.Select(choices= [
    (' ', '---------'),
    ('academic', 'Academic Staff'),
    ('associate', 'Associate Academic Staff'),
    ('researchers', 'Researchers / PhD Students'),
    ('external', 'Interns / Alumni / External Collaborators'),
    ]))

    class Meta:
        model = UserProfile
        fields = ('title', 'usertype', 'occupation', 'institution', 'department', 'research_field', 'picture',)


class PublicationForm(forms.ModelForm):
    class Meta:
        model = Publication
        fields = ('title', 'author', 'type', 'year', 'magazine', 'page','doi', 'conferenceid', 'tag' )

class EventForm (forms.ModelForm):
    time = forms.DateField()

    class Meta:
        model = Event
        fields = ('name', 'time', 'location', 'type', 'participant', 'description', )

class ConferenceForm(forms.ModelForm):
    class Meta:
        model = Conference
        fields = ('name', 'time', 'location',)

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ('name',)

class DataForm(Form):
    file = FileField()
    def clean_file(self) -> str:
        """upload file."""
        data = self.cleaned_data["file"]
        extension = os.path.splitext(data.name)[1]
        valid_extensions:list[str] = [".xlsx", ".csv"]
        if extension not in valid_extensions:
            raise ValidationError("File type not supported")
        return data