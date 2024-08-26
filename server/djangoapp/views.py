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

from django.http import JsonResponse
from .models import CarMake, CarModel

from .restapis import get_request, analyze_review_sentiments, post_review



def get_cars(request):
    count = CarMake.objects.filter().count()
    print(count)
    if(count == 0):
        initiate()
    car_models = CarModel.objects.select_related('car_make')
    cars = []
    for car_model in car_models:
        cars.append({"CarModel": car_model.name, "CarMake": car_model.car_make.name})
    return JsonResponse({"CarModels":cars})

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


#Update the `get_dealerships` render list of dealerships all by default, particular state if state is passed
def get_dealerships(request, state="All"):
    if(state == "All"):
        endpoint = "/fetchDealers"
    else:
        endpoint = "/fetchDealers/"+state
    dealerships = get_request(endpoint)
    return JsonResponse({"status":200,"dealers":dealerships})

def get_dealer_reviews(request, dealer_id):
    # if dealer id has been provided
    if(dealer_id):
        endpoint = "/fetchReviews/dealer/"+str(dealer_id)
        reviews = get_request(endpoint)
        for review_detail in reviews:
            response = analyze_review_sentiments(review_detail['review'])
            print(response)
            review_detail['sentiment'] = response['sentiment']
        return JsonResponse({"status":200,"reviews":reviews})
    else:
        return JsonResponse({"status":400,"message":"Bad Request"})


def get_dealer_details(request, dealer_id):
    if(dealer_id):
        endpoint = "/fetchDealer/"+str(dealer_id)
        dealership = get_request(endpoint)
        return JsonResponse({"status":200,"dealer":dealership})
    else:
        return JsonResponse({"status":400,"message":"Bad Request"})


def get_dealers(request):
    # Fetch the list of dealers from the backend service
    endpoint = "/fetchDealers"
    dealers = get_request(endpoint)

    logger.info(f"Dealers data received from backend: {dealers}")

    # Check if the response contains a list of dealers
    if isinstance(dealers, list):
        # Iterate over the list and check if each item is a dictionary
        for dealer in dealers:
            if not isinstance(dealer, dict):
                logger.warning(f"Unexpected data format: {dealer}")
                return render(request, 'dealers.html', {"error": "Failed to fetch dealers"})

        # Create a context dictionary to pass the dealer data to the template
        context = {"dealers": dealers}

        # Render the template with the dealer data
        return render(request, 'dealers.html', context)
    else:
        # Handle the case when the response is not a list of dealers
        logger.warning(f"Unexpected data format: {dealers}")
        return render(request, 'dealers.html', {"error": "Failed to fetch dealers"})


def add_review(request):
    if(request.user.is_anonymous == False):
        data = json.loads(request.body)
        try:
            response = post_review(data)
            return JsonResponse({"status":200})
        except:
            return JsonResponse({"status":401,"message":"Error in posting review"})
    else:
        return JsonResponse({"status":403,"message":"Unauthorized"})


#added 
def populate_database(request):
    if request.method == 'POST':
        try:
            # Load JSON data from request body
            data = json.loads(request.body)
            # Extract car makes and models from data
            car_makes = data.get('car_makes')
            car_models = data.get('car_models')

            # Create the car makes and models in the database
            for make in car_makes:
                car_make, created = CarMake.objects.get_or_create(name=make)

                for model in car_models[make]:
                    car_model, created = CarModel.objects.get_or_create(name=model, car_make=car_make)

            return JsonResponse({"message": "Database populated successfully"})
        except json.JSONDecodeError:
            # If error, return a response with status 400 (Bad Request)
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        # If request method is not POST, return a response with status 405 (Method Not Allowed)
        return JsonResponse({'error': 'Method not allowed'}, status=405)

def dealers(request):
    # This function will render a template that should display dealer information.
    # Ensure the 'dealers_template.html' exists in your templates directory.
    return render(request, 'dealers_template.html')

def get_dealers_template(request):
    # Renamed function to avoid conflict with the existing 'get_dealers' function.
    # This function will render a template that should provide a UI for getting dealer information.
    # Ensure the 'get_dealers_template.html' exists in your templates directory.
    return render(request, 'get_dealers_template.html')