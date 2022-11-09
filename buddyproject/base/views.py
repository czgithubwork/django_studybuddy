from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import login, logout, authenticate
from base.models import Room, Topic, Message, User
from base.forms import RoomForm, UserCreationForm, UserForm, AuthenticationForm
from django.contrib import messages
# Create your views here.

# rooms = [{'id':1, 'name':'Learn django', 'host':'echu', 'topic': 'django'},
# {'id':2, 'name':'Learn python', 'host':'tim', 'topic': 'python'}]

def index(request):
    context = {}
    return render(request, 'index.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email,password=password)
            if user is not None:
                login(request,user)
                return redirect('home')
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")

    context = {'login_form' : form}
    return render(request, 'base/login_register.html', context)


def logoutPage(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.username = form.username.lower()
            form.save()
            login(request, form)
            return redirect('home')
        else:
            form = UserCreationForm(request.POST, request.FILES)

    context = {'register_form': form}
    return render(request, 'base/login_register.html', context)


def home(request):
    rooms = Room.objects.all()
    topics = Topic.objects.all()
    activities = Message.objects.all()
    # participants = rooms.participants.all()

    query = request.GET.get('q')
    if query:
        #topic__name or ... contains query with no case sensitive
        rooms = Room.objects.filter(Q(topic__name__icontains=query) | Q(name__icontains=query) | Q(description__icontains=query))
        activities = Message.objects.filter(Q(room__topic__name__icontains=query))

    room_count = rooms.count()
    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count, 'activities': activities}
    return render(request, 'base/home.html', context)


def room(request,pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        Message.objects.create(user=request.user, room=room, body=request.POST.get('body'))
        room.participants.add(request.user)        
        return redirect('room', pk=room.id)


    context = {'room': room, 'room_messages': room_messages, 'participants':participants}
    return render(request, 'base/room.html', context)


def userProfilePage(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    activities = user.message_set.all()
    topics = Topic.objects.all()

    context = {'user': user,'rooms': rooms, 'topics': topics, 'activities': activities}
    return render(request, 'base/user_profile.html', context)


def topicsPage(request):
    topics = Topic.objects.all()
    query = request.GET.get('q')
    if query:
        topics = Topic.objects.filter(Q(name__icontains=query))

    context={'topics': topics}
    return render(request, 'base/topics.html', context)


@login_required(login_url='/login/')
def createRoom(request):
    form  = RoomForm()
    if request.method == 'POST':
        form  = RoomForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.host = request.user
            form.save()
            form.participants.add(request.user)
            return redirect('home')

    context = {'form' : form}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='/login/')
def updateRoom(request,pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return redirect('home')

    form = RoomForm(instance=room)
    if request.method == 'POST':
        #specify instance to update the specify room
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form':form}
    return render(request,'base/room_form.html', context)


@login_required(login_url='/login/')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return redirect('home')
    
    if request.method == 'POST':
        room = room.delete()
        return redirect('home')

    context = {'obj' : room}
    return render(request, 'base/delete.html', context)


@login_required(login_url='/login/')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    room = message.room

    if request.user != message.user:
        return redirect('room', room.id)

    if request.method == 'POST':
        message = message.delete()
        #if user does not have any comments in the room, remove user from participants list
        count = Message.objects.filter(room=room, user=request.user).count()
        if count == 0:
            room.participants.remove(request.user)
        
        return redirect('room', room.id)

    context = {'obj': message}
    return render(request, 'base/delete.html', context)


@login_required(login_url='/login/')
def updateProfile(request):
    form = UserForm(instance=request.user)

    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile', pk=request.user.id)

    context={'form': form}
    return render(request, 'base/update_profile.html', context)
