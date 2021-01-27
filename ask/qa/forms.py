from django import  forms
from qa.models import Question
from qa.models import Answer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class AskForm(forms.Form):
    title = forms.CharField(max_length=100)
    text = forms.CharField(widget=forms.Textarea)

    def __init__(self, user, *args, **kwargs):
        self._user = user
        super(AskForm, self).__init__(*args, **kwargs)

    def clean_title(self):
        if len(self.cleaned_data['title']) == 0:
            raise forms.ValidationError(u'Title must be filled')
        else:
            return self.cleaned_data['title']

    def clean_text(self):
        if len(self.cleaned_data['text']) == 0:
            raise forms.ValidationError(u'Text must be filled')
        else:
            return self.cleaned_data['text']

    def save(self):
        self.cleaned_data['author'] = self._user
        self.cleaned_data['author'] = User.objects.all()[0]
        return Question.objects.create(**self.cleaned_data)


class AnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
    question = forms.IntegerField()

    def __init__(self, user, *args, **kwargs):
        self._user = user
        super(AnswerForm, self).__init__(*args, **kwargs)

    def clean_text(self):
        if len(self.cleaned_data['text']) == 0:
            raise forms.ValidationError(u'Text must be filled')
        else:
            return self.cleaned_data['text']

    def save(self):
        self.cleaned_data['author'] = self._user
        self.cleaned_data['author'] = User.objects.all()[0]
        self.cleaned_data['question'] = Question.objects.get(id=int(self.cleaned_data['question']))
        return Answer.objects.create(**self.cleaned_data)

class SignUpForm(forms.Form):
    username = forms.CharField(max_length=50)
    email = forms.EmailField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)
    redirectPage = forms.CharField(widget=forms.HiddenInput, required=False)

    def __init__(self, redirectPage, *args, **kwargs):
        self.redirectPage = redirectPage
        super(SignUpForm, self).__init__(*args, **kwargs)

    def clean_username(self):
        if len(self.cleaned_data['username']) == 0:
            raise forms.ValidationError(u'Username must be filled')
        else:
            return self.cleaned_data['username']

    def clean_password(self):
        if len(self.cleaned_data['password']) == 0:
            raise forms.ValidationError(u'Password must be filled')
        else:
            return self.cleaned_data['password']

    def save(self):
        User.objects.create_user(username=self.cleaned_data['username'],
                                 email=self.cleaned_data['email'],
                                 password=self.cleaned_data['password'])

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)
    redirectPage = forms.CharField(widget=forms.HiddenInput, required=False)

    def __init__(self, redirectPage, *args, **kwargs):
        self.redirectPage = redirectPage
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean_username(self):
        if len(self.cleaned_data['username']) == 0:
            raise forms.ValidationError(u'Username must be filled')
        else:
            return self.cleaned_data['username']

    def clean_password(self):
        if len(self.cleaned_data['password']) == 0:
            raise forms.ValidationError(u'Password must be filled')
        else:
            return self.cleaned_data['password']

    def save(self):
        return authenticate(username=self.cleaned_data['username'], password=self.cleaned_data['password'])
