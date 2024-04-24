from django.db import models


class Candidates(models.Model):
    election_area_id = models.IntegerField(default=0)
    name = models.CharField(max_length=300, null=True)
    photo = models.CharField(max_length=300, null=True)
    ballot_no = models.CharField(max_length=20, null=True)
    voter_no = models.IntegerField(default=0)
    enroll_no = models.IntegerField(default=0)
    insert_time = models.CharField(max_length=20, default='0000-00-00 00:00')
    insert_by = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class VoteCount(models.Model):
    candidate = models.ForeignKey(Candidates, on_delete=models.CASCADE)
    number_of_votes = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.candidate.name}: {self.number_of_votes} votes"

class VoterVote(models.Model):
    voter = models.IntegerField(null=False)
    vote_1 = models.BooleanField(default=False)
    vote_2 = models.BooleanField(default=False)
    vote_1_candidates = models.CharField(null=True,max_length=255)
    vote_2_candidates = models.CharField(null=True,max_length=255)