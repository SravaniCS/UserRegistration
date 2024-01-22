from django.shortcuts import render
from app.forms import *
from django.http import HttpResponse

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
            return HttpResponse('Registration is successfull')
        else:
            return HttpResponse('Invalid Data')


    return render(request,'registration.html',d)