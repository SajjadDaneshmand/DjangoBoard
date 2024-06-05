from django.contrib import admin
from .models import Topic, Board, Post

# Register your models here.


main_app_models = [Board, Topic, Post]
admin.site.register(main_app_models)
