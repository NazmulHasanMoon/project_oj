from django.shortcuts import render, redirect, get_object_or_404
from contest.models import Contest,ContestParticipant
from problem.models import Problem
from contestant.models import ProblemTry
from user.models import CustomUser
from .forms import SubmitForm
from submission.models import Submission
from Judge_dir.judge import judging
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from datetime import datetime, date, time, timedelta

#To view all Contests
def contest_list(request):
    contests = Contest.objects.all().order_by('-id')
    context = {'contests': contests}
    return render(request, 'contest/contests.html', context)

#To view problems of a specific contest
#@login_required
def contest(request,cid):
    contest = get_object_or_404(Contest,id=cid)
    #print(timezone.now())
    #print(timezone.now()+timezone.timedelta(0,1200)-contest.end_time )
    #print(contest.problem_set.all())
    if timezone.now() > contest.end_time :
        status = "Finished !!"
    else :
        status = "Running...."  
    context={'contest':contest,'status':status}
    return render(request, 'contest/contest.html', context)

# Contest ended :(   
def contest_end(request,cid):
    contest = Contest.objects.get(id=cid)
    context = {'contest': contest}
    return render(request, 'contest/contest_end.html', context) 
    
#To View contest Problem
@login_required
def cont_problem(request, cid, pid):
    if request.method == 'POST':
        contest = get_object_or_404(Contest,id=cid)

        
        if timezone.now() > contest.end_time :
            return redirect('contest_end' , contest.id )  # show contest end message    
        
        form = SubmitForm(request.POST, request.FILES)
        if form.is_valid():
            code = form.save(commit=False)  # variable name need to change
            code.user_id = request.user
            
            # Current Problem 
            problem = Problem.objects.get(id=pid)
            problem.contest_time_submissions+=1
            # current user
            current_user = CustomUser.objects.get(id=request.user.id)
            current_user.problem_tried += 1

            code.problem_id = problem
            code.save()  # save the model before judging with default values
            if code.language == 'Python':  # Time limit for different language
                time = problem.time_limit[1]
            else:
                time = problem.time_limit[0]
            code.verdict, code.time = judging(problem.input_file.path, problem.output_file.path, code.code.path, code.language, time, problem.memory_limit)
            
            if code.verdict == 1:
               current_user.problem_solved += 1
               problem.contest_time_AC+=1


            #ContestParticipant,problemtry models update/create
            
            
            code.save()
            problem.save()
            current_user.save()
            print(current_user.id , problem.id)
            obj=ContestParticipant.objects.get_or_create(contestant__id=request.user.id ,contestid__id=contest.id)
            ob2=ProblemTry.objects.get_or_create(user__id=request.user.id , part__id=obj.id, problemid__id=problem.id)
            if(code.verdict==1 and obj2.status==False):
                obj2.status=True
                obj.solved+=1
                if(obj.penalty > 0):
                    obj.penalty_time+=(timezone.now()+timezone.timedelta(0,1200*obj.penalty)-contest.start_time)
            else:
                obj.penalty+=1
            
            obj.save()
            obj2.save()
            return redirect('single_status' , pid )  # after submit redirect to user_submission page
    else:
        form = SubmitForm()
        problem = Problem.objects.get(id=pid)
        contest = Contest.objects.get(id=cid)
        request.session['pid'] = pid
        context = {'problem': problem, 'contest': contest, 'form': form}
        return render(request, 'contest/cont_problem.html', context)


#To Show contest standings 
def contest_standings(request, cid):
    standings = ContestParticipant.objects.filter(contestid = cid).order_by('-solved','penalty_time')
    #print(contest)
    problem_list=ProblemTry.objects.filter(part=standings)
    contest=Contest.objects.get(id=cid)
    context = { 'standings':standings,'contest': contest,'problem_list':problem_list }
    return render(request, 'contest/ranklist.html', context)