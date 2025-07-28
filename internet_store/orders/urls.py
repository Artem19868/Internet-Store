from django.urls import path, include
from. import views

urlpatterns = [
   path('/buy/<slug:product_slug>', views.buy, name='buy')

]