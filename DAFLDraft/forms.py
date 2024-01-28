from dal import autocomplete

from django import forms

from .models import Roster, Team, Player

class EmailLoginForm(forms.Form):
    email = forms.EmailField()

class RosterForm(forms.ModelForm):
    player = autocomplete.ModelSelect2(url='player-autocomplete')
    class Meta:
        model = Roster
        fields = ('__all__')
        widgets = {
            'player': autocomplete.ModelSelect2(url='player-autocomplete', attrs={'data-placeholder': 'Enter a player name', 'data-theme': 'bootstrap'})
        }
    # def __init__(self, *args, **kwargs):
    #     super(RosterForm, self).__init__(*args, **kwargs)
    #     for visible in self.visible_fields():
    #         visible.field.widget.attrs['class'] = 'form-control'
class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('__all__')