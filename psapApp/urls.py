from .views import ongoing_admissions
from .views import get_campuses, get_programs, get_test_required
from .views import get_campuses
from .views import get_test_required
from .views import get_programs, get_departments
from .views import get_programs, get_departments
from django.contrib import admin
from django.urls import path
from psapApp import views
from .views import get_programs, get_departments, get_test_required, get_department_details
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
    

    path('download_merit_list/<str:university_name>/<str:department>/<str:start_date>/',
         views.download_merit_list, name='download_merit_list'),
      path('submit/', views.submit_testimonial, name='submit_testimonial'),
    path('close_admission/<int:admission_id>/',
         views.close_admission, name='close_admission'),
    

    path('ongoing/', views.ongoing_admissions, name='ongoing_admissions'),
    # AJAX endpoint to get programs for a selected university
    path('get_programs/', get_programs, name='get_programs'),

    # AJAX endpoint to get departments for a selected university and program
    path('get_departments/', get_departments, name='get_departments'),

    # AJAX endpoint to get campuses for a selected university
    path('get_campuses/', views.get_campuses, name='get_campuses'),
    # AJAX endpoint to get test required for a selected university
    path('get_test_required/', get_test_required, name='get_test_required'),
    path('get_department_details/', get_department_details,
         name='get_department_details'),

]
