from django.shortcuts import render

from interviews.plot_gen import plot_interview_status
from .models import *
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import permissions,status
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch



def home(request):
    interviews = Interview.objects.filter(is_deleted=False).order_by('-date')
    plot = plot_interview_status()
    
    return render(request, 'home.html', {'interviews': interviews,'plot_url': f'data:image/png;base64,{plot}'})


def show_questions(request):
    questions = StudyMaterial.objects.filter(is_deleted=False)
    return render(request, 'show_questions.html', {'questions': questions})



def update_study_questions(request):
    #UPDATE API FOR CHANGE ANS IN STUDY MATERIAL 
    
    if request.method == 'PUT':
        try:
            # Parse the JSON body
            data = json.loads(request.body) 
            StudyMaterial.objects.filter(id=data['id'],is_deleted=False).update(answer=data['answer'])
            return JsonResponse({'status': True, 'message': 'Question updated successfully!'},status=200)
             
        except:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)
        
    if request.method == 'POST':
        try:
            # Parse the JSON body
            data = json.loads(request.body) 
            exist = StudyMaterial.objects.filter(question__iexact=data['question'],is_deleted=False).exists()
            if exist:
                return JsonResponse({'status': 'error', 'message': 'QUestion already exist'}, status=400)

            StudyMaterial.objects.create(
                question=data['question'],answer=data['answer'],belongs_to=data['type']
            )
                
            return JsonResponse({'status': True, 'message': 'Question created successfully!'},status=200)
             
        except:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)
        
    if request.method == 'DELETE':
        try:
            # Parse the JSON body
            data = json.loads(request.body)
            
            StudyMaterial.objects.filter(id=data['id']).update(is_deleted=True)
            return JsonResponse({'status': True, 'message': 'Question deleted successfully!'},status=200)
             
        except:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)
        


def add_interview_Web(request):
    return render(request, 'add_interview.html')


def view_interview_web(request, id):
    # Define a filtered queryset for questions
    filtered_questions = QuestionAnswer.objects.filter(is_deleted=False)
    
    interview = Interview.objects.filter(sno=id).prefetch_related(Prefetch('questions', queryset=filtered_questions)).first()
    interview_data = {
        'sno': interview.sno,
        'date': interview.date,
        'company_name': interview.company_name.company_name,
        'status': interview.status,
        'state': interview.state,
        'is_deleted': interview.is_deleted,
        'is_attended': interview.is_attended,
        'description': interview.description,
        'questions': [{'question': qa.question, 'answer': qa.answer} for qa in interview.questions.all()]
    }
    return render(request, 'view_interview.html', {'interview': interview_data})

@csrf_exempt
def add_question_web(request):
    if request.method == 'GET':
        question = QuestionAnswer.objects.filter(is_deleted=False)
        interview = Interview.objects.all()
        companies = Company.objects.all()
        
        context = {
        'questions': question,
        'interviews': interview,
        'company': companies,
        }
        return render(request, 'view_question.html', context=context)
    
    if request.method == 'POST':
        try:
            # Parse the JSON body
            data = json.loads(request.body)          

            exist = QuestionAnswer.objects.filter(question=data['question'],interview_id=int(data['interview'])).exists()
            if exist:
                return JsonResponse({'status': 'error', 'message': 'Question already exist'}, status=400)

            create = QuestionAnswer.objects.create(question=data['question'],interview_id=data['interview'],answer=data['answer'],
                                                   question_type=data['question_type'],comapny_question_id=data['company'])

            # Return a JSON response
            return JsonResponse({'status': 'success', 'message': 'Question added successfully!'},status=200)

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)
        
    if request.method == 'DELETE':
        try:
            data = json.loads(request.body)    
            id_ = data['id']              
            QuestionAnswer.objects.filter(id=id_).update(is_deleted=True)
            return JsonResponse({'status': 'success', 'message': 'Question deleted successfully!'})
        
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': 'Invalid data'}, status=400)

    

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)


