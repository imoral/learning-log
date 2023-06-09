from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpRequest
from django.shortcuts import render, redirect


# Create your views here.
def register(request: HttpRequest):
    """Register a new user."""
    if request.method != 'POST':
        # Display a blank registration form
        form = UserCreationForm()
    else:
        # Complete user registration
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            # Log the user in and then redirect to home page.
            login(request, new_user)
            return redirect('learning_logs:index')

    context = {'form': form}
    return render(request, 'registration/register.html', context)
