from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import ValueViewset, SkillViewset, ExperienceViewset, CurrentUser, UserDetail, UserSignup, Home

router = DefaultRouter()
router.register(r'Value', ValueViewset)
router.register(r'Skill', SkillViewset)
router.register(r'Experience', ExperienceViewset)

urlpatterns = [
    path('', Home.as_view()),
    path('vse/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('user/', CurrentUser.as_view(), name="current-user"),
    path('user/<int:pk>/', UserDetail.as_view(), name="user-detail"),
    path('signup/', UserSignup.as_view(), name="signup"),
    path('token_pair/', TokenObtainPairView.as_view(), name="token-pair"),
    path('token_refresh/', TokenRefreshView.as_view(), name="token-refresh"),
]