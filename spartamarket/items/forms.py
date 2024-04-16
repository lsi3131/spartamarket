from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from items.models import Article, Comment


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = "__all__"
        exclude = ('author',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = "__all__"
        exclude = ('article', )


