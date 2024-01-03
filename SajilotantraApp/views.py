from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.decorators import login_required

# from .forms import PostForm

from Sajilotantra import settings
from SajilotantraApp.models import Event, GovernmentProfile

from .models import Notification, Guidance, GovernmentProfile, UserProfile
from .models import Post, PostComment, PostLike
from .tokens import generate_token
from django.http import Http404

def index(request):
    return render(request, 'index.html')

def signup(request):
    if request.method=="POST":
        username=request.POST.get("username")
        pass1=request.POST.get("pass1")
        fname=request.POST.get("fname")
        lname=request.POST.get("lname")
        pass2=request.POST.get("pass2")
        email=request.POST.get("email")
        print(username,pass1,pass2,fname,lname,email)

        #authentication(to check if the username and email are already taken)

        if User.objects.filter(username=username):
            messages.error(request,"The username you entered is already taken, try another username")
            return redirect("signup")
        
        if User.objects.filter(email=email):
            messages.error(request,"The email you entered is already taken, try another email")
            return redirect("signup")
        
        myuser=User.objects.create_user(username,email,pass1)#create user in the database with the details entered
        myuser.first_name=fname
        myuser.last_name=lname
        myuser.is_active=False# before the user confirms their email address, the user's account(created) will not be active.

        myuser.save()

        messages.success(request,"Your account has been successfully Created.  We have sent you a confirmation email, please click on the activation link to activate your account.")

        #Send Welcome Email
        subject="Welcome to Sajilotantra"
        message="Hello "+ str(myuser.first_name)+", \nWelcome to Sajilotantra. We have also sent you a confirmation email, please confirm your email address to activate your account.\n\n Thank You, \n Sajilotantra Team."
        from_email=settings.EMAIL_HOST_USER
        to_list=[myuser.email]
        send_mail(subject,message,from_email,to_list,fail_silently=True)#even if the email is not sent, it will not crash the website

        #Send Confirmation Email with Activation Token
        current_site=get_current_site(request)
        email_subject="Confirm your email @Sajilotantra"
        email_message=render_to_string("email_confirmation.html",{
            "name":myuser.first_name,
            "domain":current_site.domain,
            "uid": urlsafe_base64_encode(force_bytes(myuser.pk)),
            "token": generate_token.make_token(myuser)
        })
        email=EmailMessage(
            email_subject,
            email_message,
            settings.EMAIL_HOST_USER,
            [myuser.email],

        )
        email.fail_silently=True
        email.send()

        return redirect("signin")#after a successfull signup, redirect the user to sign in page

    return render(request,"signup.html")

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        remember_me = request.POST.get('remember')
        user = authenticate(request, username=username, password=pass1)
        print(username, pass1)

        # Check if user exists
        if user is None:
            messages.info(request, "Incorrect login credentials. Try again")
            return redirect('signin')

        # Login successful
        login(request, user)
        return redirect('dashboard')

    form = AuthenticationForm()
    return render(request, 'signin.html', {'form': form})


def activate(request,uidb64,token):#activate user account if the confirmation link is clicked
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser,token):
        myuser.is_active = True
        # user.profile.signup_confirmation = True
        myuser.save()
        signin(request)
        messages.success(request, "Your Account has been activated!")
        return redirect('signin')
    else:
        return render(request,'activation_failed.html')
    



     
def events(request):
    all_events = Event.objects.all()
    context = {
        "events":all_events,
    }
    return render(request,'events.html',context)

def all_events(request):
    all_events = Event.objects.all()
    out = []
    for event in all_events:
        out.append({
            'title': event.name,
            'id': event.id,
            'description': event.description,
            'start': event.start.isoformat(),  # Use isoformat() here
            'end': event.end.isoformat(),      # Use isoformat() here
        })
    return JsonResponse(out, safe=False)

    all_events = Event.objects.all()
    out = []
    for event in all_events:
        out.append({
            'title': event.name,
            'id': event.id,
            'start': event.start.strftime("%m/%d/%Y, %H:%M:%S"),
            'end': event.end.strftime("%m/%d/%Y, %H:%M:%S"),
        })
    return JsonResponse(out, safe=False)
    return render(request,'events.html')

# def map(request):
#     return render(request, 'map.html')

