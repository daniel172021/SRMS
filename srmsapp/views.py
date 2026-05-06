from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.contrib import messages
# Create your views here.
def index(request):
    return render(request, 'index.html')

def admin_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Perform authentication logic here
        # For example, you can use Django's built-in authentication system
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('dashboard')  # Redirect to the dashboard after successful login
        else:
            # Handle invalid login credentials
            #return render(request, 'admin_login.html', {'error': 'Invalid username or password'})
            error = 'Invalid username or password'
    return render(request, 'admin_login.html', locals())

def dashboard(request):
    return render(request, 'dashboard.html')

def create_class(request):
    return render(request, 'create_class.html')