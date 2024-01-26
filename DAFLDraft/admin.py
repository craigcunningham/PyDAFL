from django.contrib import admin

from DAFLDraft.models import Team, Owner, Roster, Player, Season

# Register your models here.
admin.site.register(Team)
admin.site.register(Owner)
admin.site.register(Roster)
admin.site.register(Player)
admin.site.register(Season)

class RosterAdmin(admin.ModelAdmin):
    list_display = ("person.name", "team.name", "position")