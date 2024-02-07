from django.shortcuts import render, reverse, redirect
from .models import *
from users.models import User
from .forms import *
from .decorators import *
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib.auth.decorators import login_required,user_passes_test


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def registerpage(request):
    return render(request, 'admin1/registerpage.html')

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def registeradmin(request):
    form = UserForm()
    if request.method =='POST':
        form = UserForm(request.POST)
        userid = request.POST.get('userid')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if User.objects.filter(userid=userid):
            messages.error(request, "Staff_ID already exists")
            return redirect('registeradmin')
        if password1 != password2:
            messages.error(request, "Incorrect password")
            return redirect('registeradmin')
        if form.is_valid():
            user= form.save()
            name = form.cleaned_data.get('first_name')
            group= Group.objects.get(name='admin')
            user.groups.add(group)  
            messages.success(request, 'Admin Account has been created for ' + name)
            return redirect('registerpage')
    context = {'form':form}
    return render(request, 'admin1/registeradmin.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def registerstudent(request):
    form = UserForm1()
    if request.method =='POST':
        form = UserForm1(request.POST)
        first_name = request.POST.get('first_name')
        userid = request.POST.get('userid')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if User.objects.filter(userid=userid):
            messages.error(request, "Matric_no already exists")
            return redirect('registerstudent')
        if password1 != password2:
            messages.error(request, "Incorrect password")
            return redirect('registerstudent')
        
        if form.is_valid():
            user= form.save()
            name = form.cleaned_data.get('first_name')
            group= Group.objects.get(name='student')
            user.groups.add(group)
        
            Student.objects.create(
                user=user,
                name=first_name,
                matric_no=user.userid,
                email=user.email,
                faculty=user.faculty,
                phone=user.phone,
                level=user.level,
                department=user.department
                
            )
            messages.success(request, 'Student account has been created for ' + name)
            return redirect('registerstudent')
    context = {'form':form}
    return render(request, 'admin1/registerstudent.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def changepassword(request):
    
    form = PasswordChangeForm(user=request.user, data=request.POST)
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        oldpassword = request.POST.get('old_password')
        password1 = request.POST.get('new_password1')
        password2 = request.POST.get('new_password2')
        if password1 != password2:
            messages.error(request, "Incorrect password")
            return redirect('changepassword')   
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Password has been changed successfully')
            return redirect('dashboard')
    context={'form':form}
    return render(request, 'admin1/changepassword.html', context)

@login_required(login_url='login')
@allowed_users1(allowed_roles=['student'])
def studentchangepassword(request):
    form = PasswordChangeForm(user=request.user, data=request.POST)
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
    if form.is_valid():
        form.save()
        update_session_auth_hash(request, form.user)
        messages.success(request, 'Password has been changed successfully')
        return redirect('dashboard')
    context={'form':form}
    return render(request, 'admin1/studentchangepassword.html', context)


def is_admin(user):
    return user.groups.filter(name='admin').exists()
def is_student(user):
    return user.groups.filter(name='student').exists()


def login_user(request):
    if request.method == "POST":
        userid = request.POST['userid']
        password = request.POST['password']
        user = authenticate(userid=userid, password=password)
        if user is not None:
            login(request, user)
        if is_student(request.user):      
            return redirect('studentdashboard')
        if is_admin(request.user):      
            return redirect('dashboard')
        else:
            messages.error(request, "invalid login value")
            return redirect('login')
    return render(request, "admin1/loginpage.html")


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def dashboard(request):
    stu=Student.objects.all().count()
    pos=Position.objects.all().count()
    can=Candidate.objects.all().count()
    context={'stu':stu,'pos':pos,'can':can}
    return render(request, 'admin1/dashboard.html',context)

@login_required(login_url='login')
@allowed_users1(allowed_roles=['student'])
def profilestudent(request):
    user=User.objects.get(id=request.user.id)
    stu=Student.objects.filter(user=user)
    context={'stu':stu}
    return render(request, 'admin1/profilestudent.html',context)

@login_required(login_url='login')
@allowed_users1(allowed_roles=['student'])
def studentposition(request):
    pos=Position.objects.all()
    context={'pos':pos}
    return render(request, 'admin1/studentposition.html',context)


@login_required(login_url='login')
@allowed_users1(allowed_roles=['student'])
def studentcandidate(request):
    can=Candidate.objects.all()
    context={'can':can}
    return render(request, 'admin1/studentcandidate.html',context)

@login_required(login_url='login')
@allowed_users1(allowed_roles=['student'])
def vote(request):
    can=Candidate.objects.all()
    context={'can':can}
    return render(request, 'admin1/vote.html',context)




@login_required(login_url='login')
@allowed_users1(allowed_roles=['student'])
def stuvote(request,pk):
    status=Student.objects.filter(voted=True)
    if status:
        messages.info(request, 'You cannot vote twice.')
        return redirect('vote')
    can=Candidate.objects.get(id=pk)
    can1=Candidate.objects.filter(id=pk)
    pos=can1[0].position
    name=can1[0].student
    stu=Student.objects.get(user_id=request.user.id)
    stu1=Student.objects.filter(user_id=request.user.id)
    
    Votes.objects.create(
        candidate=name,
        position=pos,
        voter=stu,
    )
    
    stu1.update(
        voted=True
        )
    messages.success(request, "Your vote has been successfullly casted to " + str(can))
    return redirect('vote')
    
    

@login_required(login_url='login')
@allowed_users1(allowed_roles=['student'])
def studentdashboard(request):
    context={}
    return render(request, 'admin1/studentdashboard.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def student(request):
    groups=Group.objects.get(name='student')
    stu=User.objects.filter(groups=groups)
    context={'stu':stu}
    return render(request, 'admin1/student.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updatestudent(request,pk):
    user=User.objects.get(id=pk)
    try:
        student=Student.objects.filter(user=user)
    except ObjectDoesNotExist:
        return redirect('student')
    
    form = StudentForm(instance=user)
    if request.method == 'POST':
       form =  StudentForm(request.POST,instance=user)
       if form.is_valid():
           form=form.save(commit=False)
           form.save()
           
           student.update(
                user=user,
                name=user.first_name,
                matric_no=user.userid,
                email=user.email,
                faculty=user.faculty,
                phone=user.phone,
                level=user.level,
                department=user.department
                
            )
           
           messages.success(request, 'Updated Successfully')
           return redirect('student')
    context={'form':form}
    return render(request, 'admin1/updatestudent.html',context)
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deletestudent(request,pk):
    user=User.objects.get(id=pk)
    stu=Student.objects.get(user=user)
    user.delete()
    stu.delete()
    messages.success(request, 'Student has been deleted') 
    return redirect('student')


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def position(request):
    context={}
    return render(request, 'admin1/position.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def newposition(request):
    form=PositionForm()
    if request.method == 'POST':
        form=PositionForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.save()
            messages.success(request, "New Position Created")
            return redirect('position')
        else:
            messages.error(request, "Form errors")
            return redirect('newposition')
    context={'form':form}
    return render(request, "admin1/newposition.html", context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def profileposition(request):
    pos=Position.objects.all()
    context={'pos':pos}
    return render(request, "admin1/profileposition.html", context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteposition(request,pk):
    pos=Position.objects.get(id=pk)
    pos.delete()
    messages.success(request, 'position has been deleted') 
    return redirect('profileposition')



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def newcandidate(request):
    form=CandidateForm()
    if request.method == 'POST':
        form=CandidateForm(request.POST,request.FILES,)
        if form.is_valid():
            form = form.save(commit=False)
            student=Student.objects.get(id=request.POST.get('studentID'))
            position=Position.objects.get(id=request.POST.get('positionID'))
            form.student=student
            form.position=position
            form.save()
            messages.success(request, "Candidate has been added to the list")
            return redirect('candidate')
        else:
            messages.error(request, "Form errors")
            return redirect('newcandidate')
    context={'form':form}
    return render(request, "admin1/newcandidate.html", context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def candidate(request):
    context={}
    return render(request, 'admin1/candidate.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def profilecandidate(request):
    can=Candidate.objects.all()
    context={'can':can}
    return render(request, 'admin1/profilecandidate.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deletecandidate(request,pk):
    can=Candidate.objects.get(id=pk)
    can.delete()
    messages.success(request, 'Candidate has been Removed') 
    return redirect('profilecandidate')

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def votes(request):
    vot=Votes.objects.all()
    count=vot.count()
    context={'count':count}
    return render(request, 'admin1/votes.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def profilevotes(request):
    pos=Position.objects.all()
    context={'pos':pos}
    return render(request, 'admin1/profilevotes.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def result(request,pk):
    pos=Position.objects.get(id=pk)
    vot=Votes.objects.filter(position=pos).count()
    can=Candidate.objects.filter(position=pk)
    context={'vot':vot,'can':can}
    return render(request, 'admin1/result.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def viewresult(request,pk):
    can=Candidate.objects.get(id=pk)
    can1=Candidate.objects.filter(id=pk)
    pos=can1[0].position
    vot=Votes.objects.filter(candidate=can).count()
    pos1=Votes.objects.filter(position=pos).count()
    if vot and pos1 !=0:
        cent=(vot/pos1)*100
    else:
        cent=0
    context={'vot':vot,'can':can,'pos1':pos1,'cent':cent}
    return render(request, 'admin1/viewresult.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def viewvoters(request,pk):
    can=Candidate.objects.get(id=pk)
    can1=Candidate.objects.filter(id=pk)
    pos=can1[0].position
    vot=Votes.objects.filter(position=pos,candidate=can)
    votcount=vot.count()
    context={'vot':vot,'can':can,'votcount':votcount}
    return render(request, 'admin1/viewvoters.html',context)





@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def votesreset(request):
    Votes.objects.all().delete()
    Student.objects.all().update(voted=False)
    messages.success(request, "All votes has been reset")
    return redirect('votes')


