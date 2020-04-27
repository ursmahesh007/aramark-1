# MarkoEatsBackend
This is the backend code for the MarkoEats application. This is done in python programming language and using the Django framework. Djongo allows usage of Django with MongoDB as our database, while DjangoRestFramework aids in creation of APIs.

Current API List: </br>
REGISTER (POST REQUEST): http://13.90.168.204/register/ </br>
REGISTER USING POSTMAN: body, raw </br>
{ </br>
"username": (username), </br>
"email": (email), </br>
"password1": (password), </br>
"password2": (password) </br>
}

LOGIN (POST REQUEST): http://13.90.168.204/login/ </br>
LOGIN USING POSTMAN: body, raw </br>
{ </br>
"username": (username), </br>
"password": (password) </br>
} </br>
*Once logged in, token will be given

LOGOUT (POST REQUEST): http://13.90.168.204/logout/ </br>
{ </br>
	"user_id": (user_id), </br>
	"token":  (token) </br>
}

TOKEN USING POSTMAN: headers </br>
Key: "Authorization" </br>
Value: "Token" (token) </br>
*Token will be needed to access API below.

GET ALL USERS: http://13.90.168.204/admin/api/users/ </br>
GET ONE USER: http://13.90.168.204/admin/api/users/3/ <--- specify user id </br>
POST/CREATE USER: http://13.90.168.204/admin/api/users/ </br>
PUT/EDIT USER: http://13.90.168.204/admin/api/users/3/ <--- specify user id </br>
RECOMMENDER (GET REQUEST): http://13.90.168.204/admin/api/recommendedfood/?id=5 <--- specify user id </br>
ALLERGYMAPPING (GET REQUEST): http://13.90.168.204/admin/api/allergymapping/

Note: These APIs require trailing backlash except for RECOMMENDER

Below are the dependencies which can be installed via pip:</br>
"pip install django 2.2.6"</br>
"pip install djongo 1.2.38"</br>
"pip install djangorestframework 3.10.3"</br>
"pip install django-crispy-forms 1.8.1"</br>

Use "pip freeze" to list dependencies in pip environment

Changes to models: "python manage.py makemigrations polls"</br>
Create/Change models in database: "python manage.py migrate"</br>
Create admin if needed: "python manage.py createsuperuser"</br>
Start development server: "python manage.py runserver"</br>

UI reference: https://xd.adobe.com/view/e6c91497-f223-4eb6-57ca-3258834e9d73-90f8/

Most changes will be in these files:</br>
settings.py</br>
models.py</br>
serializers.py</br>
views.py</br>
urls.py</br>

These are secondary files which will require minor changes from time to time:</br>
admin.py</br>
apps.py</br>
forms.py</br>

