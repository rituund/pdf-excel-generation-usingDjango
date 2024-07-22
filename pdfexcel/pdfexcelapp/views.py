# pdfexcelapp/views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Student, Course
from .forms import StudentForm
import openpyxl
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def student_registration(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            if is_ajax(request):
                return JsonResponse({'message': 'Student registered successfully!'})
            return redirect('student_list')
        else:
            if is_ajax(request):
                return JsonResponse({'errors': form.errors}, status=400)
    else:
        form = StudentForm()
    return render(request, 'pdfexcelapp/register.html', {'form': form})

def student_list(request):
    students = Student.objects.all()
    return render(request, 'pdfexcelapp/student_list.html', {'students': students})

def generate_excel(request):
    students = Student.objects.all()
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(['ID', 'Name', 'Email', 'Courses'])
    for student in students:
        courses = ", ".join([course.name for course in student.courses.all()])
        ws.append([student.id, student.first_name, student.email, courses])
    
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=students.xlsx'
    wb.save(response)
    return response

def generate_pdf(request):
    students = Student.objects.all()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=students.pdf'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # Define column positions
    col_id = 50
    col_name = 100
    col_email = 200
    col_courses = 400

    y = height - 40
    p.setFont("Helvetica", 12)
    p.drawString(col_id, y, "ID")
    p.drawString(col_name, y, "Name")
    p.drawString(col_email, y, "Email")
    p.drawString(col_courses, y, "Courses")

    for student in students:
        y -= 20
        courses = ", ".join([course.name for course in student.courses.all()])
        p.drawString(col_id, y, str(student.id))
        p.drawString(col_name, y, student.first_name)
        p.drawString(col_email, y, student.email)
        p.drawString(col_courses, y, courses)

    p.showPage()
    p.save()
    return response
