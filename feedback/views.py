from django.shortcuts import render, redirect
from .models import Feedback
from .forms import FeedbackForm
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta, datetime
from django.http import JsonResponse
a = 0
start_date = None
end_date = timezone.now()

def submit_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            print('YES')
            form.save()
            return redirect('thanks')
    else:
        print('NO')
        form = FeedbackForm()
    return render(request, 'feedback/submit_feedback.html', {'form': form})


def get_emoji_stats(start_date, end_date):
    emoji_stats = Feedback.objects.filter(created_at__range=(start_date, end_date)).values('emoji').annotate(count=Count('emoji'))
    return emoji_stats

def dashboard(request):
    end_date = timezone.now()
    start_date = None
 
    period = request.GET.get('period')
    if period == 'aujourd_hui':
        start_date = datetime.combine(end_date.date(), datetime.min.time())
    elif period == 'hier':
        start_date = datetime.combine((end_date - timedelta(days=1)).date(), datetime.min.time())
        end_date = datetime.combine((end_date - timedelta(days=1)).date(), datetime.max.time())
    elif period == '7_derniers_jours':
        start_date = end_date - timedelta(days=7)
    elif period == '30_derniers_jours':
        start_date = end_date - timedelta(days=30)
    elif period == '365_derniers_jours':
        start_date = end_date - timedelta(days=365)
    elif period == 'personnalisé':
        start_date_str = request.GET.get('start_date')
        end_date_str = request.GET.get('end_date')
        if not start_date_str and end_date_str:  # Si seulement end_date est fourni pour la période personnalisée
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').replace(hour=23, minute=59, second=59)
            start_date = end_date.replace(hour=0, minute=0, second=0)  # Utilisez la même date pour start_date
        elif start_date_str and not end_date_str:  # Si seulement start_date est fourni pour la période personnalisée
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').replace(hour=0, minute=0, second=0)
            end_date = start_date.replace(hour=23, minute=59, second=59)  # Utilisez la même date pour end_date
        else:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').replace(hour=0, minute=0, second=0)
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').replace(hour=23, minute=59, second=59)  
    emoji_stats = get_emoji_stats(start_date, end_date)
    return render(request, 'feedback/dashboard.html', {'emoji_stats': emoji_stats})


def thanks(request):
    return render(request, 'feedback/thanks.html')