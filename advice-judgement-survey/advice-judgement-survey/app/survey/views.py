from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.db.models import Count
from .models import Advice, Rating

def consent_form(request):
    prolific_id = request.GET.get("prolific_id")
    if request.method == 'POST':
        prolific_id = request.POST.get('prolific_id')
        request.session['prolific_id'] = prolific_id  # Set prolific_id in session
        request.session['ratings_count'] = 0  # Initialize counter in session
        request.session['rated_chat_ids'] = []  # Initialize list of rated chats
        return redirect('rate_advice')  # Redirect to the rating view
    return render(request, 'consent_form.html', {'prolific_id': prolific_id})

def initiate_session(request, prolific_id):
    if 'ratings_count' not in request.session:
        request.session['ratings_count'] = 0
        request.session['rated_chat_ids'] = []
        request.session['prolific_id'] = prolific_id  # Store the prolific_id in the session

def update_session(request, chat_id):
    # Assuming the chat_id is the ID of a chat just rated by the user
    if 'rated_chat_ids' in request.session:
        request.session['rated_chat_ids'].append(chat_id)
        request.session.modified = True  # Tell Django to save changes

def logout_user(request):
    request.session.flush()  # Removes all session data

def rate_advice(request):
    # Ensure the session has the required prolific_id to proceed
    if 'prolific_id' not in request.session:
        return redirect('consent_form')  # No session found, redirect to consent form

    prolific_id = request.session['prolific_id']
    initiate_session(request, prolific_id)

    if request.session['ratings_count'] >= 3:
        return redirect('thank_you')

    advice = Advice.objects.exclude(
        chat_id__in=request.session['rated_chat_ids']  # Correctly referencing 'chat_id__in'
    ).annotate(
        num_ratings=Count('rating')
    ).select_related('chat').order_by('num_ratings').first()

    update_session(request, advice.chat.chat_id)

    if advice is None:
        return redirect('thank_you')

    if request.method == 'POST':
        rating_chat_value = request.POST.get('rating_chat')
        rating_value = request.POST.get('rating')
        text_feedback = request.POST.get('text_feedback')
        advice_id = request.POST.get('advice_id')

        if not rating_value or not text_feedback:
            return render(request, 'rate_advice.html', {
                'advice': advice,
                'error': 'Both a rating and feedback must be provided.'
            })

        # Create a new Rating instance
        Rating.objects.create(
            advice_id=advice_id,
            prolific_id=prolific_id,
            rating_chat=rating_chat_value,
            rating=rating_value,
            text_feedback=text_feedback
        )

        update_session(request, advice.chat_id)
        request.session['ratings_count'] += 1
        return redirect('rate_advice')

    return render(request, 'rate_advice.html', {'advice': advice})

def thank_you(request):
    logout_user(request)
    return render(request, 'thank_you.html')
