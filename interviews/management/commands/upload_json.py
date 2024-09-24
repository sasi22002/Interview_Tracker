from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
import os,django,logging
import pandas as pd
from docx import Document
from interviews.models import PrepareQuestions  # Replace with your app's name
from interviewTracker.settings import BASE_DIR
import json


class Command(BaseCommand):
    help = 'Create question & Ans via a json file'

    def handle(self, *args, **options):
        try:
            docx_file =  os.path.join(BASE_DIR, "interviews","docs","question.json")
            with open(docx_file) as json_file:
                json_data = json.load(json_file)

            for val in json_data:
                exist = PrepareQuestions.objects.filter(question=val,belongs_to="Interview").exists()
                if not exist:                  
                    PrepareQuestions.objects.create(
                        question=val,
                        answer=json_data[val],
                        belongs_to="Interview"  
                    )
        
            self.stdout.write(self.style.SUCCESS("Uploaded successfully"))
        except Exception as e:
            logging.info('command not works',e)
            raise CommandError(e)
    

