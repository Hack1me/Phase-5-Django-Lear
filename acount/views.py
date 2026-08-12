from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db.models import Q
from django.shortcuts import redirect, render


# sign up view
def sign_up(request):
    if request.method == 'POST':
        
        # Handle form submission here
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password1')
        confirm_password = request.POST.get('password2')
        
        # Validate email format
        error = False
        messages = []
        try:
            validate_email(email)
        except ValidationError:
            # Handle invalid email
            messages.append("Invalid email address.")
            error = True
            return render(request, 'acount/sign_up.html', {'messages': messages})
        
        # Validate password and confirm password match
        if not error and password != confirm_password:
                # Handle password mismatch
            messages.append("Passwords do not match.")
            error = True
            return render(request, 'acount/sign_up.html', {'messages': messages})
        
        # Check if the username or email already exists
        user = User.objects.filter(Q(username=username) | Q(email=email)).first()
        if user :
            messages.append(f"Username {username} or email {email} already exists.")
            error = True
            return render(request, 'acount/sign_up.html', {'messages': messages})
        
        # Create the user if there are no errors       
        if not error:
            user = User(
                username=username, 
                email=email
                )
            user.set_password(password)
            user.save()
            return redirect('sign_in')
    else:
        return render(request, 'acount/sign_up.html')

def sign_in(request):
        return render(request, 'acount/sign_in.html')
    
def dashboard(request):
    return render(request, 'acount/dashboard.html')