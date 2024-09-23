from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('view/<int:id>/', views.view_interview, name='view_interview'),
    path('add_question', views.add_question, name='add_question'),
    path('add_interview', views.add_interview, name='add_interview'),
    path('api/companies', views.list_company, name='list_company'),
    path('api/add_company', views.add_company, name='add_company'),
    path('api/add_interview', views.save_interview, name='save_interview'),
]

