from django.urls import path, include
from .import views
from django.contrib.auth.views import LogoutView,LoginView

urlpatterns = [
    path('', views.login_user, name="login"),
    path('registerpage/', views.registerpage, name="registerpage"),
    path('registeradmin/', views.registeradmin, name="registeradmin"),
    path('registerstudent/', views.registerstudent, name="registerstudent"),
    path('changepassword/', views.changepassword, name="changepassword"),
    path('studentchangepassword/', views.studentchangepassword, name="studentchangepassword"),
    path('logout/', LogoutView.as_view(template_name= "admin1/logout.html"),name='logout'),
    
    
    path('dashboard/', views.dashboard, name="dashboard"),
    
    
    
    # * Student
    path('studentdashboard/', views.studentdashboard, name="studentdashboard"),
    path('profilestudent/', views.profilestudent, name="profilestudent"),
    path('studentposition/', views.studentposition, name="studentposition"),
    path('student/', views.student, name="student"),
    path('updatestudent/<str:pk>/', views.updatestudent, name="updatestudent"),
    path('deletestudent/<str:pk>/', views.deletestudent, name="deletestudent"),
    path('studentcandidate/', views.studentcandidate, name="studentcandidate"),
    path('vote/', views.vote, name="vote"),
    path('viewresult/<str:pk>/', views.viewresult, name="viewresult"),
    path('viewvoters/<str:pk>/', views.viewvoters, name="viewvoters"),
    path('stuvote/<str:pk>/', views.stuvote, name="stuvote"),
    
    
    
    
    # * Position
    path('newposition/', views.newposition, name="newposition"),
    path('profileposition/', views.profileposition, name="profileposition"),
    path('position/', views.position, name="position"),
    path('deleteposition/<str:pk>/', views.deleteposition, name="deleteposition"),
    
    
    # * Candidate
    path('newcandidate/', views.newcandidate, name="newcandidate"),
    path('candidate/', views.candidate, name="candidate"),
    path('profilecandidate/', views.profilecandidate, name="profilecandidate"),
    path('deletecandidate/<str:pk>/', views.deletecandidate, name="deletecandidate"),
    
    
    # * Votes
    path('votes/', views.votes, name='votes'),
    path('votesreset/', views.votesreset, name='votesreset'),
    path('profilevotes/', views.profilevotes, name='profilevotes'),
    path('result/<str:pk>/', views.result, name='result'),


]