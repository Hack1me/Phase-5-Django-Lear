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
        if not validate_email(email):
            # Handle invalid email
            messages.append("Invalid email address.")
            error = True
        if password != confirm_password:
            # Handle password mismatch
            messages.append("Passwords do not match.")
            error = True
            
        print(f"Username: {username}, Email: {email}, Password: {password}, Confirm Password: {confirm_password}")
        
        # Perform validation and save the user to the database
        
        # Redirect to a success page or login page after successful registration
        return render(request, 'acount/sign_in.html', {'success': True})
    else:
        return render(request, 'acount/sign_up.html', {'messages': messages})


def sign_in(request):
        return render(request, 'acount/sign_in.html')
    
def dashboard(request):
    return render(request, 'acount/dashboard.html')