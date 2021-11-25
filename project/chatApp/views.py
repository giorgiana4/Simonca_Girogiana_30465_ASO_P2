from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http.response import JsonResponse, HttpResponse
from chatApp.models import Message
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from chatApp.serializers import MessageSerializer
from chatApp.forms import SelectUsers
from django.contrib.auth.models import Group
# Create your views here.

def login_view(request):
    if request.user.is_authenticated:
        return redirect('chatBoxe')
    if request.method == 'GET':
        return render(request, 'login.html', {})
    if request.method == 'POST':
        #primire username si password de la formul de login
        username = request.POST['username']
        password = request.POST['password']

        #autentificarea userului
        user = authenticate(username=username, password=password)

        if user is None:
            return HttpResponse('User not found! Verfy your credentials again, please!')
        else:
            login(request, user)
        return redirect('chatBoxe')


def chatBox_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'GET':
        return render(request, "chatBox.html",
                      {'users': User.objects.exclude(username=request.user.username)})

def message_view(request, sender, receiver):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'GET':
        print(Message.objects.filter(sender_id = sender, receiver_id = receiver) | Message.objects.filter(sender_id = receiver, receiver_id = sender))
        return render(request, "message.html",
                      {'users': User.objects.exclude(username = request.user.username),
                       'receiver': User.objects.get(id=receiver),
                       'messages': Message.objects.filter(sender_id = sender, receiver_id = receiver) |
                                  Message.objects.filter(sender_id = receiver, receiver_id = sender)
                      })


@csrf_exempt
def message_list(request, sender=None, receiver=None):
    """
    List all required messages, or create a new message.
    """
    if request.method == 'GET':
        messages = Message.objects.filter(sender_id=sender, receiver_id=receiver, is_read=False)
        serializer = MessageSerializer(messages, many=True, context={'request': request})
        for message in messages:
            message.is_read = True
            print("Mesajul este: ",message)
            print("userul este sau nu activ: ", User.objects.get(id=receiver))
            message.save()
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

def chat_view_groups(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == "GET":
        return render(request, 'chat_group.html',
                      {'groups': request.user.groups.all()})

def createGroup_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == "GET":
        form = SelectUsers()
        template = 'create_group.html'
        context = {'form': form}
        return render(request, template, context)
       # return render(request, 'chat/create-group.html',
       #         {'users': User.objects.exclude(username=request.user.username)})
    else:
        form = SelectUsers(request.POST)
        if form.is_valid():
            users = form.cleaned_data.get('Users')

            group_name = form.cleaned_data['group_name']
            g1 = Group.objects.create(name = group_name)
            i = 0
            for i in  range(0,len(users)):
                user = User.objects.get(id=users[i])
                g1.user_set.add(user)
                i+=1
            g1.user_set.add(request.user)
            groupp = Group.objects.get(name=group_name)
            users1 = groupp.user_set.all()
            print("Grupppp: ",request.user.groups.all())
            return redirect('chatBoxe')