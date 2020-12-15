from django.contrib import admin
from .models import Contest,ContestParticipant
from problem.models import Problem

class ProblemInline(admin.StackedInline):
	model = Problem
	extra = 4


class ContestAdmin(admin.ModelAdmin):
	fieldsets=[
		(None,					{'fields':['user_id','title','category','description']}),
		('Date Information', 	{'fields':['start_time','end_time']}),
	]
	inlines = [ProblemInline]
	
admin.site.register(Contest,ContestAdmin)
admin.site.register(ContestParticipant)