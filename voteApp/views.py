from django.shortcuts import render,redirect
from django.template import loader
from django.http import HttpResponse
from .models import Candidates,VoteCount,VoterVote
from authentication.views import login_required

@login_required(login_url='login')  
def ballot(request,id):
    
    voter = VoterVote.objects.get(voter=id)
    if voter.vote_1:
        return redirect("ballot_2", id=id)
    else:
        candidates = Candidates.objects.filter(election_area_id=1).values()
        context = {
            'candidates': candidates,
            'id':id,
        }
        return render(request, 'ballot.html', context=context)
@login_required(login_url='login')  
def ballot_2(request,id):
    voter = VoterVote.objects.get(voter=id)
    if voter.vote_2:
        return redirect("logout")
    else:
        candidates = Candidates.objects.filter(election_area_id=2).values()
        context = {
            'candidates': candidates,
            'id':id,
        }
        return render(request, 'ballot_2.html', context=context)

@login_required(login_url='login')  
def vote_count_1(request, id):
    if request.method == 'POST':
        candidate_ids = request.POST.getlist('candidate_ids')
        for candidate_id in candidate_ids:
            candidate = VoteCount.objects.get(candidate_id=candidate_id)
            voter = VoterVote.objects.get(voter=id)
            candidate.number_of_votes += 1
            candidate.save()  # Save the updated vote count
            voter.vote_1 = True
            voter.vote_1_candidates = str(candidate_ids)
            voter.save()
        return redirect("ballot_2", id=id)  # Move the redirect outside the loop
    else:
        pass

@login_required(login_url='login')  
def vote_count_2(request, id):
    if request.method == 'POST':
        candidate_ids = request.POST.getlist('candidate_ids')
        for candidate_id in candidate_ids:
            candidate = VoteCount.objects.get(candidate_id=candidate_id)
            voter = VoterVote.objects.get(voter=id)
            candidate.number_of_votes += 1
            candidate.save()  # Save the updated vote count
            voter.vote_2 = True
            voter.vote_2_candidates = str(candidate_ids)
            voter.save()
        return redirect("logout")  # Move the redirect outside the loop
    else:
        pass