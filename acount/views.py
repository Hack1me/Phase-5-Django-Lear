import codecs

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.core.validators import validate_email
from django.db.models import Q
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from LENOXDEV import settings


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

#sign in view
def sign_in(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        messages = []

        if not email or not password:
            messages.append("Veuillez saisir votre email et votre mot de passe.")
            return render(request, 'acount/sign_in.html', {'messages': messages})

        try:
            validate_email(email)
        except ValidationError:
            messages.append("Adresse email invalide.")
            return render(request, 'acount/sign_in.html', {'messages': messages})

        user = User.objects.filter(email__iexact=email).first()
        if not user:
            messages.append("Aucun compte trouvé avec cet email.")
            return render(request, 'acount/sign_in.html', {'messages': messages})

        authuser = authenticate(request, username=user.username, password=password)
        if authuser is not None:
            login(request, authuser)
            return redirect('dashboard')

        messages.append("Mot de passe incorrect.")
        return render(request, 'acount/sign_in.html', {'messages': messages})

    return render(request, 'acount/sign_in.html')

#sign out view
def sign_out(request):
    logout(request)
    return redirect('sign_in')

#landing page view
def home(request):
    return render(request, 'acount/home.html')

#password reset request view
def password_reset(request):
    if request.method == "POST":
        email = request.POST.get("email")
        messages = []

        try:
            validate_email(email)
        except ValidationError:
            messages.append("Adresse email invalide.")
            return render(request, 'acount/password_reset_form.html', {'messages': messages})

        user = User.objects.filter(email__iexact=email).first()
        if not user:
            messages.append("Aucun compte trouvé avec cet email.")
            return render(request, 'acount/password_reset_form.html', {'messages': messages})

        # Here you would typically send a password reset email to the user.
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        current_site = request.META['HTTP_HOST']
        protocol = 'https://' if request.is_secure() else 'http://'
        context = {
            'user': user,
            'token': token,
            'uid': uid,
            'protocol': protocol,
            'domain': current_site
        }
        html_text = render_to_string('acount/email_template.html', context)
        msg = EmailMessage(
            "Réinitialisation du mot de passe",
            html_text,
            settings.DEFAULT_FROM_EMAIL,
            [email],
        )

        msg.content_subtype = "html"
        msg.send(fail_silently=False)

        # For this example, we'll just display a success message.
        messages.append("Un email de réinitialisation du mot de passe a été envoyé à votre adresse email.")
        return render(request, 'acount/password_reset_form.html', {'messages': messages})
    else:
        return render(request, 'acount/password_reset_form.html')

#password reset done view
def password_reset_done(request):
    return render(request, 'acount/password_reset_done.html')

def password_reset_confirm(request, token, uid):
    if request.method == "POST":
        password = request.POST.get("new_password1")
        confirm_password = request.POST.get("new_password2")
        messages = []
        print(f"Received token: {token}, uid: {uid}")  # Debugging line
        
        try:
            user_id = urlsafe_base64_decode(uid)
            decode_uid = codecs.decode(user_id, "utf-8")
            user = User.objects.get(pk=decode_uid)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            messages.append("Vous n'avez pas le droit de modifier les informations cet utilisateur")
            return render(request, 'acount/password_reset_confirm.html', {'messages': messages})
        
        check_token = default_token_generator.check_token(user, token)
        if not check_token:
            messages.append("Vous n'avez pas le droit de modifier les informations cet utilisateur")
            return render(request, 'acount/password_reset_confirm.html', {'messages': messages})
           
        if password != confirm_password:
            messages.append("Les mots de passe ne correspondent pas.")
            return render(request, 'acount/password_reset_confirm.html', {'messages': messages})

        try:
            validate_password(password)
            user.set_password(password)
            user.save()
        except ValidationError as e:
            messages.extend(e.messages)
            return render(request, 'acount/password_reset_confirm.html', {'messages': messages})

        # Here you would typically update the user's password in the database.
        print("Password has been reset successfully.")  # Placeholder for actual password reset logic
        # For this example, we'll just display a success message.
        return redirect('password_reset_complete')
    else:
        return render(request, 'acount/password_reset_confirm.html')

def password_reset_complete(request):
    return render(request, 'acount/password_reset_complete.html')

def password_reset_email(request):
    return render(request, 'acount/password_reset_email.html')

@login_required(login_url='sign_in')
def dashboard(request):
    return render(request, 'acount/dashboard.html')