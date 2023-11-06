from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from .models import UserProfile


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
