from .face_detection.face_verify import gen_frames,check_face_recognition
from django.http import StreamingHttpResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.views.decorators import gzip
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.contrib import messages
from django.template import loader
from .forms import CreateUserForm, CreateUserInfoForm
from .forms import LoginForm
from .models import User
from voteApp.models import VoterVote
import base64
import os


def register_page(request):

    user_form = CreateUserForm()
    user_info_form = CreateUserInfoForm()
    if request.method == "POST":
        user_form = CreateUserForm(request.POST)
        user_info_form = CreateUserInfoForm(request.POST)
        
        if user_form.is_valid() and user_info_form.is_valid():
            membership_number = user_form.cleaned_data.get('username')
            user_form.save()
            user_info = user_info_form.save(commit=False)
            directory = f"assets/faces/{membership_number}/1.jpg"
            user_info.image_path = directory
            user_info.membership_number = membership_number
            user_info.save()
            
            
            new_entry = VoterVote(voter=membership_number)
            new_entry.save()
            
            return redirect("register_photo",id = membership_number)
        else:
            messages.error(request, 'Failed. Please check your input.')


    else:
        user_form = CreateUserForm()
        user_info_form = CreateUserInfoForm()
    return render(request, "registration.html", {'user_form': user_form, 'user_info_form':user_info_form})

def take_photo(request,id):
    template = loader.get_template('take_photo.html')
    context = {
        'id':id
    }
    
    return HttpResponse(template.render(context))

def save_image(request):
    if request.method == 'POST':
        # Get the base64 encoded image data from the request
        image_data = request.POST.get('image_data')
        id = request.POST.get('id')
        
        # Decode the base64 data
        image_binary = base64.b64decode(image_data.split(",")[1])

        # Construct the directory path
        directory = os.path.join('assets','faces', str(id))

        # Ensure the directory exists, create it if it doesn't
        if not os.path.exists(directory):
            os.makedirs(directory)


        # Construct the filename with the next serial number
        filename = os.path.join(directory, "1.jpg")

        # Save the image to a file
        with open(filename, 'wb') as f:
            f.write(image_binary)

        return JsonResponse({'message': 'Image saved successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'})

def home(request):
    template = loader.get_template('home.html')
    context = {}
    
    return HttpResponse(template.render(context))

def login_verify(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect("photo_verify",id= username)
            else:
                messages.error(request, 'Invalid username or password. Please try again.')
    
    context = {'loginform':form}
    return render(request, 'login.html', context=context)

@login_required(login_url='login')
def photo_verify(request, id):
    

    return render(request, 'photo_verify.html', {'id':id})

@login_required(login_url='login')  
def ballot_collection(request,id):
    template = loader.get_template('ballot_collection.html')
    context = {
        'id':id
    }
    
    return HttpResponse(template.render(context))

@login_required(login_url='login')
def web_feed(request,id):
    user = User.objects.get(membership_number=id)
    image_path = user.image_path
    return StreamingHttpResponse(gen_frames(id,image_path), content_type='multipart/x-mixed-replace; boundary=frame')

@login_required(login_url='login')  
def verify_face(request,id):
    is_face_recognition = check_face_recognition()
    if is_face_recognition:
        return JsonResponse({"success": True, "redirectUrl": "/authentication/ballot_collection/{}/".format(id)})
    else:
        return JsonResponse({"success": False})
    
def logout(request):
    auth.logout(request)
    return redirect("home")
