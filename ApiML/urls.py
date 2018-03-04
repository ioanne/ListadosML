"""ApiML URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib.auth.decorators import login_required
from django.urls import path
from apps.listing.views import HomeView, ListingsView, ListingTopSeller, ListingHigherPrice
from apps.applicationML.views import HomeApplicationView, AuthorizingView, AuthorizedView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_required(HomeView.as_view())),
    path('authorize', login_required(HomeApplicationView.as_view())),
    path('authorizing', login_required(AuthorizingView.as_view())),
    path('authorized', login_required(AuthorizedView.as_view())),
    path('listados', login_required(ListingsView.as_view())),
    path('listados/top-seller', login_required(ListingTopSeller.as_view())),
    path('listados/higer-price', login_required(ListingHigherPrice.as_view()))
]
    