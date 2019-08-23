from django.shortcuts import render, HttpResponse, redirect
from apps.the_wall_app.models import *
from django.contrib import messages
import bcrypt

def index(request):
    # return HttpResponse("index route")
    return render(request, 'the_wall_app/index.html')

# register - POST : validate registration information (come back or go to /wall)
def register(request) :
    errors = User.objects.validator(request.POST)
    print ("**errors: ", errors)
    if (len(errors) > 0) :
        for key, value in errors.items():
            # messages.error(request, value)
            messages.add_message(request, messages.ERROR, value, extra_tags='register')
        # messages.error(request, errors)
        temp_inputs={"first_name":request.POST['first_name'],
                    "last_name":request.POST['last_name'],
                    "email":request.POST['email'], 
                    "birthday":request.POST['bday']}
        request.session['temp_inputs'] = temp_inputs
        return redirect('/')
        
    else :
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user = User.objects.create(first_name=request.POST['first_name'], 
                            last_name=request.POST['last_name'],
                                email=request.POST['email'], 
                                password=hashed_pw,
                                birthday=request.POST['bday'])
        messages.success(request, "User succesfully registered")
        request.session['user_id'] = user.id
        request.session['user_fname'] = user.first_name
        return redirect('/wall')
    # return HttpResponse("register route")

# login - POST : validate user information (come back or go to /wall)
def login(request) :
    email = request.POST['login_email']
    try :
        user = User.objects.get(email=email)
        if bcrypt.checkpw(request.POST['login_pw'].encode(), user.password.encode()) :
            print ("here")
            request.session['user_id'] = user.id
            request.session['user_fname'] = user.first_name
            messages.add_message(request, messages.SUCCESS, 'Successfully logged in!')
            return redirect('/wall')
        else :
            messages.add_message(request, messages.ERROR, 'Invalid user information - not correct password', extra_tags='login')
    except :
        messages.add_message(request, messages.ERROR, 'Invalid user information', extra_tags='login')
    return redirect('/')
    # return HttpResponse("login route")

# wall - html
def wall(request) :
    if not 'user_id' in request.session :
        messages.add_message(request, messages.ERROR, 'You should login first', extra_tags="no_login")
        return redirect('/')
    # all messages
    all_messages = Message.objects.all()
    context = {"all_messages":all_messages}
    return render(request, 'the_wall_app/wall.html', context)

# post_message
def post_message(request) :
    user_id = request.session['user_id']
    message = Message.objects.create(
                content=request.POST['message'],
                user = User.objects.get(id=user_id)
            )
    return redirect('/wall')

# delete_comment
def delete_comment(request, comment_id) :
    comment = Comment.objects.get(id=comment_id)
    comment.delete()
    return redirect('/wall')

# post_comment
def post_comment(request, message_id) :
    comment = Comment.objects.create(
                content = request.POST['comment'],
                user = User.objects.get(id=request.session['user_id']),
                message = Message.objects.get(id=message_id)
                )
    return redirect('/wall')

# log_out - clear session and redirect
def logout(request) :
    request.session.clear()
    return redirect('/')