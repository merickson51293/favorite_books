from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import *

def index(request):
    return render(request, "index.html")

def main(request):
    context={
        'all_books':Book.objects.all(),
        'this_user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, "main.html", context)

def user_page(request, user_id):
    context={
        'user': User.objects.get(id=user_id)
    }
    return render(request, "user.html", context)

def register(request):
    if request.method=="POST":
        errors=User.objects.validator(request.POST)
        if errors:
            for error in errors:
                messages.error(request, errors[error])
            return redirect('/')
        user_pw=request.POST['password']
        hash_pw=bcrypt.hashpw(user_pw.encode(), bcrypt.gensalt()).decode()
        new_user=User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=hash_pw)
        request.session['user_id']=new_user.id
        request.session['user_name']=f"{new_user.first_name} {new_user.last_name}"
        return redirect("/main")
    return redirect('/')

def login(request):
    if request.method=="POST":
        errors=User.objects.login_validator(request.POST)
        if errors:
            for error in errors:
                messages.error(request, errors[error])
            return redirect('/')
        logged_user=User.objects.filter(email=request.POST['email'])
        if logged_user:
            logged_user=logged_user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['user_id']=logged_user.id
                request.session['user_name']=f"{logged_user.first_name} {logged_user.last_name}"
                return redirect('/main')
    return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')

def favorite(request, book_id):
    user = User.objects.get(id=request.session["user_id"])
    book = Book.objects.get(id=book_id)
    user.favorited_books.add(book)

    return redirect(f'/book/{book_id}')

def unfavorite(request, book_id):
    user = User.objects.get(id=request.session["user_id"])
    book = Book.objects.get(id=book_id)
    user.favorited_books.remove(book)

    return redirect(f'/book/{book_id}')

def add_book(request):
    user=User.objects.get(id=request.session['user_id'])
    book = Book.objects.create(title=request.POST['title'], desc=request.POST['desc'], person=user)
    user.favorited_books.add(book)
    return redirect('/main')

def book(request, book_id):
    context={
        'one_book':Book.objects.get(id=book_id),
        'current_user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, "book_page.html", context)

def delete(request, book_id):
    book=Book.objects.get(id=book_id)
    book.delete()
    return redirect('/main')

def edit(request, book_id):
    edit = Book.objects.get(id=book_id)
    edit.desc = request.POST['desc']
    edit.save()
    return redirect(f'/book/{book_id}')

