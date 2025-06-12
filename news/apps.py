from django.apps import AppConfig
import os
class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'
    path = os.path.dirname(os.path.abspath(__file__))
    verbose_name = 'Новостной портал' 