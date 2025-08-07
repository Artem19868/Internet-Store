from django.urls import path, include
from. import views

urlpatterns = [
   path('/buy/<slug:product_slug>', views.buy, name='buy'),
   path('/write_review/<int:product_id>', views.write_review, name='write_review')

]