from django.contrib import admin
from .models import Athlete, Activity, ChallengedSegment

# Register your models here.
admin.site.register(Athlete)
admin.site.register(ChallengedSegment)
admin.site.register(Activity)
