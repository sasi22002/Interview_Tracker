from django.dispatch import receiver
from django.db.models.signals import pre_save,post_save
from models import QuestionAnswer
import logging

@receiver(post_save, sender=QuestionAnswer)
def update_questiontype(sender, instance, created, **kwargs):
    try:
        if created == True:
            import pdb;pdb.set_trace()
            pass

    except Exception as e:
        logging.warning(f'admin_addon_notification- {e}')
        pass