def view_single_question(request, id):
    try:
        question = QuestionAnswer.objects.filter(id=id).values('id', 'interview_id', 'question', 'answer', 'question_type', 'comapny_question__company_name', 'is_deleted').first()  
        return render(request, 'view_singlequestion.html', {'question': [question]})  # Pass as a list
    except Exception as e:
        # Handle the error (e.g., logging)
        return render(request, 'error.html')  # Redirect to an error page if needed



def edit_single_question(request, id):
    try:
        if request.method == 'GET':
            question = QuestionAnswer.objects.filter(id=id).values('id', 'interview_id', 'question', 'answer', 'question_type', 'comapny_question__company_name', 'is_deleted').first()  
            return render(request, 'edit_question.html', {'question': [question]})  # Pass as a list
        
        if request.method == 'PUT':
            data = json.loads(request.body)    
            QuestionAnswer.objects.filter(id=id).update(question=data['question'],answer=data['answer'],question_type=data['question_type'])
            return JsonResponse({'status': 'success', 'message': 'Question updated successfully!'},status=200)
        
    except Exception as e:
        return render(request, 'error.html')  # Redirect

    

def list_company(request):
    res = Company.objects.all().values('id','company_name')
    res = list(res) if res else {}
    return JsonResponse({'data':res})



def add_company(request):
    try:
        data = json.loads(request.body)

        #check data is exist
        exist = Company.objects.filter(company_name=data['company_name']).exists()
        if exist:
            return JsonResponse({'status': 'error', 'message': 'Company already exists'}, status=400)
        else:
            Company.objects.create(company_name=data['company_name'])
        
        return JsonResponse({'status': 'success', 'message': 'Company created successfully'}, status=201)

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': 'error'}, status=500)
    
    


def save_interview(request):
    try:
        data = json.loads(request.body)
        if request.method == 'POST':       
            #check data is exist
            exist = Interview.objects.filter(company_name__company_name=data['company_name'],date=data['date']).exists()
            if exist:
                return JsonResponse({'status': 'error', 'message': 'Interview already added'}, status=400)
            else:
                comp_id = Company.objects.filter(company_name=data['company_name']).last() if Company.objects.filter(company_name=data['company_name']).exists() else Company.objects.create(company_name=data['company_name'])
                Interview.objects.create(company_name=comp_id,date=data['date'],status=data['status'],state=data['state'])   
                    
            return JsonResponse({'status': 'success', 'message': 'Interview added successfully'}, status=201)

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': 'error'}, status=500)
    

def edit_interview_web(request,id):
    try:        
        interview = Interview.objects.filter(sno=id).values('sno', 'date', 'company_name__company_name', 'status', 'state','description')
        return render(request, 'edit_interview.html', {'interview': list(interview)[0]})
        
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': 'error'}, status=500)
            
   
   

def edit_interview(request):
    try:
        data = json.loads(request.body)
        if request.method == 'PUT':       
            #check data is exist
            exist = Interview.objects.filter(sno=data['id']).exists()
            if exist:
                Interview.objects.filter(sno=data['id']).update(date=data['date'],status=data['status'],state=data['state'],description=data['description'])   

                return JsonResponse({'status': 'success', 'message': 'Interview updated successfully'}, status=201)
                               
            return JsonResponse({'status': 'Failed', 'message': 'Interview not found'}, status=400)

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': 'error'}, status=500)
    
    
def delete_interview(request,id):
    try:
        exist = Interview.objects.filter(sno=id).exists()
        if not exist:
            return JsonResponse({'status': 'Failed', 'message': 'Interview not found'}, status=400)

        interviews = Interview.objects.filter(sno=id).update(is_deleted=True)
        return JsonResponse({'status': 'success', 'message': 'Interview deleted successfully'}, status=201)
    
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': 'error'}, status=500)

    