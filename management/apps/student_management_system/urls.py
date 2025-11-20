from django.urls import path
from .views import *


urlpatterns = [
    path('create-student/', create_student, name='create_student'),
    path('all-student/', all_student, name='all_student'),
    path('student-details/<int:std_id>/', student_details, name='student_details'),
    path('subject-create/', subject_create, name='subject_create'),
    path('all-subject/', all_subject, name='all_subject'),
    path('result-create/', result_create, name='result_create'),
    path('result-list/', result_list, name='result_list'),
    path('get-student-by-roll/', get_student_by_roll, name='get_student_by_roll'),
]
