from django.shortcuts import render, redirect
from django.contrib.auth import logout
import firebase


config = { 
   'apiKey': "AIzaSyALZPh3aSkY3nh_J6xDVUOBtIqKcaY4VTc",
   'authDomain': "django1-project.firebaseapp.com",
   "databaseURL": "https://django1-project-default-rtdb.firebaseio.com/",
    'projectId': "django1-project",
   'storageBucket': "django1-project.appspot.com",
   'messagingSenderId': "137756756811",
   'appId': "1:137756756811:web:02041d586e745bf4a836ce",
}



firebases = firebase.initialize_app(config)

# set up database
db = firebases.database()

auth = firebases.auth()



def sign_in(request):
    return render(request, 'log/signin.html')


def post_logged(request):
    email = request.POST.get('email')
    passw = request.POST.get('pass')

    try:
        user = auth.sign_in_with_email_and_password(email, passw)
    except:
        message = "invalid cres"
        return render(request, 'log/signin.html')
    print(user)

    # request session and after session you put logout in check
    session_id=user['idToken']
    request.session['uid']=str(session_id)
    return render(request, 'log/welcome.html', {'e': email})

def signup(request):
    return render(request, 'log/signup.html')


def post_signup(request):
    name=request.POST.get('name')
    email=request.POST.get('email')
    passw=request.POST.get('pass')

    # Create new user and sign in
    try:
        user=auth.create_user_with_email_and_password(email, passw)
        # Send the account creation confirmation email
        firebase.auth().send_email_verification(user)
    except:
        message="Unable to create new account try"
        return redirect('sign-up', {'message': message})

    uid = user['localId']

    # data = {"name": name, "status": 1}

    # Data to save in database
    data = {
        "name": name,
        "email": user.get('email')
    }

    # Store data to Firebase Database
    db.child("users").push(data, user.get('idToken'))
    return redirect('sign')

def create(request):
    return render(request, 'log/create.html')


def post_create(request):
    import time
    from datetime import datetime, timezone
    import pytz

    tz=pytz.timezone('Africa/Ghana')
    time_now=datetime.now(timezone.utc).astimezone(tz)
    millis = int(time.mktime|(time_now.timetuple()))
    work = request.POST.get('work')
    progress=request.POST.get('progress')

   

    idToken = request.session['uid']
    a = auth.get_account_info(idToken)
    a = dict(list(a.items())[1:2])
    print(a)
    
    data = {
        "work":work,
        "progress":progress
    }


    return render(request, 'log/welcome.html')

def post_create(request):
    return render(request, 'log/welcome.html')

def logout(request):
    # logout(request)
    try:
        del request.session['uid']
    except:
        KeyError
        pass
    return redirect('sign')



def reset(request):
	return render(request, "log/reset.html")

def postReset(request):
	email = request.POST.get('email')
	try:
		auth.send_password_reset_email(email)
		message = "A email to reset password is successfully sent"
		return render(request, "log/reset.html", {"msg":message})
	except:
		message = "Something went wrong, Please check the email you provided is registered or not"
		return render(request, "log/reset.html", {"msg":message})


def firebase_facebook(request):
    #  auth = firebase.auth(client_secret="c2f4b099f7a5eb5ab00927c9e0a34bc5")
    #  auth.authenticate_login_with_facebook()

     CLIENT_SECRET = { "web": { 
                             "client_id": "1693469637779315", 
                             "client_secret": "c2f4b099f7a5eb5ab00927c9e0a34bc5",
                             "redirect_uris": ["https://xxx.firebaseapp.com/__/auth/handler"]
                             }
                    }
     
    #  auth = auth(client_secret=CLIENT_SECRET)
     return auth.authenticate_login_with_facebook(client_secret=CLIENT_SECRET)

def create_social_auth(request):
     
     auth.create_authentication_uri()