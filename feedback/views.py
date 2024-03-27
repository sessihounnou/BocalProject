from django.shortcuts import render, redirect
from .models import Feedback
from .forms import FeedbackForm
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta, datetime

def submit_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            print('YES')
            form.save()
            return redirect('dashboard')
    else:
        print('NO')
        form = FeedbackForm()
    return render(request, 'feedback/submit_feedback.html', {'form': form})

"""
def dashboard(request):
    feedback_counts = Feedback.objects.values('emoji').order_by('emoji').annotate(total=Count('emoji'))
    return render(request, 'feedback/dashboard.html', {'feedback_counts': feedback_counts})
"""

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
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').replace(hour=0, minute=0, second=0)
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').replace(hour=23, minute=59, second=59)
        
    print(start_date)
    print(end_date)    
    emoji_stats = Feedback.objects.filter(created_at__range=(start_date, end_date)).values('emoji').annotate(count=Count('emoji'))

    return render(request, 'feedback/dashboard.html', {'emoji_stats': emoji_stats})