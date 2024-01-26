from django import forms
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.timezone import datetime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.shortcuts import render
from django.db.models import Count, Sum
from django.db import transaction
from django.template.defaulttags import register
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from dal import autocomplete
import datetime
from DAFLDraft.forms import RosterForm, TeamForm
from DAFLDraft.models import Player, Owner, Roster, Season, Team

def DAFLLogin(request, username, password):
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        owner = get_object_or_404(Owner, username=username)
        team = get_object_or_404(Team, owner_id=owner.id)
        year = datetime.date.today().year
        season = get_object_or_404(Season, year=year)
        if season.protection_lists_locked:
            return redirect("team-roster", team.id)
        else:
            return redirect("team-protection-list", team.id)

# @login_required
def TeamProtectionList(request, teamId = None):
    if teamId:
        team = Team.objects.get(id = teamId)
    else:
        owner = get_object_or_404(Owner, username=request.user.username)
        team = get_object_or_404(Team, owner_id=owner.id)
    if request.method == "POST":
        with transaction.atomic():
            teamRoster = Roster.objects.all().filter(team_id = team.id)
            teamRoster.update(active=False)
            for ros_id in request.POST.getlist('protect'):
                protected = Roster.objects.get(id = ros_id)
                protected.active = True
                protected.save()

        return redirect("team-protection-list", teamId)        

    season = get_object_or_404(Season, year=datetime.date.today().year)
    roster_data = Roster.objects.all().filter(team_id = team.id).order_by("-active", "-salary")
    totalSalary = 0
    playerCount = 0
    for contract in roster_data:
        if contract.active:
            playerCount += 1
            totalSalary += contract.salary
    context = {'team': team, 'roster_data': roster_data, 'protection_lists_locked': season.protection_lists_locked, 'total_salary': totalSalary, 'player_count': playerCount}
    return render(request, "DAFLDraft\\team_protection_list_form.html", context)

def TeamView(request, teamId=None):
    if request.method == "POST":
        new_position = request.POST["position"]
        roster_id = request.POST["id"]
        roster = Roster.objects.all().filter(id = roster_id).first()
        roster.position = new_position
        roster.save()
        return redirect("team-roster", teamId)        

    if teamId:
        team = Team.objects.get(id = teamId)
    else:
        owner = get_object_or_404(Owner, username=request.user.username)
        team = get_object_or_404(Team, owner_id=owner.id)
    roster_data = Roster.objects.all().filter(team_id = teamId).order_by("position")
    roster_data_compiled = []
    POSITIONS = ["C","1B","2B","3B","SS","OF","U","P","B"]
    # sorted(roster_data, key=POSITIONS.index)
    for pos in POSITIONS:
        roster_position = roster_data.filter(position__exact = pos)
        counter = 1
        if roster_position:
            for ros in roster_position:
                roster_dict = {"id": "", "player_id": "", "name": "", "position": pos, "salary": "", "year": "", "eligible_positions": "" }
                roster_dict["id"] = ros.id
                roster_dict["player_id"] = ros.player.id
                roster_dict["name"] = ros.player.name
                roster_dict["position"] = ros.position
                if counter > 1:
                    roster_dict["position"] = roster_dict["position"] + " - " + str(counter)
                roster_dict["salary"] = ros.salary
                roster_dict["contract_year"] = ros.contract_year
                roster_dict["eligible_positions"] = ros.player.eligible_positions
                counter += 1
                roster_data_compiled.append(roster_dict)
        else:
            roster_dict = {"id": "", "player_id": "", "name": "", "position": pos, "salary": "", "year": "", "eligible_positions": "" }
            roster_data_compiled.append(roster_dict)

    context = {'team': team, 'roster_data': roster_data_compiled}
    return render(request, "DAFLDraft\\team_form.html", context)

@register.filter(name='split')
def split(value): 
    return value.split("|")

def logout_view(request):
    logout(request)

class PlayerListView(ListView):
    model = Player
class PlayerDetailView(DetailView):
    model = Player
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context
class PlayerCreateView(CreateView):
    model = Player
    fields = ["name","fangraphs_id","cbs_id","mlb_id"]
    success_url = reverse_lazy("player-list")
class PlayerUpdateView(UpdateView):
    model = Player
    fields = ["name","fangraphs_id","cbs_id","mlb_id"]
    success_url = reverse_lazy("player-list")
class PlayerDeleteView(DeleteView):
    model = Player
    success_url = reverse_lazy("player-list")

