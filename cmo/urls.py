"""CMO URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from cmoapi.views import register_user, login_user
from rest_framework import routers
from cmoapi.views import MessageView, PTOView, CategoryView, ResponseView, FamilyMemberRelationshipView, FamilyMemberView, CMOUserView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'messages', MessageView, 'message')
router.register(r'pto', PTOView, 'pto')
router.register(r'categories', CategoryView, 'category')
router.register(r'responses', ResponseView, 'response')
router.register(r'family_member_relationships', FamilyMemberRelationshipView, 'family_member_relationship')
router.register(r'family_members', FamilyMemberView, 'family_member')
router.register(r'cmo_users', CMOUserView, 'cmo_user')

urlpatterns = [
    path('register', register_user),
    path('login', login_user),
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
