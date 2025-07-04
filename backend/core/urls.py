from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register(r'notifications', views.NotificationViewSet, basename='notifications')
router.register(r'notifications', views.NotificationViewSet, basename='notifications')


urlpatterns = [
    path("mint-badge/", views.issue_badge, name="mint-badge"),
    path("mint-gig-badge/", views.mint_gig_badge, name="mint-gig-badge"),
    path("badges/", views.list_badges, name="list-badges"),
    path("auth/register/", views.register_user),
    path("auth/me/", views.get_current_user),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("auth/profile/", views.user_profile, name="user-profile"),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/student/', views.create_student_profile, name='create-student-profile'),
    path('profile/employer/', views.create_employer_profile, name='create-employer-profile'),
    path("gigs/", views.GigListCreateView.as_view(), name="gig-list"),
    path("gigs/<int:pk>/", views.GigDetailView.as_view(), name="gig-detail"),
    path("applications/", views.ApplicationListCreateView.as_view(), name="applications"),
]

urlpatterns += router.urls