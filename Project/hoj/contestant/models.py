from django.db import models
from django.utils import timezone
from django.utils.timezone import now
from user.models import CustomUser
from contest.models import ContestParticipant
from problem.models import Problem
# Create your models here.

class ProblemTry(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    part=models.ForeignKey(ContestParticipant,default=1,on_delete=models.CASCADE)
    prob=models.ForeignKey(Problem,default=1,on_delete=models.CASCADE)
    status=models.BooleanField(default=False,null=True)

    def __str__(self):
        return str(self.user.id)+ str(self.part.id) + str(self.prob.id)+str(self.status)
