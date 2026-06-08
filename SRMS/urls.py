

from django.contrib import admin
from django.urls import path
from srmsapp.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='home'),
    path('admin-login/', admin_login, name='admin-login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('create-class/', create_class, name='create-class'),
    path('logout/', logout, name='logout'),
    path('view-classes/', view_classes, name='view-classes'),
    path('edit-class/<int:class_id>/', edit_class, name='edit-class'),
    path('create-subject/', create_subject, name='create-subject'), 
    path('manage-subjects/', manage_subjects, name='manage-subjects'),
    path('edit-subject/<int:subject_id>/', edit_subject, name='edit-subject'),
    path('create-subjectcombination/', create_subject_combination, name='create-subjectcombination'),
    path('manage-subjectcombinations/', manage_subject_combinations, name='manage-subjectcombinations'), 
    path('add-student/', add_student, name='add-student'),
    path('manage-students/', manage_students, name='manage-students'),
    path('edit-student/<int:student_id>/', edit_student, name='edit-student'),  
    path('add-result/', add_result, name='add-result'),
    path('manage-results/', manage_results, name='manage-results'), 
    path('edit-result/<int:result_id>/', edit_result, name='edit-result'), 


]
    