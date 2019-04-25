from django.shortcuts import render, redirect,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from .models import person
import random
import ctypes 
import win32api

fname=""
lname=""
mobile=""
otpp=0 #global random generator
otppp=0
def Register_form(request):
    from pages.namer import otp
    global fname
    global lname
    global mobile
    fname= request.POST["fname"]
    lname= request.POST["lname"]
    mobile= request.POST["mobile"]
    already_present=person.objects.filter(mobile_number=mobile)
    if(already_present):
        win32api.MessageBox(0, 'Mobile No. already present!!', 'WARNING!!', 0x00001000)
        return render(request,"about.html",{})
    global otpp
    otpp=random.randrange(100000,999999,1)	
    return render(request, "Enter_otp.html",{})
#"my_stuff": otp('koAO45zCako-DZtRg5E2TJcHZu0Jc3xjeOdDGvSNPO', mobile,'TXTLCL', otpp)
def Otp_validation(request):
    from pages.namer import dataset_generator
    otp_valid= request.POST["otp_valid"]
    if(otp_valid=="786"):
        y=fname+str(random.randrange(100000,999999,1))
        win32api.MessageBox(0, "Your user-id is "+ y +". Please make a note of it as this will be used in future for logging in. ", "SUCCESS!!", 0x00001000)
        p=person(first_name=fname,last_name=lname,mobile_number=mobile,user_id=y)
        p.save()      
        return render(request,"home.html",{"generate": dataset_generator(mobile)})
    else:
        win32api.MessageBox(0, "Wrong OTP entered!!!", "WARNING!", 0x00001000)
        return render(request,"about.html",{})
    
def Otp_validation1(request):
    otp_valid1= request.POST["otp_valid1"]
    if(otp_valid1=="786"):
        win32api.MessageBox(None, "Successfully logged in.", "SUCCESS!", 0x00001000)
        return HttpResponseRedirect('http://localhost:8000/page2',)
    else:
        win32api.MessageBox(0, "Wrong OTP entered. Please try again...", "FAILURE!!!", 0x00001000)
        return render(request,"home.html",{})       

def home(request):
    return render(request,"home.html",{})

def home1(request):
    from pages.namer import face_detector,otp
    idf= request.POST["cat"] 
    per=person.objects.filter(user_id=idf)
    if(per):  
        mob_id=face_detector()
        if(mob_id!="0"):
            perr=str(per)
            perrr=perr.split(":")
            perrrr=perrr[1].split(">")
            global otppp
            otppp=random.randrange(100000,999999,1)	
            return render(request, "Enter_otp1.html",{}) 
        
        else:
            win32api.MessageBox(0, "Face not matched!!!. Try again...", "WARNING!", 0x00001000)
            return render(request, "home.html",{})    
    else:
        win32api.MessageBox(0, "Enter correct User-id!!!", "WARNING!", 0x00001000)
        return render(request, "home.html",{})   
 #"my_stuff": otp('koAO45zCako-DZtRg5E2TJcHZu0Jc3xjeOdDGvSNPO', perrrr[0],'TXTLCL', otppp)       

def about(request):
	return render(request,"about.html",{})

def Enter_otp(request):
	return render(request,"Enter_otp.html",{})

def Enter_otp1(request):
	return render(request,"Enter_otp1.html",{})
