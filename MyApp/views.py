from django.shortcuts import render, redirect
from django.http import HttpResponse
from MyApp.models import *
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User,Group
from django import forms
from  django.contrib import messages




class registerValidations(forms.Form):  # форма для проверки, введены ли данные
    username = forms.CharField(max_length= 30)
    email = forms.EmailField()
    password = forms.CharField(min_length = 8)

class loginValidations(forms.Form):
    username = forms.CharField(max_length = 30)
    password = forms.CharField(min_length = 8)


# Create your views here.



def login_page(request):    # Авторизация
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'
        

        form = loginValidations(request.POST)

        
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
                         
        if user is None:
            messages.add_message(request, messages.ERROR, "Проверьте введённые данные")
            return render(request, 'login.html')
        login(request, user)
        return redirect('/')
        
def register(request):          #регистрация
    if request.method == 'GET':
        return render(request, "register.html")
    if request.method == "POST":
        
        form = registerValidations(request.POST)
        if not form.is_valid():
            return HttpResponse("Проверьте введённые данные")
        
        user = User()
        if User.objects.filter(username = request.POST['username']).exists():
            return HttpResponse("Имя пользователя уже занято")

        user.username = request.POST['username']
        user.set_password(request.POST['password'])
        user.email = request.POST['email']
        user.telegram = request.POST['telegram']
        
        user.save()
        login(request, user)

        return redirect('/')

def logout_page(request):   # Выход из аккаунта
    logout(request)
    return redirect('/login')







def index(request):     # Страница со списком студента
    if not request.user.is_authenticated:
        return redirect('/login')
    students = student.objects.all()
    user = request.user
    if user.groups.filter(name='admin').exists():
        return render(request , "StartStudent.html", {"students":students})
    else:
        return render(request , "StartStudentTeacher.html", {"students":students})

def details(request):       # Профиль студента
    if not request.user.is_authenticated:
        return redirect('/login')
    if request.method == 'GET':
        id = request.GET['id']
        students = student.objects.get(pk=id)
        comments = Comment.objects.filter(user_for= id)
        user = request.user
        if user.groups.filter(name='admin').exists():
            return render(request , "Students.html", {"student":students,"comments" : comments,"ticket" : ticket})
        else:
            return render (request , "StudentTeacher.html", {"student":students,"comments" : comments,"ticket" : ticket})
    if request.method == 'POST':
        user_for = student.objects.get(pk = request.GET['id'])
        user_from = request.user
        text = request.POST.get('text','')

        if text == "":
            return HttpResponse("Введите текст")
        
        comment = Comment();
        comment.text = text
        comment.user_for = user_for
        comment.user_from = user_from

        comment.save()
        return redirect('/student?id={}'.format(request.GET['id']))

def add(request):       # Создание студента
    if not request.user.is_authenticated:
        return redirect('/login')
    user = request.user
    if user.groups.filter(name='admin').exists():
        if request.method == 'GET':
            courses = Cours.objects.all()
            return render(request, "add.html",{'courses':courses})
        if request.method == 'POST':
            first_name = request.POST.get('first_name','')
            last_name = request.POST.get('last_name','')
            cours = request.POST.get('select1', '')
            email = request.POST.get('email', '')
            room = request.POST.get('room', '')
            discription = request.POST.get('discription', '')

            if first_name =="" or last_name == "" or room == "" or email == "":
                return HttpResponse("Заполните все поля")
            students = student()
            students.first_name = first_name
            students.last_name = last_name
            students.room = room
            students.email = email
            students.discription= discription
            
            if 'avatar' in request.FILES:
                students.photo = request.FILES['avatar']
            else:
                students.photo = None


            if cours != '':
                course = Cours.objects.get(pk=cours)
                students.cours = course
            else:
                students.cours = None
            
            students.save()

            return redirect('/student?id={}'.format(students.id))
    else:
        return redirect("/startstudent")
        
