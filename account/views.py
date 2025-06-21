from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from .forms import SignupForm , UserProfileForm
from .models import UserProfile
from  courses.models import Courses
from django.contrib.auth import update_session_auth_hash


# def sign_up(request):
#     form = SignupForm()
#     if request.method == 'POST':
#         form = SignupForm(request.POST)

#         if form.is_valid():
#             username = form.cleaned_data.get('username')  # احصل على اسم المستخدم

#             if User.objects.filter(username=username).exists():
#                 return render(request, 'account/signup.html', {
#             'error': 'اسم المستخدم مستخدم بالفعل. الرجاء اختيار اسم آخر.'
#             })
#             user = form.save() 
#             InstructorProfile.objects.create(user=user )
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password1')

#             user = authenticate(request, username = username, password = password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('account:view_profile',username=request.user.username)
            
        
#     context={
#         'form':form,
#              }

#     return render(request, 'account/signup.html', context)




def sign_up(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            if User.objects.filter(username=username).exists():
                # return render(request, 'account/signup.html', {
                #     'error': 'اسم المستخدم مستخدم بالفعل. الرجاء اختيار اسم آخر.'
                # })
                form.add_error('username', 'اسم المستخدم مستخدم بالفعل. الرجاء اختيار اسم آخر.')
            else:
                user = form.save(commit=False)  
                role = form.cleaned_data.get('role')
                user.save()
                UserProfile.objects.create(user=user, role=role)

                if role == 'student':
                    group = Group.objects.get(name='Students')
                    user.groups.add(group)
                elif role == 'instructor':
                    group = Group.objects.get(name='Instructors')
                    user.groups.add(group)

                password = form.cleaned_data.get('password1')
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    update_session_auth_hash(request, user)
                    return redirect('account:view_profile', username=user.username)
    else:
        form = SignupForm()
    context = {
        'form':form
    }

    return render(request, 'account/signup.html', context)




def sign_in(request):
    ERROR = None
    # لو هو قده عامل تسجيل دخول وعمل الرابط حق تسجيل الدخول بيوديه على طول للصفحة الرئيسية
    if request.user.is_authenticated:
        return redirect('courses:index')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('account:view_profile', username=request.user.username)
        else:
            ERROR = 'Invalid credentials! , password or username is invalid!'

    context = {
        'error':ERROR,
    }

    return render(request, 'account/signin.html', context, )

def sign_out(request):
    logout(request)
    return redirect('account:signin')


@login_required(login_url='account:signin')
def edit_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    form = UserProfileForm(instance=profile)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account:view_profile',username=request.user.username)
    
    context = {
        'form':form
    }

    return render(request, 'account/edit_profile.html', context)


@login_required(login_url='account:signin')
def view_profile(request, username):
    user = get_object_or_404(User, username = username)
    profile = get_object_or_404(UserProfile,  user=request.user)

    courses = Courses.objects.filter(owner = request.user)
    user_courses = request.user.enrolled_courses.all()
    context = {
        'profile': profile,
        'courses': courses,
        'user_courses': user_courses,
        'user_role': profile.role
    }
    print(user.get_all_permissions())

    return render(request,'account/view_profile.html', context)