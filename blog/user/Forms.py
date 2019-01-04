
from django import forms

class userForm(forms.Form):
    name=forms.CharField(max_length=20,min_length=2,label='姓名')
    age=forms.IntegerField(label='年龄')
    password = forms.CharField(max_length=20,min_length=6,label='密码')

