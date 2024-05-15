from django.urls import path, include
from rest_framework.routers import DefaultRouter
from memberships.api import MembershipViewSet, CompanyMembershipViewSet, PurchaseMembershipView, \
    MembershipPaymentSuccessView

router = DefaultRouter()
router.register(r'types', MembershipViewSet)
router.register(r'company-memberships', CompanyMembershipViewSet)

api_urls = ([
    path('', include(router.urls)),
    path('purchase/<int:company_id>/<int:membership_id>/', PurchaseMembershipView.as_view(), name='purchase_membership'),
    path('success/', MembershipPaymentSuccessView.as_view(), name='membership_success'),
], 'memberships')

urlpatterns = []
