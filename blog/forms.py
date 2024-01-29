from django import forms
from .models import Comment
from django_summernote.widgets import SummernoteWidget  # Summernote редактор


# Дизайн Bootstrap 5
class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25, required=True, widget=forms.TextInput(attrs={"class": "form-control mb-1", 'placeholder': 'Name'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={"class": "form-control mb-1", 'placeholder': 'E-Mail'}))
    to = forms.EmailField(required=True, widget=forms.TextInput(attrs={"class": "form-control mb-1", 'placeholder': 'To'}))
    comments = forms.CharField(required=False,
                               widget=forms.Textarea(attrs={"class": "form-control mb-1", 'placeholder': 'Comments'}))

# class EmailPostForm(forms.Form):
#     name = forms.CharField(max_length=25)
#     email = forms.EmailField()
#     to = forms.EmailField()
#     comments = forms.CharField(required=False,
#                                widget=forms.Textarea)



# Дизайн Bootstrap 5
class CommentForm(forms.ModelForm):
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': 'Name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={"class": "form-control", 'placeholder': 'Email'}))
    body = forms.CharField(required=True,
                                # Summernote редактор
                               widget=SummernoteWidget(
                                   attrs={"class": "form-control", 'summernote': {'width': '100%', 'height': '300px'}}))


    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']

# class CommentForm(forms.ModelForm):
#     body = forms.CharField(required=True,
#                            widget=SummernoteWidget())  # Summernote редактор
#     class Meta:
#         model = Comment
#         fields = ['name', 'email', 'body']



# полнотекстовый поиск на ДБ postgres
# Дизайн Bootstrap 5
class SearchForm(forms.Form):
    query = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control mb-1", 'placeholder': 'Введите поисковый запрос...'}))

# class SearchForm(forms.Form):
#     query = forms.CharField(label="Найти")