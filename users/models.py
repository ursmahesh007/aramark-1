'''
A model is the single, definitive source of information about your data. 
It contains the essential fields and behaviors of the data you’re storing. 
Generally, each model maps to a single database table.

The basics:
Each model is a Python class that subclasses django.db.models.Model.
Each attribute of the model represents a database field.
With all of this, Django gives you an automatically-generated database-access API.

https://docs.djangoproject.com/en/3.0/topics/db/models/
'''
# users/models.py
# from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractUser
from django.db import models
from djongo import models

# Create your models here.
class CustomUser(AbstractUser):    
    age_range = ((1, "15-20"), (2, "20-25"), (3, "25-30"), (4, "30-35"), (5, "35-40"), (6, "40-45"), (7, "45-50"))
    genders = ((1, "Male"), (2, "Female"))
    height_range = ((1, "4'0\" - 4'11\""), (2, "5'0\" - 5'11\""), (3, "6'0\" - 6'11\""), (4, "7'0\" - 7'11\""))
    weight_range = ((1, "Below 150lb"), (2, "150lb to 200lb"), (3, "Over 200lb"))
    lifestyle = ((1, "Sedentary"), (2, "Moderately Active"), (3, "Active"))
    
    email = models.CharField(max_length = 32, unique=True)
    first_name = models.CharField(max_length = 32, default = '', blank = True)
    last_name = models.CharField(max_length = 32, default = '', blank = True)
    age = models.IntegerField(choices = age_range, null = True, blank = True)
    gender = models.IntegerField(choices = genders, null = True, blank = True)
    height = models.IntegerField(choices = height_range, null = True, blank = True)
    weight = models.IntegerField(choices = weight_range, null = True, blank = True)
    activity = models.IntegerField(choices = lifestyle, null = True, blank = True)
    allergic_food = models.ListField(default = list)

    def __str__(self):
        return str(self.id)

class RecommendedFood(models.Model):
    recipe_id = models.CharField(max_length = 256)
    recipe_name = models.CharField(max_length = 256)
    marketing_description = models.CharField(max_length = 256)
    allergen_attributes = models.CharField(max_length = 256)
    dietary_attributes = models.CharField(max_length = 256)

    class Meta:
        managed = False
        db_table = 'serviceRecipeNutrition'

    
    # username = None
    # email = models.EmailField(_('email address'), unique=True)
    # USERNAME_FIELD = 'email'

class AllergyMapping(models.Model):
    milk = models.IntegerField()
    egg = models.IntegerField()
    peanut = models.IntegerField()
    tree_nut = models.IntegerField()
    soy = models.IntegerField()
    wheat = models.IntegerField()
    fish = models.IntegerField()
    shellfish = models.IntegerField()
    msg_monosodium_glutamate = models.IntegerField()
    high_fructose_corn_syrup_hfcs = models.IntegerField()
    mustard = models.IntegerField()
    celery = models.IntegerField()
    sesame = models.IntegerField()
    gluten = models.IntegerField()
    red_yellow_blue_dye = models.IntegerField()
    gluten_free_per_fda = models.IntegerField()
    non_gmo_claim = models.IntegerField()

    class Meta:
        db_table = 'foodallergies'
        managed = False
    

class Custom_recipes(models.Model):
    recipe_name = models.CharField(max_length = 256)
    recipe_description = models.CharField(max_length = 256)
    preparation_time  = models.CharField(max_length = 256)
    number_of_servings = models.DecimalField(max_digits= 5, decimal_places= 2)
    calories_per_serving = models.CharField(max_length = 256)

    def __str__(self):
        return self.recipe_name

class Meals(models.Model):
    _id = models.ObjectIdField()
    recipe_id = models.CharField(max_length = 256)
    recipe_name = models.CharField(max_length = 256)
    marketing_description = models.CharField(max_length = 256)
    allergen_attributes = models.CharField(max_length = 256)
    dietary_attributes = models.CharField(max_length = 256)

    class Meta:
        managed = False
        db_table = 'serviceRecipeNutrition'

    def __str__(self):
        return self.recipe_id


class Diary(models.Model):
    meals = ((1, "Breakfast"), (2, "Lunch"), (3, "Dinner"), (4, "Snack"))

    timestamp_entry = models.DateTimeField(max_length=100,null = True)
    profile_id = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    meal_type = models.CharField(choices=meals,max_length=100,null = True)
    is_custom_recipe = models.BooleanField(null=True)
    custom_recipe = models.ManyToManyField(Custom_recipes, null = True, blank = True)
    meals = models.ManyToManyField(Meals)












