from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.subject_courses_list, name='index'),
    path('courses', views.courses_list, name='courses_list'),
    path('subjects', views.subjecta_list, name='subjects_list'),
    path('course/<slug:slug>/', views.courses_details, name='course_details'),
    path('add-course', views.add_course, name='add_coures'),
    path('edit-course/<slug:slug>',views.edit_course, name='edit_course'),
    path('delete-course/<slug:slug>', views.delete_course, name='delete_course'),
    path('course/<slug:slug>/add-module/',views.add_module, name='add_module'),
    path('course/<slug:slug>/edit-module/',views.edit_module, name='edit_module'),
    path('course/<int:pk>/delete-module/', views.delete_module, name='delete_module'),
    path('enroll-course/<slug:slug>/', views.enroll_course, name='enroll_course'),
    path('unenroll-course/<slug:slug>/', views.unenroll_course, name='unenroll_course'),
]
