from urllib import request

from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib import messages
from . models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
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
    if not request.user.is_authenticated:
        return redirect('admin-login')
    return render(request, 'dashboard.html')
def logout(request):
    auth_logout(request)
    return redirect('admin-login')

@login_required
def create_class(request):
    if request.method == 'POST':
        try:
         class_name = request.POST.get('classname')
         section = request.POST.get('sectionname')
         Class.objects.create(class_name=class_name, section=section)
         messages.success(request, "Class created successfully") 
         return redirect('create-class') 
        except Exception as e: 
            messages.error(request, f"Something went wrong: {str(e)}")
            return redirect('create-class') 
    return render(request, 'create_class.html')

@login_required
def view_classes(request):
    classes = Class.objects.all()

    if request.GET.get('delete'):
        try:
            class_id = request.GET.get('delete')
            class_obj = get_object_or_404(Class, id=class_id)
            class_obj.delete()
            messages.success(request, "Class deleted successfully")
            return redirect('view-classes')
        except Exception as e:
            messages.error(request, f"Something went wrong: {str(e)}")
            return redirect('view-classes')
    return render(request, 'view_class.html', {'classes': classes})

@login_required
def edit_class(request, class_id):

    class_obj = get_object_or_404(Class, id=class_id)

    if request.method == 'POST':
        try:
            class_name = request.POST.get('class_name')
            section = request.POST.get('section')

            class_obj.class_name = class_name
            class_obj.section = section

            class_obj.save()

            messages.success(request, "Class updated successfully")
            return redirect('view-classes')

        except Exception as e:
            messages.error(request, f"Something went wrong: {str(e)}")
            return redirect('edit-class', class_id=class_id)

    return render(request, 'edit_class.html', {'class_obj': class_obj}) 

@login_required
def create_subject(request):
    if request.method == 'POST':
        try:
         subject_name = request.POST.get('subjectname')
         subject_code = request.POST.get('subjectcode')
         Subject.objects.create(subject_name=subject_name, subject_code=subject_code)
         messages.success(request, "Subject created successfully") 
         return redirect('create-subject') 
        except Exception as e: 
            messages.error(request, f"Something went wrong: {str(e)}")
            return redirect('create-subject') 
    return render(request, 'create_subject.html')   

@login_required
def manage_subjects(request):
    subjects = Subject.objects.all()

    if request.GET.get('delete'):
        try:
            subject_id = request.GET.get('delete')
            subject_obj = get_object_or_404(Subject, id=subject_id)
            subject_obj.delete()
            messages.success(request, "Subject deleted successfully")
            return redirect('manage-subjects')
        except Exception as e:
            messages.error(request, f"Something went wrong: {str(e)}")
            return redirect('manage-subjects')
    return render(request, 'manage_subjects.html', {'subjects': subjects})  

@login_required
def edit_subject(request, subject_id):

    subject_obj = get_object_or_404(Subject, id=subject_id)

    if request.method == 'POST':
        try:
            subject_name = request.POST.get('subject_name')
            subject_code = request.POST.get('subject_code')

            subject_obj.subject_name = subject_name
            subject_obj.subject_code = subject_code

            subject_obj.save()

            messages.success(request, "Subject updated successfully")
            return redirect('manage-subjects')

        except Exception as e:
            messages.error(request, f"Something went wrong: {str(e)}")
            return redirect('edit-subject', subject_id=subject_id)

    return render(request, 'edit_subject.html', {'subject_obj': subject_obj}) 

@login_required
def create_subject_combination(request):
    classes = Class.objects.all()
    subjects = Subject.objects.all()

    if request.method == 'POST':
        try:
            class_id = request.POST.get('class')
            subject_id = request.POST.get('subject')
            SubjectCombination.objects.create(student_class_id=class_id, subject_id=subject_id, status=1)
            messages.success(request, "Subject combination created successfully")
            return redirect('create-subjectcombination')
        except Exception as e:
            messages.error(request, f"Something went wrong: {str(e)}")
            return redirect('create-subjectcombination')

    return render(request, 'create_subject_combination.html', {'classes': classes, 'subjects': subjects})   

@login_required
def manage_subject_combinations(request):
    combinations = SubjectCombination.objects.all()
    act = request.GET.get('act')
    if request.GET.get('act'):
        try:
           SubjectCombination.objects.filter(id = act).update(status=1)
           messages.success(request, "Subject combination activated successfully")
           return redirect('manage-subjectcombinations')
        except Exception as e:
            messages.error(request, f"Something went wrong: {str(e)}")
            return redirect('manage-subjectcombinations')
        
    dia = request.GET.get('dia')
    if request.GET.get('dia'):
        try:
           SubjectCombination.objects.filter(id = dia).update(status=0)
           messages.success(request, "Subject combination deactivated successfully")
           return redirect('manage-subjectcombinations')
        except Exception as e:
            messages.error(request, f"Something went wrong: {str(e)}")
            return redirect('manage-subjectcombinations')
    return render(request, 'manage_subjectcombinations.html', {'combinations': combinations})  
