from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
import os,django,logging
import pandas as pd
from docx import Document
from interviews.models import StudyMaterial  # Replace with your app's name
from interviewTracker.settings import BASE_DIR

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'interviewTracker.settings')  # Replace with your project name
django.setup()

# Step 1: Extract data from the docx file
def extract_data_from_docx(docx_file):
    doc = Document(docx_file)
    questions = []
    answers = []
    current_question = ""
    current_answer = ""

    for para in doc.paragraphs:
        if para.style.name.startswith('Heading'):  # Assume Heading style is for questions
            if current_question and current_answer:  # If previous question-answer exists
                questions.append(current_question)
                answers.append(current_answer.strip())  # Append to the lists

            current_question = para.text  # New question
            current_answer = ""  # Reset the answer for new question
        else:
            current_answer += para.text + " "  # Accumulate answer text

    # Append the last question-answer pair
    if current_question and current_answer:
        questions.append(current_question)
        answers.append(current_answer.strip())

    return questions, answers

# Step 2: Convert data to pandas DataFrame
def create_dataframe(questions, answers):
    data = {'Question': questions, 'Answer': answers}
    df = pd.DataFrame(data)
    return df

def save_dataframe_to_model(df):
    for _, row in df.iterrows():
        # Saving each row of DataFrame to Django model
        exist = StudyMaterial.objects.filter(question=row['Question'],belongs_to="Interview").exists()
        if not exist:                  
            StudyMaterial.objects.create(
                question=row['Question'],
                answer=row['Answer'],
                belongs_to="Interview"  
            )
            

def save_questions_from_docx_with_pandas(docx_file):
    questions, answers = extract_data_from_docx(docx_file)
    df = create_dataframe(questions, answers)
    save_dataframe_to_model(df)


class Command(BaseCommand):
    help = 'Create question & Ans via a doc file'

    def handle(self, *args, **options):
        try:
            import shutil
            # Call the function with your .docx file path
            # docx_file =  os.path.join(BASE_DIR, "interviews","docs","python_interview_questions_and_answers_filled.docx")
            # save_questions_from_docx_with_pandas(docx_file)
            docx_file =  os.path.join(BASE_DIR, "interviews","docs","questions_and_answers.docx")
            import pdb;pdb.set_trace()
            shutil.copyfile(docx_file, "testcopy.md")

            save_questions_from_docx_with_pandas(docx_file)
        
            self.stdout.write(self.style.SUCCESS("Uploaded successfully"))
        except Exception as e:
            logging.info('command not works',e)
            raise CommandError(e)
    
