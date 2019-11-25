from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
	path('post/<int:pk>/', views.post_detail, name='post_detail'),
	path('post/new/', views.post_new, name='post_new'),
	path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
	path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
	path('post/<int:pk>/add-comment/', views.comment_add, name='comment_add'),
	path('post/<int:pk>/delete-comment/<int:cid>/', views.comment_delete, name='comment_delete'),
	path('post/<int:pk>/edit-comment/<int:cid>/', views.comment_edit, name='comment_edit'),
]
