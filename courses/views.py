from django.shortcuts import render, redirect, get_object_or_404
from .models import Subject, Courses, Module
from django.contrib.auth.decorators import login_required, permission_required
from .forms import CourseForm, ModuleForm
from django.http import HttpResponseForbidden
from django.contrib import messages
from account.models import UserProfile
# Create your views here.

@login_required(login_url='account:signin')
def subject_courses_list(request):
    # ذي تجيب المادة مع حقه الكورسات 
    subjects = Subject.objects.prefetch_related('courses').all()
    courses = Courses.objects.all()
    return render(request, 'course/index.html', context={'subjects':subjects, 'courses':courses})

def courses_list(request):
    course = Courses.objects.all()
    return render(request, 'course/courses_list.html', context={'courses':course})

def subjecta_list(request):
    subject = Subject.objects.all()
    return render(request, 'course/subjects_list.html', context={'subjects':subject})

@login_required(login_url='account:signin')
def courses_details(request, slug):
    course = get_object_or_404(Courses, slug = slug)
    is_owner = (course.owner == request.user)
    profile = get_object_or_404(UserProfile, user = request.user)
    context = {
        'course_info':course,
        'user_role': profile.role,
        'is_owner': is_owner
    }
    return render(request, 'course/course_details.html', context)


@login_required(login_url='account:signin')
@permission_required('courses.add_courses', raise_exception=True)
def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST ,request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.owner = request.user
            course.save()
            return redirect('courses:index')
    else:
        form = CourseForm()
    
    context = {
        'form':form
    }
    return render(request, 'course/add_course.html', context)


@login_required(login_url='account:signin')
def edit_course(request, slug):
    course = get_object_or_404(Courses, slug = slug, owner=request.user)
    form = CourseForm(instance=course)

    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            return redirect('account:view_profile',username=request.user.username)
    
    context = {
        'form':form,
        'course': course
    }

    return render(request, 'course/edit_course.html', context)

@login_required
@permission_required('courses.delete_courses', raise_exception=True)
def delete_course(request, slug):
    course = get_object_or_404(Courses, slug=slug, owner=request.user)

    if request.method == 'POST':
        course.delete()
        return redirect('account:view_profile',username=request.user.username)

    # عند GET، عرض نموذج تأكيد الحذف
    return redirect('account:view_profile',username=request.user.username)

@login_required()
@permission_required('courses.add_module', raise_exception=True)
def add_module(request, slug):
    course = get_object_or_404(Courses, slug=slug)
    if request.method == 'POST':
        form = ModuleForm(request.POST)
        if form.is_valid():
            module = form.save(commit=False)
            module.course = course
            module.save()
            return redirect ('courses:course_details', slug=course.slug)
    else:
        form = ModuleForm()
    context = {
        'form':form,
        'course':course
    }
    return render(request, 'course/add_module.html', context)

@login_required
@permission_required('courses.can_change_module', raise_exception=True)
def edit_module(request,slug):
    module = get_object_or_404(Module, course__slug=slug, course__owner=request.user)
    form = ModuleForm(instance=module)
    if request.method == 'POST':
        form = ModuleForm(request.POST, instance=module)
        if form.is_valid():
            form.save()
            return redirect('courses:course_details', slug=slug)
    context = {
        'module':module,
        'form':form
    }
    return render(request, 'course/edit_module.html', context)

@login_required
@permission_required('courses.can_delete_module', raise_exception=True)
def delete_module(request, pk):
    module = get_object_or_404(Module, pk=pk, course__owner=request.user)
    course_slug = module.course.slug
    if request.method == 'POST':
        module.delete()
        return redirect('courses:course_details', slug=course_slug)
    
    return redirect('courses:course_details', slug=course_slug)
    

@login_required
def enroll_course(request, slug):
    course = get_object_or_404(Courses, slug=slug)
    # if request.user in course.students.all():
    #     messages.info(request, 'أنت مسجل بالفعل في هذا الكورس.')
    # else:
    course.students.add(request.user)
    messages.success(request, 'تم تسجيلك في الكورس بنجاح.')

    return redirect ('courses:course_details', slug=course.slug)

@login_required
def unenroll_course(request, slug):
    course = get_object_or_404(Courses, slug=slug)
    # if request.user in course.students.all():
    course.students.remove(request.user)
    messages.success(request, 'تم إلغاء تسجيلك في الكورس بنجاح.')
    return redirect ('courses:course_details', slug=course.slug)
