# Uncomment the required imports before adding the code

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from datetime import datetime
from django.shortcuts import redirect
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
    context = {}

    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']
    username_exist = False
    email_exist = False
    try:
        # Check if user already exists
        User.objects.get(username=username)
        username_exist = True
    except:
        # If not, simply log this is a new user
        logger.debug("{} is new user".format(username))

    # If it is a new user
    if not username_exist:
        # Create user in auth_user table
        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,password=password, email=email)
        # Login the user and redirect to list page
        login(request, user)
        data = {"userName":username,"status":"Authenticated"}
        return JsonResponse(data)
    else :
        data = {"userName":username,"error":"Already Registered"}
        return JsonResponse(data)


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
