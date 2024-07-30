from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.db.models import Count
from .models import Advice, Rating

def consent_form(request):
    prolific_id = request.GET.get("prolific_id")
    if request.method == 'POST':
        prolific_id = request.POST.get('prolific_id')
        # Store prolific_id, initialize ratings count and rated chat list in session
        request.session['prolific_id'] = prolific_id 
        request.session['ratings_count'] = 0  
        request.session['rated_chat_ids'] = []  
        return redirect('rate_advice')  # Redirect to the rating view
    # Render consent form with potential prefilled prolific_id
    return render(request, 'consent_form.html', {'prolific_id': prolific_id})

def initiate_session(request, prolific_id):
    if 'ratings_count' not in request.session:
        # Initialize session variables if they don't exist
        request.session['ratings_count'] = 0
        request.session['rated_chat_ids'] = []
        request.session['prolific_id'] = prolific_id  # Store the prolific_id in the session

def update_session(request, chat_id):
    # Add the rated chat_id to the session list
    if 'rated_chat_ids' in request.session:
        request.session['rated_chat_ids'].append(chat_id)
        request.session.modified = True  # Ensure session changes are saved

def logout_user(request):
    request.session.flush()  # Clear all session data

def rate_advice(request):
    # Check if prolific_id exists in session
    if 'prolific_id' not in request.session:
        return redirect('consent_form')  # Redirect to consent form if not found

    prolific_id = request.session['prolific_id']
    initiate_session(request, prolific_id)

    # Redirect to thank you page if the user has rated 3 advices
    if request.session['ratings_count'] >= 3:
        return redirect('thank_you')

    # Fetch the next piece of advice to rate, excluding already rated ones
    advice = Advice.objects.exclude(
        chat_id__in=request.session['rated_chat_ids']  # Correctly referencing 'chat_id__in'
    ).annotate(
        num_ratings=Count('rating')
    ).select_related('chat').order_by('num_ratings').first()

    update_session(request, advice.chat.chat_id)

    if advice is None:
        return redirect('thank_you') # Redirect if no advice is available

    if request.method == 'POST':
        # Retrieve form data
        rating_chat_value = request.POST.get('rating_chat')
        rating_value = request.POST.get('rating')
        text_feedback = request.POST.get('text_feedback')
        advice_id = request.POST.get('advice_id')

        if not rating_value or not text_feedback:
            # Render error if rating or feedback is missing
            return render(request, 'rate_advice.html', {
                'advice': advice,
                'error': 'Both a rating and feedback must be provided.'
            })

        # Save the new rating to the database
        Rating.objects.create(
            advice_id=advice_id,
            prolific_id=prolific_id,
            rating_chat=rating_chat_value,
            rating=rating_value,
            text_feedback=text_feedback
        )

        # Update session after rating
        update_session(request, advice.chat_id)
        request.session['ratings_count'] += 1
        return redirect('rate_advice') # Redirect to rate next advice

    # Render the advice rating form
    return render(request, 'rate_advice.html', {'advice': advice})

def thank_you(request):
    logout_user(request)    # Clear session data on thank you page
    return render(request, 'thank_you.html')    # Render thank you page
