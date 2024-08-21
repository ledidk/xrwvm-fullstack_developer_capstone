# Uncomment the following imports before adding the Model code

from django.db import models
from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator

# Car Make model
class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    # Add other fields as needed

    def __str__(self):
        return self.name  # Return the name as the string representation of the CarMake object

# Car Model model
class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)  # Many-to-One relationship with CarMake
    name = models.CharField(max_length=100)
    CAR_TYPES = [
    ('SEDAN', 'Sedan'),
    ('SUV', 'SUV'),
    ('WAGON', 'Wagon'),
    ('COUPE', 'Coupe'),
    ('CONVERTIBLE', 'Convertible'),
    ('HATCHBACK', 'Hatchback'),
    ('MINIVAN', 'Minivan'),
    ('PICKUP', 'Pickup Truck'),
    ('SPORTS', 'Sports Car'),
    ('CROSSOVER', 'Crossover'),
    ('HYBRID', 'Hybrid'),
    ('ELECTRIC', 'Electric'),
    ('LUXURY', 'Luxury'),
]
    type = models.CharField(max_length=15, choices=CAR_TYPES, default='SUV')
    year = models.IntegerField(default=2023,
        validators=[
            MaxValueValidator(2023),
            MinValueValidator(2015)
        ]
    )
    # Add other fields as needed

    def __str__(self):
        return f"{self.name} ({self.car_make.name})"  # Return the name of the car model and its make
