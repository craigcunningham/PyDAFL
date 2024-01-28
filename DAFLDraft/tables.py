import django_tables2 as tables
from .models import Player

class PlayerTable(tables.Table):
    class Meta:
        model = Player
        template_name = "django_tables2/bootstrap.html"
        fields = ("name", "adp", "value", "elibible_positions", "stat1", "stat2", "stat3", "stat4", "stat5", "stat6")