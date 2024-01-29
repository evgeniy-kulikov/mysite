from django import forms
from .models import Comment
from django_summernote.widgets import SummernoteWidget  # Summernote редактор


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,
                               widget=forms.Textarea)



class CommentForm(forms.ModelForm):
    body = forms.CharField(required=True,
                           widget=SummernoteWidget())  # Summernote редактор
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']


# полнотекстовый поиск на ДБ postgres
class SearchForm(forms.Form):
    query = forms.CharField(label="Найти")