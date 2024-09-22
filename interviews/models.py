from django.db import models

# Create your models here.
from django.db import models

class Company(models.Model):
    company_name = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'company_data'
   

class Interview(models.Model):
    sno = models.AutoField(primary_key=True)
    date = models.DateField()
    company_name = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company_int')
    status = models.CharField(max_length=50)  # e.g., 'Did well', 'Not well'
    state = models.CharField(max_length=100)  # e.g., 'Moved to next', 'Failed', etc.
    
    class Meta:
        db_table = 'interview_master'
   
class QuestionAnswer(models.Model):
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE, related_name='questions')
    question = models.TextField()
    answer = models.TextField()
    question_type = models.CharField(max_length=20)
    comapny_question = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company_question')
    
    class Meta:
        db_table = 'question_master'
   
