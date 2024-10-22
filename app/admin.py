from django.contrib import admin

from .models import Answers, Questions, Records, User

admin.site.register(User)
admin.site.register(Records)
admin.site.register(Questions)
admin.site.register(Answers)
