from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import TaskViewSet, CalendarTaskViewSet, ContactViewSet, UserSingnupView, UserInfoView, UserExistsView


router = DefaultRouter()
# task
router.register("tasks", TaskViewSet, basename="tasks")
router.register("calendartasks", CalendarTaskViewSet, basename="calendartasks")
router.register("contact", ContactViewSet, basename="contact")


urlpatterns = [
    # token
    path("token/", TokenObtainPairView.as_view(),
         name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(),
         name="token_refresh"),
    # Auth
    path("signup/", UserSingnupView.as_view(), name="user_signup"),
    path("user-info/", UserInfoView.as_view(), name="user_info"),
    path("user-exist/", UserExistsView.as_view(), name="users_exist"),
    # password reset
    path("password-reset/", include("django_rest_passwordreset.urls",
         namespace="password_reset")),
] + router.urls
