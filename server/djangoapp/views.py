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
import os


def get_cars(request):
    try:
        # Assuming CarModel is your model for cars
        cars = CarModel.objects.all()
        cars_list = [{"CarMake": car.make.name, "CarModel": car.model} for car in cars]  # Ensure correct field access
        return JsonResponse({"CarModels": cars_list}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


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


# Ensure correct JSON format in get_dealer function
def get_dealer_details(request, dealer_id):
    if dealer_id:
        endpoint = f"/fetchDealer/{str(dealer_id)}"
        dealership = get_request(endpoint)
        
        # Log the dealership data
        logger.info(f"Dealership data received: {dealership}")
        
        # Ensure dealership is a valid JSON object or dict
        if isinstance(dealership, dict):  # Ensure it's a dictionary
            return JsonResponse({"status": 200, "dealer": dealership})
        else:
            logger.error("Received invalid dealership data format.")
            return JsonResponse({"status": 400, "message": "Bad Request"})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})




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
    if request.user.is_anonymous:
        return JsonResponse({"status": 403, "message": "Unauthorized"})

    data = json.loads(request.body)
    review_text = data.get('review')
    dealer_id = data.get('dealer_id')  # Assuming dealer_id is passed in the request

    try:
        # First, post the review using your existing post_review logic
        response = post_review(data)
        
        # If the post request is successful, proceed to save the review to a file
        if response.status_code == 201:
            review_entry = {
                "dealer_id": dealer_id,
                "review": review_text,
                "timestamp": datetime.now().isoformat()
            }

            # Define the file path
            file_path = os.path.join('path_to_your_directory', 'reviews.json')

            # Read existing reviews from the file
            if os.path.exists(file_path):
                with open(file_path, 'r') as file:
                    existing_reviews = json.load(file)
            else:
                existing_reviews = []

            # Append the new review to the list
            existing_reviews.append(review_entry)

            # Write the updated reviews back to the file
            with open(file_path, 'w') as file:
                json.dump(existing_reviews, file, indent=4)

            return JsonResponse({"status": 200, "message": "Review added successfully"})
        else:
            return JsonResponse({"status": 401, "message": "Error in posting review"})

    except json.JSONDecodeError:
        return JsonResponse({"status": 400, "message": "Invalid JSON"}, status=400)
    except Exception as e:
        logger.error(f"Error in adding review: {str(e)}")
        return JsonResponse({"status": 500, "message": "Internal Server Error"}, status=500)



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

@csrf_exempt
def post_review(request, dealer_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Assuming 'review' is a key in the posted JSON
            review_text = data['review']
            # Add logic to save the review associated with the dealer_id
            # Example: Review.objects.create(dealer_id=dealer_id, review=review_text)
            
            return JsonResponse({"status": "success"}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)



def dealer_details(request, dealer_id):
    return HttpResponse (" dealer details")
    """if dealer_id:
        endpoint = f"/fetchDealer/{dealer_id}"
        dealership = get_request(endpoint)
        endpoint = f"/fetchReviews/dealer/{dealer_id}"
        reviews = get_request(endpoint)
        for review_detail in reviews:
            response = analyze_review_sentiments(review_detail['review'])
            review_detail['sentiment'] = response['sentiment']
        context = {
            "dealer": dealership,
            "reviews": reviews
        }
        return render(request, 'dealer_details.html', context)
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})"""