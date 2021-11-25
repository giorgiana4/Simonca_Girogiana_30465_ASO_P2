from django.shortcuts import render, redirect
from django.contrib.auth.models import  User
from django import forms


def login(request):
    if request.user.is_authenticated:
        return redirect('chatBox')
    if request.method == 'GET':
        return render(request, '')

class SelectUsers(forms.Form):
    OPTIONS = User.objects.values_list('id', 'username')

    group_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    Users = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                          choices=OPTIONS)