def edit(request):      # Изменение студента
    if not request.user.is_authenticated:
        return redirect('/login')
    user = request.user
    if user.groups.filter(name='admin').exists():
        if request.method == 'GET':
            id = request.GET['id']
            studentes = student.objects.get(pk=id)
            courses = Cours.objects.all()
            return render(request, "edit.html",{'courses':courses, 'studentes':studentes})
        if request.method == 'POST':

            first_name = request.POST.get('first_name','')
            last_name = request.POST.get('last_name','')
            cours = request.POST.get('select1', '')
            email = request.POST.get('email', '')
            room = request.POST.get('room', '')
            discription = request.POST.get('discription', '')

            id = request.GET['id']
            

            if first_name =="" or last_name == "" or room == "" or email == "":
                return HttpResponse("Заполните все поля")
            
            studentes = student.objects.get(pk=id)

            studentes.first_name = first_name
            studentes.last_name = last_name
            studentes.room = room
            studentes.email = email
            studentes.discription= discription

            if 'avatar' in request.FILES:
                studentes.photo = request.FILES.get('avatar')
            
            if cours != '':
                course = Cours.objects.get(pk=cours)
                studentes.cours = course
            else:
                student.cours = None

            studentes.save()
            return redirect('/student?id={}'.format(studentes.id))
    else:
        return redirect("/startstudent")


def delete(request):    # Удаление студента  
    if not request.user.is_authenticated:
        return redirect('/login')
    user = request.user
    if user.groups.filter(name='admin').exists():
        id = request.GET['id']
        studentes = student.objects.get(pk=id)
        studentes.delete()
        return redirect('/startstudent')
    else:
        return redirect('/startstudent')
def lobby(request):     # Начальная станица
    if not request.user.is_authenticated:
        return redirect('/login/')
    return render(request, "Lobby.html")






def indexcourse(request):   # Страница со списком курсов
    if not request.user.is_authenticated:
        return redirect('/login')
    courses = Cours.objects.all()
    user = request.user
    if user.groups.filter(name='admin').exists():
        return render(request , "StartCourse.html", {"courses":courses})
    else:
        return render(request , "StartCourseTeacher.html", {"courses":courses})

def detailscourse(request):     # Станица курса
    if not request.user.is_authenticated:
        return redirect('/login')
    id = request.GET['id']
    studentes =student.objects.filter(cours = id)
    course = Cours.objects.get(pk=id)
    user = request.user
    if user.groups.filter(name='admin').exists():
        return render(request , "Course.html", {"course":course, "studentes": studentes})
    else:
        return render(request , "CourseTeacher.html", {"course":course, "studentes": studentes})

def addcourse(request):     # Создание курса
    if not request.user.is_authenticated:
        return redirect('/login')
    user = request.user
    if user.groups.filter(name='admin').exists():
        if request.method == 'GET':
            teachers = Teacher.objects.all()
            return render(request, "addcourse.html",{'teachers':teachers})
        if request.method == 'POST':
            name = request.POST.get('name','')
            teaher = request.POST.get('select1','')

            if name =="" :
                return HttpResponse("Заполните все поля")
            course = Cours()
            course.name = name

            if teaher != '':
                teaheres = Teacher.objects.get(pk=teaher)
                course.teacher = teaheres
            else:
                course.teacher = None
            course.save()

            return redirect('/course?id={}'.format(course.id))
    else:
        return redirect('/startcourse')
        
def editcourse(request):        # Изменение курса
    if not request.user.is_authenticated:
        return redirect('/login')
    user = request.user
    group = Group.objects.filter(name='admin').first()
    if user.groups.filter(name=group).exists():
        if request.method == 'GET':
            id = request.GET['id'] 
            course =Cours.objects.get(pk=id)
            teachers = Teacher.objects.all()
            return render(request, "editcourse.html",{'course':course, 'teachers':teachers})
        if request.method == 'POST':
            name = request.POST.get('name','')
            teacher = request.POST.get('select1', '')

            id = request.GET['id']
            

            if name =="" :
                return HttpResponse("Заполните все поля")
            
            course = Cours.objects.get(pk=id)
            if teacher != '':
                teacheres = Teacher.objects.get(pk=teacher )
                course.teacher = teacheres
            else:
                course.teacher = None

            course.save()
            return redirect('/course?id={}'.format(course.id))
    else:
        return redirect("/startcoursex")
def deletecourse(request):      # Удаление курса
    if not request.user.is_authenticated:
        return redirect('/login')
    user = request.user
    if user.groups.filter(name='admin').exists():
        id = request.GET['id']
        course = Cours.objects.get(pk=id)
        course.delete()
        return redirect('/startcourse')
    else:
        return redirect('/startcourse')