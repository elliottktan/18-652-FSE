from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

from django.contrib.auth.tokens import default_token_generator

from forms import PostForm
from models import Post
import datetime

def display(request):
    errors = []
    context = {}
    if request.user.is_authenticated():
        context['username'] = request.user.username
        context['posts'] = getAllPosts()
        return render(request, 'chatapp/index-loggedin.html', context)
    return redirect('/chatapp/login')
    #user = request.POST.get('user', False)
    #return render(request, 'chatapp/index.html', context)

def register(request):
    context = {}
    # Just display the registration form if this is a GET request
    if request.method == 'GET':
        return render(request, 'chatapp/register.html', context)

    errors = []
    context['errors'] = errors

    # Checks the validity of the form data
    if not 'username' in request.POST or not request.POST['username']:
	   errors.append('Username is required.')
    else:
        # Save the username in the request context to re-fill the username
        # field in case the form has errrors
	   context['username'] = request.POST['username']

    if not 'password1' in request.POST or not request.POST['password1']:
	   errors.append('Password is required.')
    if not 'password2' in request.POST or not request.POST['password2']:
	   errors.append('Confirm password is required.')

    if 'password1' in request.POST and 'password2' in request.POST \
       and request.POST['password1'] and request.POST['password2'] \
       and request.POST['password1'] != request.POST['password2']:
	   errors.append('Passwords did not match.')

    if len(User.objects.filter(username = request.POST['username'])) > 0:
	   errors.append('Username is already taken.')

    if errors:
        return render(request, 'chatapp/register.html', context)

    # Creates the new user from the valid form data
    username = request.POST['username']
    password = request.POST['password1']

    new_user = User.objects.create_user(username=username, \
                                        password=password)
    new_user.is_active = True
    token = default_token_generator.make_token(new_user)
    new_user.first_name = token

    new_user.save()

    user = authenticate(username=username, password=password)
    login(request, user)

    return redirect('/chatapp')

@login_required
def post(request):
    errors = []
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            new_post = Post(text=text, user=request.user, 
                            date=datetime.datetime.now())
            new_post.save()
            print request.user.username + ": " + text
            return redirect('/chatapp')

    return redirect('/chatapp')

def getAllPosts():
    try:
        return Post.objects.all()
    except ObjectDoesNotExist:
        return []
           
def getPosts(request):
    context = {}
    context['posts'] = getAllPosts
    return render(request, 'chatapp/posts.xml', context, content_type='application/xml')