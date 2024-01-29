from django import forms
from django_filters import FilterSet, ChoiceFilter
from .models import Player

class PlayerFilter(FilterSet):
    def __init__(self, *args, **kwargs):
       super(PlayerFilter, self).__init__(*args, **kwargs)

    POSITIONS = [("P","P"),("C","C"),("1B","1B"),("2B","2B"),("3B","3B"),("SS","SS"),("OF","OF"),("U","U")]
    eligible_positions=ChoiceFilter(choices=POSITIONS, widget=forms.Select, lookup_expr='contains', label='Position:')
    class Meta:
        model = Player
        fields = {"name": ["contains"]}