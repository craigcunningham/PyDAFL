from django import forms
from django_filters import FilterSet, ChoiceFilter, CharFilter, ModelChoiceFilter
from .models import Player, Roster, Team

class PlayerFilter(FilterSet):
    def __init__(self, *args, **kwargs):
       super(PlayerFilter, self).__init__(*args, **kwargs)

    POSITIONS = [("P","P"),("C","C"),("1B","1B"),("2B","2B"),("3B","3B"),("SS","SS"),("OF","OF"),("U","U")]
    eligible_positions=ChoiceFilter(choices=POSITIONS, widget=forms.Select, lookup_expr='contains', label='Position:')
    class Meta:
        model = Player
        fields = {"name": ["contains"]}
class RosterFilter(FilterSet):
    def __init__(self, *args, **kwargs):
       super(RosterFilter, self).__init__(*args, **kwargs)

    # POSITIONS = [("P","P"),("C","C"),("1B","1B"),("2B","2B"),("3B","3B"),("SS","SS"),("OF","OF"),("U","U")]
    # player__eligible_positions=ChoiceFilter(choices=POSITIONS, widget=forms.Select, lookup_expr='contains', label='Position:')
    player__name=CharFilter(lookup_expr="contains", label="Name")
    team_id=ModelChoiceFilter(queryset=Team.objects.all(), widget=forms.Select)
    class Meta:
        model = Roster
        fields = {}