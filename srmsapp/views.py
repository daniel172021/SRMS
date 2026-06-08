from urllib import request

from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib import messages
from . models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Student, Class

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

@login_required
def add_student(request):
    classes = Class.objects.all()

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        gender = request.POST.get('gender')
        id_number = request.POST.get('id_number')
        email = request.POST.get('email')
        dob = request.POST.get('dob')
        class_id = request.POST.get('student_class')

        try:
            if Student.objects.filter(id_number=id_number).exists():
                messages.error(request, "Student ID already exists.")
                return redirect('add-student')

            if Student.objects.filter(email=email).exists():
                messages.error(request, "Email already exists.")
                return redirect('add-student')

            student_class = None
            if class_id:
                student_class = Class.objects.get(id=class_id)

            Student.objects.create(
                first_name=first_name,
                last_name=last_name,
                gender=gender,
                id_number=id_number,
                email=email,
                dob=dob,
                student_class=student_class
            )

            messages.success(request, "Student added successfully.")
            return redirect('add-student')

        except Class.DoesNotExist:
            messages.error(request, "Selected class does not exist.")

        except Exception as e:
            messages.error(request, f"Error: {str(e)}")

    return render(
        request,
        'add_student.html',
        {
            'classes': classes
        }
    )

@login_required
def manage_students(request):
    students = Student.objects.all()
    if request.GET.get('delete'):
        try:
            student_id = request.GET.get('delete')
            student_obj = get_object_or_404(Student, id=student_id)
            student_obj.delete()
            messages.success(request, "Student deleted successfully")
            return redirect('manage-students')
        except Exception as e:
            messages.error(request, f"Something went wrong: {str(e)}")
            return redirect('manage-students')      
    return render(request, 'manage_students.html', {'students': students})  

@login_required
def edit_student(request, student_id):

    student_obj = get_object_or_404(Student, id=student_id)
    classes = Class.objects.all()

    if request.method == 'POST':
        try:
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            gender = request.POST.get('gender')
            id_number = request.POST.get('id_number')   
            email = request.POST.get('email')
            dob = request.POST.get('dob')
            class_id = request.POST.get('student_class')    
            student_class = None
            if class_id:
                student_class = Class.objects.get(id=class_id)  
            student_obj.first_name = first_name
            student_obj.last_name = last_name   
            student_obj.gender = gender
            student_obj.id_number = id_number   
            student_obj.email = email
            student_obj.dob = dob       
            student_obj.student_class = student_class
            student_obj.save()
            messages.success(request, "Student updated successfully")
            return redirect('manage-students')  
        except Class.DoesNotExist:
            messages.error(request, "Selected class does not exist.")
            return redirect('edit-student', student_id=student_id)  
        except Exception as e:
            messages.error(request, f"Something went wrong: {str(e)}")
            return redirect('edit-student', student_id=student_id)      
    return render(request, 'edit_student.html', {'student_obj': student_obj, 'classes': classes})   
    
@login_required
def add_result(request):
    classes = Class.objects.all()
    subjects = Subject.objects.all()
    students = Student.objects.all()

    if request.method == 'POST':
        try:
            student_id = request.POST.get('student')
            class_id = request.POST.get('student_class')
            subject_id = request.POST.get('subject')
            marks = request.POST.get('marks')

            student = Student.objects.get(id=student_id)
            student_class = Class.objects.get(id=class_id)
            subject = Subject.objects.get(id=subject_id)        
            Result.objects.create(
                student=student,
                student_class=student_class,
                subject=subject,
                marks=marks
            )
            messages.success(request, "Result added successfully.")
            return redirect('add-result')
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
    return render(request, 'add_result.html', {'classes': classes, 'subjects': subjects, 'students': students})

@login_required
def manage_results(request):
    results = Result.objects.all()
    if request.GET.get('delete'):
        try:
            result_id = request.GET.get('delete')
            result_obj = get_object_or_404(Result, id=result_id)
            result_obj.delete()
            messages.success(request, "Result deleted successfully")
            return redirect('manage-results')
        except Exception as e:
            messages.error(request, f"Something went wrong: {str(e)}")
            return redirect('manage-results')      
    return render(request, 'manage_results.html', {'results': results})     

@login_required
def edit_result(request, result_id):

    result = get_object_or_404(Result, id=result_id)

    classes = Class.objects.all()
    subjects = Subject.objects.all()
    students = Student.objects.all()

    if request.method == 'POST':
        try:
            result.student = Student.objects.get(
                id=request.POST.get('student')
            )

            result.student_class = Class.objects.get(
                id=request.POST.get('student_class')
            )

            result.subject = Subject.objects.get(
                id=request.POST.get('subject')
            )

            result.marks = request.POST.get('marks')

            result.save()

            messages.success(request, "Result updated successfully.")
            return redirect('manage-results')

        except Exception as e:
            messages.error(request, f"Something went wrong: {str(e)}")
            return redirect('manage-results')

    return render(request, 'edit_result.html', {
        'result': result,
        'students': students,
        'classes': classes,
        'subjects': subjects,
    })