class Allergies_List(models.Model):
    allergy_id = models.CharField(default='', max_length = 90)
    class Meta:
        managed = False
class UserInformation(models.Model):
    genders = (("F", "Female"), ("M", "Male"))
    levels = ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5))

    # profile_id = models.PositiveIntegerField(blank = True, null = True)
    # allergic_food = ArrayField(models.CharField(max_length=10, blank=True), size=8, default = list,)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank = True, null = True)
    height = models.FloatField(help_text="Please use centimeters",default = 0, blank = True, null = True)
    weight = models.FloatField(help_text="Please use lbs",default = 0, blank = True, null = True)
    gender = models.CharField(max_length = 1, choices = genders, default = '', blank = True)
    target_calorie_intake = models.FloatField(default = 0,blank = True, null = True)
    preferred_meal = models.CharField(max_length = 30, default = '', blank = True)
    allergic_food = models.CharField(max_length = 30, default = '', blank = True)
    work_out_level = models.CharField(max_length = 1, choices = levels, help_text="With 5 being the highest", default = '', blank = True)
    dietary_preferences = models.CharField(max_length = 30, default = '', blank = True)
    health_history = models.CharField(max_length = 30, default = '', blank = True)
    preferred_breakfast_time = models.CharField(max_length = 30, default = '', blank = True)
    preferred_lunch_time = models.CharField(max_length = 30, default = '', blank = True)
    preferred_dinner_time = models.CharField(max_length = 30, default = '',blank = True)
    # class ReadonlyMeta:
    #     readonly = ["allergic_food"]
    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['zip_code']

# class RecommendedFood(models.Model):
#     # rfood_id = models.PositiveIntegerField(blank = True, null = True)
#     # profile_id = models.PositiveIntegerField(blank = True, null = True)
#     # food_chart_id = models.PositiveIntegerField(blank = True, null = True)
#     food_item = models.CharField(max_length=255, default = '', blank = True)

# class CalorieTracker(models.Model):
#     # ctracker_id = models.PositiveIntegerField(blank = True, null = True)
#     # profile_id = models.PositiveIntegerField(blank = True, null = True)
#     calorie_count = models.FloatField(blank = True, null = True)
#     date = models.DateField(blank = True, null = True)
#     consumed_calories = models.FloatField(blank = True, null = True)
#     remaining_calories = models.FloatField(blank = True, null = True)
#     total_calories = models.FloatField(blank = True, null = True)

# class FoodIntakeHistory(models.Model):
#     # intake_id = models.PositiveIntegerField(blank = True, null = True)
#     # profile_id = models.PositiveIntegerField(blank = True, null = True)
#     food_item = models.CharField(max_length=255, default = '', blank = True)
#     intake_time = models.DateField(blank = True, null = True)
#     intake_calories = models.FloatField(blank = True, null = True)

# class FoodAllergies(models.Model):
#     # allergy_id = models.PositiveIntegerField(blank = True, null = True)
#     # profile_id = models.PositiveIntegerField(blank = True, null = True)
#     food_chart_id = models.PositiveIntegerField(blank = True, null = True)
#     food_item = models.CharField(max_length=255, default = '', blank = True)

# class FoodMenu(models.Model):
#     # food_chart_id = models.PositiveIntegerField(blank = True, null = True)
#     cuisine_name = models.CharField(max_length=255, default = '')
#     ratings = models.CharField(max_length=255, default = '')
#     description = models.CharField(max_length=255, default = '')
#     calories = models.FloatField(blank = True, null = True)
#     carbs_count = models.FloatField(blank = True, null = True)
#     protein_count = models.FloatField(blank = True, null = True)
#     bar_code = models.PositiveIntegerField(blank = True, null = True)

# class FoodOrderHistory(models.Model):
#     # order_id = models.PositiveIntegerField(blank = True, null = True)
#     # profile_id = models.PositiveIntegerField(blank = True, null = True)
#     # food_chart_id = models.PositiveIntegerField(blank = True, null = True)
#     food_item = models.CharField(max_length=255, default = '')
#     order_time = models.DateField(blank = True, null = True)