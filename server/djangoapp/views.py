# Uncomment the required imports before adding the code

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from datetime import datetime

from django.http import JsonResponse
from django.contrib.auth import login, authenticate
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from .populate import initiate


# Get an instance of a logger
logger = logging.getLogger(__name__)

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['userName']
        password = data['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['username'] = username  # Store username in session
            return JsonResponse({"userName": username, "status": "Authenticated"})
        else:
            return JsonResponse({"status": "Failed"}, status=401)
    return JsonResponse({"status": "Invalid request"}, status=400)

@csrf_exempt
def logout_user(request):
    if request.method == 'POST':
        logout(request)
        request.session.flush()  # Clear all session data
        return JsonResponse({"status": "Logged out"})
    return JsonResponse({"status": "Invalid request"}, status=400)

@csrf_exempt
def registration(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['userName']
        password = data['password']
        if User.objects.filter(username=username).exists():
            return JsonResponse({"status": "User already exists"})
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return JsonResponse({"status": "Registered and Authenticated", "userName": username})
    return JsonResponse({"status": "Invalid request"}, status=400)

def get_dealerships(request):
    # Assuming you have a function to get dealerships
    dealerships = initiate()  # Example function, replace with actual
    return render(request, 'djangoapp/index.html', {"dealerships": dealerships})

def get_dealer_reviews(request, dealer_id):
    # Replace with actual review retrieval logic
    reviews = initiate()  # Example function, replace with actual
    return render(request, 'djangoapp/dealer_reviews.html', {"reviews": reviews})

def get_dealer_details(request, dealer_id):
    # Replace with actual dealer detail retrieval logic
    dealer_details = initiate()  # Example function, replace with actual
    return render(request, 'djangoapp/dealer_details.html', {"dealer": dealer_details})

def add_review(request, dealer_id):
    if request.method == "POST":
        review_text = request.POST.get('review')
        # Add review logic here
        messages.success(request, "Review submitted successfully!")
        return redirect('djangoapp:dealer_reviews', dealer_id=dealer_id)
    else:
        return render(request, 'djangoapp/add_review.html', {"dealer_id": dealer_id})
