from functools import wraps
import logging
from models import Interview,QuestionAnswer

def get_user_info(function):
    @wraps(function)
    def wrap(cls, *args, **kwargs):
        try:
            user=QuestionAnswer.objects.filter(id=cls.request.user.id).last()
            cls.request.userdata = user
            
            return function(cls, *args, **kwargs)
        except Exception as e:
           pass
    return wrap
