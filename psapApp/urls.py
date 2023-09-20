from django.contrib import admin
from django.urls import path
from psapApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('university_login/', views.university_login, name='university_login'),
    #     path('university/logout/', views.university_logout, name='university_logout'),
    # Replace 'index' with your actual view for 'index.html'
    path('', views.index, name='index'),
    path('uniOrStd/', views.uniOrStd, name='uniOrStd'),
    path('student_registration/', views.student_registration,
         name='student_registration'),
    path('registerasUniPage/', views.registerasUniPage, name='uni'),
    path('loginasUni/', views.loginasUni, name='loginasUni'),
    path('student_login/', views.student_login, name='student_login'),
    path('loginasStd/', views.loginasStd, name='loginasStd'),
    path('registerasStd/', views.registerasStd, name='registerasStd'),
    #     path('registerasUni/', views.registerasUni, name='registerasUni'),
    path('stdHome/', views.stdHome, name='stdHome'),
    path('stdNewApplication/', views.stdNewApplication, name='stdNewApplication'),
    path('stdApplied/', views.stdApplied, name='stdApplied'),
    #     path('stdRegistrationForm/', views.stdRegistrationForm,
    #     name='stdRegistrationForm'),
    path('uniHome/', views.uniHome, name='uniHome'),
    path('uniNewAdmissions/', views.uniNewAdmissions, name='uniNewAdmissions'),
    path('uniRegistrationForm/', views.uniRegistrationForm,
         name='uniRegistrationForm'),
    path('uniUpdateForm/', views.uniUpdateForm, name='uniUpdateForm'),
    path('stdUpdateForm/', views.stdUpdateForm, name='stdUpdateForm'),
    path('announce_admissions/', views.announce_admissions,
         name='announce_admissions'),
    path('stdApplyAdmission/', views.apply_admission, name='stdApplyAdmission'),
    path('delete-merit/<int:merit_id>/', views.delete_merit_data, name='delete_merit_data'),
    
#     path('download_merit_list/<str:department>/', views.download_merit_list, name='download_merit_list'),
    path('download_merit_list/<str:university_name>/<str:department>/', views.download_merit_list, name='download_merit_list'),
      path('submit/', views.submit_testimonial, name='submit_testimonial'),
    

    #     path('apply_admissionSaveIntoTable/', views.apply_admissionSaveIntoTable,
    #     name='apply_admissionSaveIntoTable'),

]
