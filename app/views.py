from django.shortcuts import render
from app.forms import *
from django.http import HttpResponse,HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def registration(request):
    ufo=UserForm()
    pfo=ProfileForm()
    d={'ufo':ufo,'pfo':pfo}

    if request.method=="POST" and request.FILES:
        ufd=UserForm(request.POST)  #ufo has contain only data so we'll write request.POST to collect data
        pfd=ProfileForm(request.POST,request.FILES)  #pfo includes data & files/images so we'll write both the commands

        if ufd.is_valid() and pfd.is_valid():
            #by default commit is true we'll make it false for making unmodifiable obj to Modifiable(MUFDO)
            MUFDO=ufd.save(commit=False)
            pw=ufd.cleaned_data['password'] #we need to modify password so we'll send data directly
            MUFDO.set_password(pw) #we need to encrypt the password son we use User's buitl-in method
            MUFDO.save() #save it to the database

            #we need to modify the profile becoz it required 3 columns data so provide it from the userobject
            MPFDO=pfd.save(commit=False)
            MPFDO.username=MUFDO #we need username  column data get it from the lastly saved userobj
            MPFDO.save()

            #Sending mail to the register users
            send_mail('Registration',
            'Thank you for Registering. your Registration is Successful.',
            'sravanisravya772@gmail.com',
            [MUFDO.email],
            fail_silently=True,
            )

            return HttpResponse('Registration is successfull')
        else:
            return HttpResponse('Invalid Data')


    return render(request,'registration.html',d)



def user_login(request):
    if request.method=='POST':
        username=request.POST['un']
        passw=request.POST['pw']
        AUO=authenticate(username=username,password=passw)
        if AUO and AUO.is_active:
            login(request,AUO)
            request.session['username']=username
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponse('Invalid creditials')

    return render(request,'user_login.html')



def home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'home.html',d)

    return render(request,'home.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


@login_required
def profile_display(request):
    un=request.session.get('username')
    UO=User.objects.get(username=un)
    PO=Profile.objects.get(username=UO)
    d={'UO':UO,'PO':PO}
    return render(request,'profile_display.html',d)


@login_required
def change_password(request):
    if request.method=='POST':
        pw=request.POST['pw']
        un=request.session.get('username')
        UO=User.objects.get(username=un)
        UO.set_password(pw)
        UO.save()
        return HttpResponse('password changed successfully')
    return render(request,'change_password.html')



def forget_password(request):
    if request.method=='POST':
        un=request.POST['un']
        pw=request.POST['pw']
        LUO=User.objects.filter(username=un)
        if LUO:
            UO=LUO[0]
            UO.set_password(pw)
            UO.save()
            return HttpResponse('paassword')
        else:
            return HttpResponse('not valid user')
    return render(request,'forget_password.html')