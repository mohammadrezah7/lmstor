from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Research, ResearchParticipant


def research_list(request):
    researches = Research.objects.all()
    return render(request, 'research/list.html', {'researches': researches})


@login_required
def my_research(request):
    professor_id = request.session.get('professor_id')
    participations = ResearchParticipant.objects.filter(
        participantid=professor_id,
        participanttype='Professor'
    ).select_related('researchid')
   