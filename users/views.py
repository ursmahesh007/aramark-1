'''
ViewSets are essentially just a type of class based view, that doesn't provide
any method handlers, such as `get()`, `post()`, etc... but instead has actions,
such as `list()`, `retrieve()`, `create()`, etc...

Actions are only bound to methods at the point of instantiating the views.
    user_list = UserViewSet.as_view({'get': 'list'})
    user_detail = UserViewSet.as_view({'get': 'retrieve'})

Typically, rather than instantiate views from viewsets directly, you'll
register the viewset with a router and let the URL conf be determined
automatically.
    router = DefaultRouter()
    router.register(r'users', UserViewSet, 'user')
    urlpatterns = router.urls

https://github.com/encode/django-rest-framework/blob/master/rest_framework/viewsets.py
https://www.django-rest-framework.org/api-guide/viewsets/

https://github.com/encode/django-rest-framework/blob/master/rest_framework/views.py
https://www.django-rest-framework.org/api-guide/generic-views/
https://docs.djangoproject.com/en/3.0/topics/class-based-views/
https://docs.djangoproject.com/en/3.0/ref/views/
'''
# from django.contrib import messages
# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render, redirect, get_object_or_404
# from django.http import HttpResponse, JsonResponse
from django.core.serializers import serialize
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt

from rest_framework import viewsets, mixins
from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
# from rest_framework.parsers import JSONParser, ParseError

from . import models
from . import serializers

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def register(request):
    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")
    if models.CustomUser.objects.filter(username=username).exists():
        return Response({"code": 1, "error": "Username is already in use"})
    elif models.CustomUser.objects.filter(email=email).exists():
        return Response({"code": 2, "error": "Email is already in use"})
    else:
        user = models.CustomUser.objects.create_user(username, email, password)
        user.save()
        token, _ = Token.objects.get_or_create(user=user)
        userquery = models.CustomUser.objects.filter(username=username)
        return Response({'token': token.key, 'user': userquery.values("id", "username", "email")[0]},
                    status=HTTP_200_OK)
    
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'status': False, 'token': None, 'user': None},
                        status=HTTP_200_OK)
    token, _ = Token.objects.get_or_create(user=user)
    userquery = models.CustomUser.objects.filter(username=username)
    # if userquery.values("first_name")[0]["first_name"] == '':
    for lists in userquery.values("id", "username", "email",
                    "first_name", "last_name", "age", "gender", "height", "weight", "activity",
                    "allergic_food"):
        # print(lists)
        for values in lists.values():
            if values is None:
                print(values)
                return Response({"code": 3, "error": "Missing profile information", 'status': True, 'token': token.key, 
                    'user': userquery.values("id", "username", "email",
                    "first_name", "last_name", "age", "gender", "height", "weight", "activity",
                    "allergic_food")[0]})
    return Response({'status': True, 'token': token.key, 'user': userquery.values("id", "username", "email",
                    "first_name", "last_name", "age", "gender", "height", "weight", "activity",
                    "allergic_food")[0]},
                    status=HTTP_200_OK)

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def logout(request):
    user_id = request.data.get("user_id")
    token = request.data.get("token")
    Token.objects.filter(user=user_id, key=token).delete()
    data = {'success': 'Sucessfully logged out'}
    return Response(data=data, status=HTTP_200_OK)

