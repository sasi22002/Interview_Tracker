from django.shortcuts import render
from .models import *
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import permissions,status



def home(request):
    interviews = Interview.objects.all()
    return render(request, 'home.html', {'interviews': interviews})

def add_interview(request):
    return render(request, 'add_interview.html')


def view_interview(request, id):
    interview = Interview.objects.get(id=id)
    return render(request, 'view_interview.html', {'interview': interview})

@csrf_exempt
def add_question(request):
    if request.method == 'GET':
        question = QuestionAnswer.objects.all()
        interview = Interview.objects.all()
        companies = Company.objects.all()
        
        context = {
        'questions': question,
        'interviews': interview,
        'company': companies,
        }
        # import pdb;pdb.set_trace()
        return render(request, 'view_question.html', context=context)
    
    if request.method == 'POST':
        try:
            # Parse the JSON body
            data = json.loads(request.body)          

            exist = QuestionAnswer.objects.filter(question=data['question'],interview_id=int(data['interview'])).exists()
            if exist:
                return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)

            create = QuestionAnswer.objects.create(question=data['question'],interview_id=data['interview'],answer=data['answer'],
                                                   question_type=data['question_type'],comapny_question_id=data['company'])

            # Return a JSON response
            return JsonResponse({'status': 'success', 'message': 'Question added successfully!'})

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)


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
        
    
   
   