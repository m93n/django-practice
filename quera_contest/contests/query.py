from django.contrib.auth import get_user_model
from django.db.models import Max
from django.db.models.expressions import F
from django.shortcuts import get_object_or_404

from problems.models import Submission, Problem
from .models import Contest
from django.db.models import Max, Q

User = get_user_model()


def list_problems(contest_id):
    problems = Contest.objects.get(id=contest_id).problems.all()
    return problems

def list_users(contest_id):
    participants = Contest.objects.get(id=contest_id).participants.all()
    return participants


def list_submissions(contest_id):
    participants_id = Contest.objects.get(id=contest_id).participants.all().values_list('id')
    submissions = Submission.objects.filter(participant__in=participants_id).order_by('-submitted_time')
    return submissions


def list_problem_submissions(contest_id, problem_id):
    participants_id = Contest.objects.get(id=contest_id).participants.all().values_list('id')
    submissions = Submission.objects.filter(participant__in=participants_id).filter(problem=problem_id).order_by('-submitted_time')
    return submissions


def list_user_submissions(contest_id, user_id):
    participant = Contest.objects.get(id=contest_id).participants.get(id=user_id)
    submissions = Submission.objects.filter(participant=participant).order_by('-submitted_time')
    return submissions


def list_problem_user_submissions(contest_id, user_id, problem_id):
    participant = Contest.objects.get(id=contest_id).participants.get(id=user_id)
    submissions = Submission.objects.filter(participant=participant).filter(problem=problem_id).order_by('-submitted_time')
    return submissions


def list_users_solved_problem(contest_id, problem_id):
    participants = Contest.objects.get(id=contest_id).participants.all().values_list('id')
    score = Problem.objects.get(id=3).score
    submissions = Submission.objects.filter(participant__in=participants).filter(problem=3).filter(score=score).values_list('participant').order_by('-submitted_time')
    users = User.objects.filter(id__in=submissions)
    return users
    


def user_score(contest_id, user_id):
    participant = Contest.objects.get(id=contest_id).participants.get(id=user_id)
    submission = Submission.objects.filter(participant=participant)
    problems = submission.values_list('problem')
    sum_max_scores = 0
    for problem in list(dict.fromkeys(problems)):
        scores = submission.filter(problem=problem)
        max_score = scores.aggregate(Max('score'))['score__max']
        sum_max_scores = sum_max_scores + max_score 
    
    return sum_max_scores



def list_final_submissions(contest_id):
    participants = Contest.objects.get(id=contest_id).participants.all()
    problems = Contest.objects.get(id=contest_id).problems.all()
    submitted_times = []
    for participant in participants:
        for problem in problems:
            submitted_time = Submission.objects.filter(Q(participant=participant),Q(problem=problem)).aggregate(Max('submitted_time'))
            submitted_times.append(submitted_time['submitted_time__max'])
   
    submission = Submission.objects.filter(Q(participant__in=participants),Q(submitted_time__in=submitted_times)).annotate(score__max=F('score'))

    return list(submission.values('participant_id', 'problem_id', 'score__max'))