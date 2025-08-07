from .models import ReviewRating
from django.forms import ModelForm

class FormReview(ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['rating', 'review']