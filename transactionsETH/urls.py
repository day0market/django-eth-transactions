from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter

import main.views as main_views

router = DefaultRouter()
router.register(r'accounts', main_views.ApiAccountViewSet)
router.register(r'transactions', main_views.ApiTransactionsViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
    path('admin/', admin.site.urls),
    url(r'^$', main_views.redirect_to_api)
]
