from django import forms
from .models import Thread, Comment

class ThreadForm(forms.Form):
    newthread = forms.CharField(label='New thread', max_length=100)

class CommentForm(forms.Form):
    newcomment = forms.CharField(label='Your comment', max_length=300)

# build form from models
# "If you're building a database-driven app, chances are you'll have forms that map closely to Django models. For instance, you might have a BlogComment model, and you want to create a form that lets people submit comments. In this case, it would be redundant to define the field types in your form, because you've already defined the fields in your model. For this reason, Django provides a helper class that lets you create a Form class from a Django model." ---https://docs.djangoproject.com/en/1.8/topics/forms/modelforms/

class ThreadModelForm(forms.ModelForm):
    class Meta:
        model = Thread 
        fields = ['title', 'description']

class CommentModelForm(forms.ModelForm):
    class Meta:
        model = Comment 
        fields = ['text']
