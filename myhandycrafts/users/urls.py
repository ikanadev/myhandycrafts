# from django.urls import path
#
# from myhandycrafts.users.views import (
#     user_redirect_view,
#     user_update_view,
#     user_detail_view,
# )
#
# app_name = "users"
# urlpatterns = [
#     path("~redirect/", view=user_redirect_view, name="redirect"),
#     path("~update/", view=user_update_view, name="update"),
#     path("<str:username>/", view=user_detail_view, name="detail"),
# ]


# Django
from django.urls import include, path
# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import users as user_views

router = DefaultRouter()
router.register(r'a/users', user_views.UserAdminViewSet, basename='admin/users')
router.register(r'a/users_list', user_views.UserListAdminViewSet, basename='admin/users_list')
router.register(r'u/users', user_views.UserUserViewSet, basename='user/users')
router.register(r'users', user_views.UserClientViewSet, basename='client/users')

urlpatterns = [
    path('', include(router.urls)),
]

