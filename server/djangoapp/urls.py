from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'

urlpatterns = [
    # path for get dealerships
    path(route='get_dealers', view=views.get_dealerships, name='get_dealers'),
    path(route='get_dealers/<str:state>', view=views.get_dealerships, name='get_dealers_by_state'),
    # path for get dealer reviews
    path(route='reviews/dealer/<int:dealer_id>', view=views.get_dealer_reviews, name='dealer_details'),
    # path for add reviews
    path(route='add_review', view=views.add_review, name='add_review'),
    # path for get cars
    path(route='get_cars', view=views.get_cars, name ='getcars'),
    # Path for login 
    path(route='login', view=views.login_user, name='login'),
    # Path for logout
    path(route='logout', view=views.logout_user, name='logout'),
    # Path for registration
    path(route='register', view=views.registration, name='registration'),
    # Path for dealer reviews view
    path(route='dealer/<int:dealer_id>/reviews', view=views.get_dealer_reviews, name='dealer_reviews'),
    # Path for add a review view
    path(route='dealer/<int:dealer_id>/add_review', view=views.add_review, name='add_review'),

    #added
    path('populate_database/', views.populate_database, name='populate_database'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
