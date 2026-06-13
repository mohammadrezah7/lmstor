from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import LoginForm


def user_login(request):
    if request.user.is_authenticated:
        return redirect_to_dashboard(request)
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            remember = form.cleaned_data.get('remember_me', False)
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                
                # Remember me
                if not remember:
                    request.session.set_expiry(0)
                else:
                    request.session.set_expiry(86400 * 30)  # 30 days
                
                # Welcome message based on role
                role = request.session.get('role', 'admin')
                name = user.get_full_name() or user.username
                
                if role == 'student':
                    messages.success(request, f'{name} عزیز، به پنل دانشجویی خوش آمدید! 📚')
                elif role == 'professor':
                    messages.success(request, f'استاد {name}، به پنل اساتید خوش آمدید! 🎓')
                else:
                    messages.success(request, f'مدیر {name}، به پنل مدیریت خوش آمدید! ⚙️')
                
                return redirect_to_dashboard(request)
            else:
                messages.error(request, '❌ کد ملی/ایمیل یا رمز عبور اشتباه است!')
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


def user_logout(request):
    logout(request)
    # Clear session
    for key in ['role', 'student_id', 'professor_id']:
        if key in request.session:
            del request.session[key]
    messages.info(request, '👋 شما با موفقیت خارج شدید.')
    return redirect('accounts:login')


def redirect_to_dashboard(request):
    """Redirect user based on their role"""
    role = request.session.get('role', 'admin')
    
    if role == 'student':
        return redirect('students:my_dashboard')
    elif role == 'professor':
        return redirect('professors:my_dashboard')
    else:
        return redirect('core:dashboard')