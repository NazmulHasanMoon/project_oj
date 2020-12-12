from django.shortcuts import render, redirect, get_object_or_404
from contest.models import Contest,ContestParticipants
from problem.models import Problem
from user.models import CustomUser
from .forms import SubmitForm
from submission.models import Submission
from Judge_dir.judge import judging
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.decorators import login_required

#To view all Contests
def contest_list(request):
    contests = Contest.objects.all().order_by('-id')
    context = {'contests': contests}
    return render(request, 'contest/contests.html', context)

#To view problems of a specific contest
#@login_required
def contest(request,cid):
    contest = get_object_or_404(Contest,id=cid)
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
def cont_problem(request, pid, cid):
    if request.method == 'POST':
        contest = Contest.objects.get(id=cid)
        
        if timezone.now() > contest.end_time :
            return redirect('contest_end' , contest.id )  # show contest end message    
        
        form = SubmitForm(request.POST, request.FILES)
        if form.is_valid():
            code = form.save(commit=False)  # variable name need to change
            code.user_id = request.user
            
            # Current Problem 
            problem = Problem.objects.get(id=pid)
            problem.no_of_submissions += 1

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
               problem.no_of_accepted += 1
            
            try:
                obj = ContestParticipants.objects.get(contestant=request.user, contest_id=cid)
                if(code.verdict==1 and obj.problem_list[pid-1]==False):
                    obj.problem_list[pid-1]=True
                    obj.solved+=1
                else:
                    obj.penalty+=20
                obj.save()
            except ContestParticipants.DoesNotExist:
                obj = ContestParticipants(contestant=request.user, contest_id=cid)
                if(code.verdict==1):
                    obj.problem_list[pid-1]=True
                    obj.solved+=1
                else:
                    obj.penalty+=20
                obj.save()
            
            code.save()
            problem.save()
            current_user.save()
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
    contest = Contest.objects.get(id=cid)
    context = { 'contest': contest }
    return render(request, 'contest/ranklist.html', context)