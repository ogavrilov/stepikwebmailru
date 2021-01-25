from django import  forms
from qa.models import Question
from qa.models import Answer
from django.contrib.auth.models import User

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