from django.urls import path
from . import views


app_name = 'hackathonguild'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:post_id>/', views.post_detail, name='post_detail'),
    path('make_post/', views.make_post, name='make_post'),
    path('submit_post/', views.submit_post, name='submit_post'),
    path('<int:post_id>/join/', views.join_to_project, name='join'),
    path('<int:post_id>/delete/',views.delete_POST, name='delete'),
    path('accept_participant/<token>/', views.accept_participant, name='accept_participant'),
]
