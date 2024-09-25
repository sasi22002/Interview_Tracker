from django.urls import path
from . import views

urlpatterns = [
    
    #HOME
    path('', views.home, name='home'),
    
    #COMPANY ROUETS
    path('api/companies', views.list_company, name='list_company'),
    path('api/add_company', views.add_company, name='add_company'),
    
    #INTERVIEW ROUTES
    path('view/<int:id>/', views.view_interview_web, name='view_interview'),
    path('add_interview', views.add_interview_Web, name='add_interview'),
    path('api/add_interview', views.save_interview, name='save_interview'),
    path('api/edit_interview', views.edit_interview, name='edit_interview_api'),
    path('api/delete_interview/<int:id>', views.delete_interview, name='delete_interview_api'),
    path('edit_interview/<int:id>/', views.edit_interview_web, name='edit_interview'),
    
    #QUESTION ROUTES
    path('add_question', views.add_question_web, name='add_question'),
    path('add_question/view/<int:id>/', views.view_single_question, name='add_question_view'),
    path('edit_question/view/<int:id>/', views.edit_single_question, name='edit_question_view'),
    path('show-questions/', views.show_questions, name='show_questions'),
    path('show-questions/update-study_questions', views.update_study_questions, name='update-study_questions'),

]