class OwnerListView(ListView):
    model = Owner
class OwnerDetailView(DetailView):
    model = Owner
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context
class OwnerCreateView(CreateView):
    model = Owner
    fields = ["name", "email"]
    success_url = reverse_lazy("owner-list")
class OwnerUpdateView(UpdateView):
    model = Owner
    fields = ["name", "email"]
    success_url = reverse_lazy("owner-list")
class OwnerDeleteView(DeleteView):
    model = Owner
    success_url = reverse_lazy("owner-list")

class TeamListView(ListView):
    model = Team
class TeamDetailView(DetailView):
    model = Team
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context

class TeamCreateView(CreateView):
    model = Team
    owner = forms.ModelMultipleChoiceField(queryset=Owner.objects.all())
    fields = ["full_name","short_name", "owner"]
class TeamUpdateView(UpdateView):
    model = Team
    fields = ["full_name","short_name", "owner"]
class TeamDeleteView(DeleteView):
    model = Team
    success_url = reverse_lazy("team-list")

class RosterListView(ListView):
    model = Roster
def RosterCreateView(request):
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = RosterForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            player = get_object_or_404(Player, id=request.POST["player"])
            team = get_object_or_404(Team, id=request.POST["team"])
            roster = Roster(player=player, team=team, salary=request.POST["salary"], position=request.POST["position"])
            roster.save()
            form = RosterForm()
            return redirect("roster-add")
    else:
        form = RosterForm()
    roster_totals = Roster.objects.filter(active=True).values("team").annotate(TotalSalary=Sum("salary"), PlayerCount=Count("player_id")).order_by("TotalSalary")
    roster_counts = Roster.objects.filter(active=True).values("team", "position").annotate(num=Count("player_id")).order_by("num")
    cc = list(roster_counts)
    totals = list(roster_totals)
    roster_data = []
    POSITIONS = ["P","C", "1B","2B","3B","SS","OF", "UT"]
    for team in Team.objects.all().order_by("short_name"):
        roster_dict = { "team_id":team.id, "team_name":team.short_name, "C":0, "1B":0, "2B":0, "3B":0, "SS":0, "OF":0, "UT":0, "P":0, "B":0, "TotalSalary":0, "MoneyLeft":0, "MaxBid":0 }
        for pos in POSITIONS:
            c = next((item for item in cc if item["team"] == team.id and item["position"] == pos), False)
            if c:
                roster_dict[pos] = c["num"]

        team_total_salary = next((item for item in totals if item["team"] == team.id), False)
        if team_total_salary:
            roster_dict["TotalSalary"] = team_total_salary["TotalSalary"]
            roster_dict["MoneyLeft"] = 260 - team_total_salary["TotalSalary"]
            roster_dict["MaxBid"] = (260 - team_total_salary["TotalSalary"]) - (25 - team_total_salary["PlayerCount"]) + 1

        roster_data.append(roster_dict)
    for ros in roster_counts:
        pos = ros["position"]
        teamid = ros["team"]
    context = {'form': form, 'roster_data': roster_data}
    return render(request, "DAFLDraft\\roster_form.html", context)

def GetPositionsForPlayer(request, playerId):
    player = Player.objects.all().filter(id = playerId).first()
    eligiblePositions = player.eligible_positions.strip()
    return JsonResponse({'eligible_positions': eligiblePositions})

class PlayerAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Player.objects.none()

        qs = Player.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


def home(request):
    return HttpResponse("Hello, Django!")

def hello_there(request, name):
    return render(
        request,
        'DAFLDraft/hello_there.html',
        {
            'name': name,
            'date': datetime.now()
        }
    )
def home(request):
    return render(request, "DAFLDraft/home.html")

def about(request):
    return render(request, "DAFLDraft/about.html")

def contact(request):
    return render(request, "DAFLDraft/contact.html")


def BasicDALView(request):
    js = """
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.1/jquery.js" crossorigin="anonymous"></script>
    """
    dal_media = autocomplete.Select2().media
    url = reverse_lazy('player-autocomplete')
    field = forms.ModelMultipleChoiceField(Player.objects.all())
    widget = autocomplete.ModelSelect2(url=url, attrs={"class": "selector", "id": id, "data-placeholder": "Placeholder"})

    widget.choices = forms.models.ModelChoiceIterator(field)
    default = None
    widget_html = widget.render(Roster.__name__, default)
    html = f"<head>{js}\n{dal_media}</head><body><p>{widget_html}</p></body>"

    return HttpResponse(html)