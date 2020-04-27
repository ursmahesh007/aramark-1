"""
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from django.contrib import admin
# from django.contrib.auth import views as auth_views
from rest_framework import routers
from users import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'recommendedfood', views.RecommendedFoodViewSet)
router.register(r'allergymapping', views.AllergyMappingViewSet)

router.register(r'custom_recipe', views.CustomRecipeViewset)
router.register(r'meals', views.MealsViewset)
router.register(r'diary', views.DiaryViewset)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # path('',views.profile,name='home'),
    # path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    # path('update/',views.update,name='update'),

    path('register/', views.register, name='register'),
    path('login/', views.login),
    path('logout/', views.logout),
	path('admin/', admin.site.urls),
    path('admin/api/', include(router.urls)),
    path('admin/api/api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/api/', views.UserViewSet),
    path('admin/api/<int:id>/', views.RecommendedFoodViewSet),
]