def dashboard(request):
    notifications = Notification.objects.all()
    guidance = Guidance.objects.all().order_by('-pk')
    posts= Post.objects.all().order_by('-pk')

    
    context = {
        'notifications': notifications,
        'guidance_items': guidance[:6],  # Fetching the first 6 guidance items
        'posts':posts,
    }

    return render(request, 'dashboard.html', context)

def card(request):
    details=Guidance.objects.all().order_by('-pk')
    context={
        'details':details
    }
    return render(request, 'guidelines_details.html',context)

def guide_blog(request,pk):
    # print(f"Guide steps function called with pk={pk} and category={category}")
    # guidance = get_object_or_404(Guidance, id=pk, category=category)
    # print(f"Guidance object retrieved: {guidance}")
    # return render(request, 'guide_steps.html', {'guidance': guidance})
   guideBlog=Guidance.objects.get(id=pk)
   blog={
    'guideBlog':guideBlog
   }
   return render(request,'guide_steps.html',blog)

def government_profiles(request):
    profiles=GovernmentProfile.objects.all().order_by('-pk')
    data={
        'profiles':profiles
    }
    return render(request, 'government_profiles.html', data)

def map(request):
    profiles=GovernmentProfile.objects.all().order_by("-pk")
    data={
        'profiles':profiles
    }
    return render(request,'map.html',data)


def government_profiles_details(request,pk):
    profiles = get_object_or_404(GovernmentProfile, profile_id=pk)
    return render(request,'government_profiles_details.html',{'GovernmentProfile':profiles})


# @login_required
def profile(request, username):
    auth_user = request.user
    print(auth_user)

    try:
        # Retrieve the user based on the provided username
        user = User.objects.get(username=username)

        if auth_user != user:
            # If they don't match, redirect to the login page
            return redirect('signin')

        if user is None:
            return render(request, "user_does_not_exist.html")

        # Retrieve or create UserProfile based on user_id
        profile, created = UserProfile.objects.get_or_create(user=user)

        # Handle profile update
        if request.method == 'POST':
            profile.bio = request.POST.get('bio', '')
            
            # Update profile picture
            if 'picture' in request.FILES:
                profile.image = request.FILES['picture']

            # Update cover photo
            if 'cover' in request.FILES:
                profile.cover = request.FILES['cover']

            profile.save()

        context = {
            'user': user,
            'auth_user': auth_user,
        }

    except User.DoesNotExist:
        raise Http404("User does not exist")

    return render(request, 'profileupdate.html', context)


def view_profile(request, username):
    user = get_object_or_404(User, username=username)
    
    try:
        profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        return render(request, 'user_does_not_exist.html')

    # if user is None:
    #     return render(request, 'user_does_not_exist.html')
    
    profile = UserProfile.objects.get(user=user)

    context = {
        'user': user,
        'profile': profile,
    }

    return render(request, 'frontprofile.html', context)


@login_required(login_url='/signin')
def create_post(request):
    if request.method == 'POST':
        caption = request.POST.get('postCaption')
        category= request.POST.get('category')
        image= request.POST.get('post-image')


        auth_user= request.user
        # Cur_user = User.objects.get(username=auth_user)
        U_profile, created = UserProfile.objects.get_or_create(user=auth_user)
        print(U_profile.pk)
        print(auth_user)
        # Check if the user is authenticated
        if isinstance(request.user, AnonymousUser):
            return render(request, 'signin.html')  # or redirect to login page

        try:
            user_profile = UserProfile.objects.get(user=U_profile.pk)
        except UserProfile.DoesNotExist as e:
            # Handle the case when the user profile does not exist
            print(f"Error: {e}")
            return render(request, 'signup.html')

        # print("USer: "+user_profile)
        
        
        post = Post.objects.create(
            user=user_profile,
            # user="demo",
            caption=caption,
            category=category,
            image=image
        )
        return redirect('dashboard')
   

    # return render(request, 'dashboard.html', {'form': form})
    return redirect('map.html')

# def create_post_new(request):
#     if request.method == 'POST':
#         form = PostForm(request.POST, request.FILES)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.user = request.user.userprofile
#             post.save()
#             return redirect('create_post.html')
#         else:
#             # Print form errors to the console for debugging
#             print(form.errors)
#     else:
#         form = PostForm()

#     return render(request, 'create_post.html', {'form': form})





