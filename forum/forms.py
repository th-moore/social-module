from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout

from .models import Group, Post, Comment


# Groups

class GroupJoinForm(forms.Form):
    group = forms.ModelChoiceField(queryset=Group.objects.all(), widget=forms.HiddenInput)


# Posts

class PostCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'title',
            'body',
        )
    
    class Meta:
        model = Post
        fields = ['title', 'body']


class PostEditForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'title',
            'body',
        )

    class Meta:
        model = Post
        fields = ['title', 'body']


# Comments

class PostCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('title', 'body')
        help_texts = {
            'body': "Keep it friendly.",
        }