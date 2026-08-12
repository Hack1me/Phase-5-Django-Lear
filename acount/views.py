# from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import render


# Create your views here.
def sign_up(request):
    if request.method == 'POST':
        # Handle form submission here
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password1')
        confirm_password = request.POST.get('password2')
        
        error = False
        messages = []
        try:
            validate_email(email)
        except ValidationError:
            # Handle invalid email
            messages.append("Invalid email address.")
            error = True
            return render(request, 'acount/sign_up.html', {'messages': messages})
        if not error and password != confirm_password:
                # Handle password mismatch
            messages.append("Passwords do not match.")
            error = True
            return render(request, 'acount/sign_up.html', {'messages': messages})
            
        if not error:
            print(f"Username: {username}, Email: {email}, Password: {password}, Confirm Password: {confirm_password}")
            messages.append("Account created successfully.")
            return render(request, 'acount/sign_in.html', {'success': True})
    else:
        return render(request, 'acount/sign_up.html')

def sign_in(request):
        return render(request, 'acount/sign_in.html')
    
def dashboard(request):
    return render(request, 'acount/dashboard.html')