from django.urls import path
from . import views
import os

app_name = 'xpndr'

urlpatterns = [
    path('all/', views.comment_list, name='comment_list'),
    path('active/', views.comment_active, name='comment_active'),
    path('inactive/', views.comment_inactive, name='comment_inactive'),
    path('all/<int:pk>', views.comment_delete, name='comment_delete'),
    path('form/', views.new_comment, name='new_comment'),
    path('update_post/<int:pk>', views.update_post, name='update_post'),
    path('detail/<int:pk>', views.comment_detail, name='comment_detail'),
    # path('sat_detail/', views.sat_detail, name='sat_detail'),    
]
