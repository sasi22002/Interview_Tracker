from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
import os,django,logging
import pandas as pd
from docx import Document
from interviews.models import StudyMaterial  # Replace with your app's name
from interviewTracker.settings import BASE_DIR
from interviews.models import QuestionAnswer



class Command(BaseCommand):
    help = 'Create question & Ans via a doc file'

    def handle(self, *args, **options):
        try:
            import shutil
        
            x = plot_interview_status()
            return x
            

          
           
        
            self.stdout.write(self.style.SUCCESS("Uploaded successfully"))
        except Exception as e:
            logging.info('command not works',e)
            raise CommandError(e)
    

#how to revert last 2 migration
#at a time 5 request to a api --- how django handle it
#default connection to db from django
#above question
#memery managemnt in python
#annotae in django
#f functions in django
#how to change db col name for response only ?
#git stash what does ?
#x = [1,2,3,4]
#24,12,8,6