class IsSuperUser(BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_superuser

class IsUser(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user:
            if request.user.is_superuser:
                return True
            else:
                return obj == request.user
        else:
            return False

        if request.method == SAFE_METHODS:
            return True

class UserViewSet(mixins.CreateModelMixin, 
                mixins.RetrieveModelMixin, 
                mixins.UpdateModelMixin,
                mixins.DestroyModelMixin,
                mixins.ListModelMixin,
                viewsets.GenericViewSet):
    queryset = models.CustomUser.objects.all().order_by('id')
    serializer_class = serializers.UserSerializer

class RecommendedFoodViewSet(mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    queryset = models.RecommendedFood.objects.all().order_by('id')
    serializer_class = serializers.RecommendedFoodSerializer
    
    def get_queryset(self):
        queryset = self.queryset.values()
        # userquery = CustomUser.objects.filter(id=self.request.user.id)
        userquery = models.CustomUser.objects.filter(id=self.request.query_params.get('id'))
        for n in userquery.values("allergic_food"):
            allergy_list = n['allergic_food']
        # allergy_list = ['fish', 'milk', 'tree_nuts', 'peanut', 'shellfish', 'gluten'] # random user_allergy list

        recommend = [] # recommended recipe holder
        ind1 = '_' 
        
        # allergens = {"milk": 301, "egg": 302, "peanut": 303, "tree_nut": 304, "soy_soyabean": 305, "wheat": 306, "fish": 307, 
        #      "shellfish": 308, "msg_monosodium_glutamate": 309, "high_fructose_corn_syrup_hfcs": 310, "mustard": 311, 
        #      "celery": 312, "sesame": 313, "gluten": 314, "red_yellow_blue_dye": 315, "gluten_free_per_fda": 316, 
        #      "non_gmo_claim": 317}

        allergens =  models.AllergyMapping.objects.all().values()

        trans = []
        for num in allergy_list:
            for lists in allergens: #.items():
                for item, number in lists.items():   
                    if number == num:
                        trans.append(item)

        for recipe in queryset: # for every recipe from the json file
            ind = False # set indicator to False
            for allergent in recipe['allergen_attributes']: # for every allergent in the recipe
                for user_allergy in trans: # loop through for each individual user provided allergent
                    if ind1 + str(user_allergy) in allergent: # check if the user_allergent matches the allergent that we are currently looping through
                        if (recipe['allergen_attributes'][allergent] == 'YES'): # if the user provided allergent is actually an allergent in the recipe
                            ind = True # set the indicator to true and break
                            break
                if ind: # if the indicator is True, break the loop
                    break

            if not ind: # add the recipe to the recommender holder if the indicator is set to False.
                recommend.append(recipe)
        # print(recommend)
        return recommend

class AllergyMappingViewSet(mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    queryset = models.AllergyMapping.objects.all().order_by('id')
    serializer_class = serializers.AllergyMappingSerializer

class DiaryViewset(viewsets.ModelViewSet):
    queryset = models.Diary.objects.all()
    serializer_class = serializers.DiaryEntriesSerializer

class CustomRecipeViewset(viewsets.ModelViewSet):
    queryset = models.Custom_recipes.objects.all()
    serializer_class = serializers.CustomRecipeSerializer

class MealsViewset(viewsets.ModelViewSet):
    queryset = models.Meals.objects.all()
    serializer_class = serializers.MealsSerializer










# @csrf_exempt
# def register(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             # username = form.cleaned_data.get('username')
#             messages.success(request, f'Your account has been created! You are now able to log in')
#             return redirect('home')
#     else:
#         form = CustomUserCreationForm()
#     return render(request, 'register.html', {'form': form})

# def update(request):
#     if request.method == 'POST':
#         u_form = CustomUserChangeForm(request.POST, instance=request.user)

#         if u_form.is_valid():
#             u_form.save()

#             messages.success(request, f'Your account has been updated!')
#             return redirect('home')

#     else:
#         u_form = CustomUserChangeForm(instance=request.user)
#     context = {
#         'u_form': u_form,
#     }
#     return render(request, 'update.html',context)

# @login_required
# def profile(request):
#     context={
#     'id': request.user.id,
#     'username':request.user.username,
#     'email':request.user.email,
#     'first_name':request.user.first_name,
#     'last_name':request.user.last_name,
#     'age':request.user.age,
#     'gender':request.user.gender,
#     'height':request.user.height,
#     'weight':request.user.weight,
#     'activity':request.user.activity,
#     'allergic_food':request.user.allergic_food
#     }
#     return render(request, 'profile.html',context)

# class UserPOST(mixins.CreateModelMixin, 
#                 viewsets.GenericViewSet):
#     queryset = CustomUser.objects.all().order_by('id')
#     serializer_class = UserSerializer

# class UserPUT(mixins.UpdateModelMixin,
#                 viewsets.GenericViewSet):
#     queryset = CustomUser.objects.all().order_by('id')
#     serializer_class = UserSerializer2

# class UserDELETE(mixins.DestroyModelMixin,
#                 viewsets.GenericViewSet):
#     queryset = CustomUser.objects.all().order_by('id')
#     serializer_class = UserSerializer2

# class UserViewSet(viewsets.ModelViewSet):
#     queryset = CustomUser.objects.all().order_by('id')
#     serializer_class = UserSerializer

    # def get_read_serializer_class(self):
    #     if self.request.method == 'POST':
    #         return OrderDetailSerializer

    # get_write_serializer_class

    # def get_queryset(self):
    #     if self.request.query_params.get('id') is not None:
    #         queryset = self.queryset.values().filter(id=self.request.query_params.get('id'))
    #     else:
    #         queryset = self.queryset.values()

    #     for x in queryset:
    #         print(x)
    #         if x['allergic_food'] is not None:
    #             x['allergic_food'] = x['allergic_food'].replace("'", "")
    #             x['allergic_food'] = x['allergic_food'].replace('"', "")
    #             x['allergic_food'] = x['allergic_food'].replace(" ", "")
    #             x['allergic_food'] = x['allergic_food'].replace("[", "")
    #             x['allergic_food'] = x['allergic_food'].replace("]", "")
    #             x['allergic_food'] = x['allergic_food'].split(',')
    #         else:
    #             continue

    #     return queryset
    
    #print(CustomUser.objects.filter(id=4))

    # def get_permissions(self):
    #     if self.action == 'list':
    #         self.permission_classes = [IsSuperUser, ]
    #     elif self.action == 'retrieve':
    #         self.permission_classes = [IsUser]
    #     return super(self.__class__, self).get_permissions()

    # def list(self, request):
    #     queryset = CustomUser.objects.all()
    #     serializer = UserSerializer(queryset, many=True)
    #     parsed = serializer.data
    #     parsed = list(parsed[0].items())[0:][0]
    #     key = parsed[0]

    #     value = parsed[1][1:-1].split(', ')
    #     value = [int(i) for i in value]
        
    #     # value = parsed[1][1:-1].replace("'", "" )
    #     # value = list(value.split(', '))
    #     print({key:value})
        
    #     return Response(serializer.data)

class UserInformationViewSet(viewsets.ModelViewSet):
    queryset = models.UserInformation.objects.all().order_by('id')
    serializer_class = serializers.UserInformationSerializer
    
    # def list(self, request):
    #     queryset = Allergies_List.objects.all()
    #     serializer = Allergies_ListSerializer(queryset, many=True)
    #     # parsed = serializer.data
    #     # parsed = list(parsed[0].items())[0:][0]
    #     # key = parsed[0]

    #     # value = parsed[1][1:-1].split(', ')
    #     # value = [int(i) for i in value]

    #     # # value = parsed[1][1:-1].replace("'", "" )
    #     # # value = list(value.split(', '))
    #     # print({key:value})
    #     print(serializer.data)
    #     return Response(serializer.data)

    # def retrieve(self, request, pk=None):
    #     queryset = Allergies_List.objects.all()
    #     user = get_object_or_404(queryset, pk=pk)
    #     serializer = Allergies_ListSerializer(user)
    #     print("HEHE",Response(serializer.data))
    #     return Response(serializer.data)


# @csrf_exempt
# def allergies_list(request):
#     """
#     List all code snippets, or create a new snippet.
#     """
#     if request.method == 'GET':
#         allergies = Allergies_List.objects.all()
#         serializer = Allergies_ListSerializer(allergies, many=True)
#         return JsonResponse(serializer.data, safe=False)

# @csrf_exempt
# def allergies_detail(request, pk):
#     """
#     Retrieve, update or delete a code snippet.
#     """
#     try:
#         allergies = Allergies_List.objects.get(pk=pk)
#     except Allergies_List.DoesNotExist:
#         return HttpResponse(status=404)

#     if request.method == 'GET':
#         serializer = Allergies_ListSerializer(allergies)
#         return JsonResponse(serializer.data)

# class GroupViewSet(viewsets.ModelViewSet):
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer



