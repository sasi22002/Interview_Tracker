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
    is_deleted = models.BooleanField(default=False)
    is_attended = models.BooleanField(default=False)
    description = models.CharField(null=True,max_length=500)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    class Meta:
        db_table = 'interview_master'
   
class QuestionAnswer(models.Model):
    """
    Field : question_type
    Choices - Python , Django , Cloud , General , Others , Database , Pandas
    
    """
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE, related_name='questions')
    question = models.TextField()
    answer = models.TextField()
    question_type = models.CharField(max_length=20)
    comapny_question = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company_question')
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    
    class Meta:
        db_table = 'question_master'
   


class StudyMaterial(models.Model):
    """ 
    Model for save overall questiona and answers
    to prepare for an Interview 
    
    """
    question = models.TextField()
    answer = models.TextField()
    belongs_to = models.CharField(max_length=20)
    repeat_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    
    class Meta:
        db_table = 'preparation_master'
   
    