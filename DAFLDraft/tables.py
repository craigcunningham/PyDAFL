import django_tables2 as tables
from .models import Player

def calculate_row_class(**kwargs):
    """ callables will be called with optional keyword arguments record and table 
    https://django-tables2.readthedocs.io/en/stable/pages/column-attributes.html?highlight=row_attrs#row-attributes
    """
    player = kwargs.get("record", None)
    if player:
        if not player.isPlayerAvailable:
            return "playerTaken"
    return ""

class PlayerTable(tables.Table):
    def render_adp(self, value, record):
        return '{:2.1f}'.format(value)
    def render_value(self, value, record):
        return '${:2.2f}'.format(value)
    def render_stat1(self, value, record):
        return '{:2.1f}'.format(value)
    def render_stat2(self, value, record):
        return '{:2.1f}'.format(value)
    def render_stat3(self, value, record):
        return '{:2.1f}'.format(value)
    def render_stat4(self, value, record):
        return '{:2.1f}'.format(value)
    def render_stat5(self, value, record):
        return '{:2.1f}'.format(value)
    def render_stat6(self, value, record):
        return '{:2.1f}'.format(value)
    def render_BAorERA(self, value, record):
        return '{:4.4f}'.format(value)
    
    class Meta:
        model = Player
        template_name = "django_tables2/bootstrap5.html"
        fields = ("name", "adp", "value", "eligible_positions", "stat5", "stat6", "BAorERA", "stat1", "stat2", "stat3", "stat4")
        f_adp = tables.Column(verbose_name= 'ADP')
        attrs = {"class": "table table-striped"}
        row_attrs = {
            "class": calculate_row_class
        }
