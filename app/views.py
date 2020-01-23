from django.shortcuts import render, redirect
from .models import User, PostMessage, Comment
from django.contrib import messages
import bcrypt

# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
    errors = User.objects.registration_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        pass_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        create_user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], pw_hash=pass_hash)
        request.session['user_id'] = create_user.id
        return redirect('/wall')
        # return redirect('/success')


def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')

    found_user = User.objects.filter(email=request.POST['email'])
    print('%'*100)
    print(len(found_user))
    print(found_user)
    if len(found_user) > 0:
        user_from_db = found_user[0]

        is_pw_correct = bcrypt.checkpw(request.POST['password'].encode(), user_from_db.pw_hash.encode())
        if is_pw_correct:
            request.session['user_id'] = user_from_db.id
            return redirect('/wall')
            # return redirect('/success')
    messages.error(request, "Invalid credentials.")
    return redirect('/')

def wall(request):                              # def success(request):
    user_id = request.session.get('user_id')
    if user_id is None:
        return redirect("/")

    user_id = request.session.get('user_id')
    if user_id is None:
        messages.error(request, "Please login or register.")
        return redirect('/')

    context = {
        'user': User.objects.get(id=user_id),
        'postmessages': PostMessage.objects.all()
    }
    return render(request,'wall.html',context)                  # return render(request,'success.html',context)

def logout(request):
    request.session.clear()
    return redirect('/')

def post_message(request):
    user_id = request.session.get('user_id')
    if user_id is None:
        return redirect("/")

    errors = PostMessage.objects.postmessage_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/wall')
    else:
        user_from_db = User.objects.get(id=request.session['user_id'])          ## first find the user
        create_posted_message = PostMessage.objects.create(posted_message=request.POST['postmessage'],user_message=user_from_db)
        return redirect('/wall')

def comment(request,id):
    user_id = request.session.get('user_id')
    if user_id is None:
        return redirect("/")

    errors = Comment.objects.comment_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/wall')
    else:
        user_from_db = User.objects.get(id=request.session['user_id'])
        message_from_db = PostMessage.objects.get(id=id)
        create_posted_comment = Comment.objects.create(posted_comment=request.POST['comment'],user_comment=user_from_db,posted_message=message_from_db)
        return redirect('/wall')

def delete(request,id):
    user_id = request.session.get('user_id')
    if user_id is None:
        return redirect("/")

    comment = Comment.objects.get(id=id)
    comment.delete()
    return redirect('/wall')

def deletemsg(request,id):
    user_id = request.session.get('user_id')
    if user_id is None:
        return redirect("/")

    message = PostMessage.objects.get(id=id)
    message.delete()
    return redirect('/wall')