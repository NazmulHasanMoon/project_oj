from django.db import models
from django.utils import timezone
from django.utils.timezone import now
from user.models import CustomUser
from contest.models import ContestParticipant
from problem.models import Problem
# Create your models here.

class ProblemTry(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    part=models.ForeignKey(ContestParticipant,on_delete=models.CASCADE)
    problemid=models.ForeignKey(Problem,on_delete=models.CASCADE)
    status=models.BooleanField(default=False,null=True)

    def __str__(self):
        return str(self.user)+ str(self.part) + str(self.problemid)+str(self.status)
