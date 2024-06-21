from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # path('', views.dashboard, name="dashboard"),
    path('DoctorProfile/', views.DoctorProfile, name="DoctorProfile"),
    path('DoctorSignUp/', views.registerDoctor, name="DoctorSignUp"),
    path('DoctorLogin/', views.DoctorLogin, name="DoctorLogin"),
    path('DoctorLogout/', views.DoctorLogout, name="DoctorLogout"),
    path('BrowseDoctors/', views.BrowseDoctors, name="BrowseDoctors"),
    path('DoctorDetail/<int:pk>', views.DoctorDetail, name="doctor_detail"),


    path('Posts/', views.PostList, name='post_list'),
    path('Posts/MyPosts', views.MyPosts, name='my_posts'),
    path('Posts/PostDetail/<int:post_id>/', views.PostDetail, name='post_detail'),
    path('Posts/CreatePost/', views.CreatePost, name='create_post'),
    path('Posts/EditPost/<int:post_id>/', views.EditPost, name='edit_post'),
    path('Posts/DeletePost/<int:post_id>/', views.DeletePost, name='delete_post'),

]