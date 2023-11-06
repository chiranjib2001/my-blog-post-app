from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from .models import UserProfile, Blog
from django.http import JsonResponse, HttpResponse




def view_blog_by_id(request, blog_id):
    if request.method == "GET":
        blog = Blog.objects.filter(id=blog_id, delete_flag=False).first()

        if blog:
            return render(request, 'blog.html', {'blog': blog})
        else:
            return JsonResponse({'message': 'Invalid blog_id'}, status=404)
    else:
        return HttpResponse("Invalid request method", status=400)


def view_blogs(request):
    latest_blogs = Blog.objects.filter(delete_flag=False).order_by('-create_timestamp')[:5]
    context = {'latest_blogs': latest_blogs}
    return render(request, 'index.html', context)


def index(request):
    # Get the latest blogs from the database
    latest_blogs = Blog.objects.all()[:5]  # Change this query to retrieve the latest blogs as needed
    context = {
        'latest_blogs': latest_blogs,
    }
    return render(request, 'index.html', context)


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        # Authenticate the user
        user = authenticate(request, email=email, password=password)
        if user is not None:
            # Login the user
            login(request, user)
            return redirect('home')  # Redirect to the home page after successful login
        else:
            # Handle authentication failure (incorrect login or password)
            return render(request, 'login.html', {'error_message': 'Incorrect login or password'})
    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Additional fields for UserProfile
            UserProfile.objects.create(
                user=user,
                name=request.POST['name'],
                emailid=request.POST['emailid'],
                phone_number=request.POST['phone_number'],
                role='viewer',  # You can set the default role here
                password='',  # Set the password here if necessary
                gender=request.POST['gender']
            )

            # Log the user in after registration
            login(request, user)
            return redirect('home')  # Redirect to a page after successful registration

    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})
