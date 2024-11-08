from django.shortcuts import render, redirect
from .models import Topics, Messages, User, Rooms
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RoomCreationForm, MyUserCreationform, UserForm

def home_viw(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Rooms.objects.filter(
        Q(name__icontains=q) |
        Q(topic__name__icontains=q) |
        Q(host__name__icontains=q) |
        Q(description__icontains=q)
    )
    messages = Messages.objects.filter(
        Q(room__name__icontains=q) |
        Q(user__name__icontains=q) |
        Q(body__icontains=q)
    )[0:rooms.count()]
    topics = Topics.objects.all()[0:rooms.count() * 3]
    for topic in topics:
        if topic.room.count == 0:
            topic.delete()
    context = {
        'topics': topics,
        'messages': messages,
        'rooms': rooms
    }
    return render(request, 'home.html', context)


def room_details(request, pk):
    room = Rooms.objects.get(id=pk)
    messages = Messages.objects.filter(room=room)
    participants = room.participants.all()
    if request.method == 'POST':
        body = request.POST['body']
        Messages.objects.create(body=body, room=room, user=request.user)
        room.participants.add(request.user)
    return render(request, 'room_details.html', {'room': room, 'messages': messages, 'participants': participants})


@login_required(login_url='login')
def room_update_view(request, pk):
    room = Rooms.objects.get(id=pk)
    form = RoomCreationForm(initial={
        'name': room.name,
        'topic': room.topic.name,
        'description': room.description
    })
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topics.objects.get_or_create(name=topic_name)
        room.delete()
        room, created= Rooms.objects.get_or_create(
            topic=topic,
            host=request.user,
            name=request.POST.get('name'), 
            description=request.POST.get('description'))
        return redirect('home')
    topics = Topics.objects.all()
    context = {
        'form':form,
        'topics':topics
    }
    return render(request, 'room-update.html', context)


def topic_details(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topics.objects.filter(Q(name__icontains=q))
   
    context = {
        'topics': topics
    }
    return render(request, 'topic_details.html', context)


@login_required(login_url="login")
def delete_room(request, pk):
    room = Rooms.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    context = {'room':room}
    return render(request, 'delete.html', context)


@login_required(login_url='login')
def delete_message(request, pk):
    message = Messages.objects.get(id=pk)
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    context = {
        'message': message
    }
    return render(request, 'delete.html', context)


@login_required(login_url='login')
def room_create(request):
    rooms = Rooms.objects.all()
    form = RoomCreationForm()
    if request.method == 'POST':
        topic, created = Topics.objects.get_or_create(name=request.POST.get('topic'))
        host = User.objects.get(email=request.user.email)
        Rooms.objects.create(name=request.POST.get('name'), topic=topic, host=host, description=request.POST.get('description'))
        return redirect('home')
    context ={
        'form': form,
        'rooms':rooms
    }
    return render(request, 'room_create.html', context)


def login_view(request):
    
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        login(request, user)
        return redirect('home')
    return render(request, 'login.html')


def signup_view(request):
    form = MyUserCreationform()
    if request.method == 'POST':
        form = MyUserCreationform(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            return redirect('home')
        else:
            print('Error something')
    context = {'form': form}
    return render(request, 'signup.html', context)


def userInfo_view(request, pk):
    topics = Topics.objects.all()
    user = User.objects.get(id=pk)
    rooms = Rooms.objects.filter(host=user)
    messages = Messages.objects.filter(user=user)
    context = {
        'user':user, 
        'messages': messages, 
        'rooms': rooms, 
        'topics': topics
    }
    return render(request, 'userInfo.html', context)


@login_required(login_url='login')
def edit_user_view(request):
    user = User.objects.get(email=request.user.email)
    form = UserForm(initial={
        'name': user.name,
        'username': user.username,
        'bio': user.bio,
        'avatar': user.avatar
    })
    context = {
        'form': form
    }
    return render(request, 'user_edit.html', context)


@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('home')