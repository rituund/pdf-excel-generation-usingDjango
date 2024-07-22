from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.student_registration, name='student_registration'),
    path('students/', views.student_list, name='student_list'),
    path('generate_excel/', views.generate_excel, name='generate_excel'),
    path('generate_pdf/', views.generate_pdf, name='generate_pdf'),
]