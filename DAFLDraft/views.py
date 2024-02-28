import csv
from django import forms
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.timezone import datetime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView, FormView
from django.db.models import Count, Sum
from django.db import transaction
from django.template.defaulttags import register
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from dal import autocomplete
import datetime
from DAFLDraft.filters import PlayerFilter, RosterFilter
from DAFLDraft.forms import RosterForm, EmailLoginForm
from DAFLDraft.models import Player, Owner, Roster, Season, Team
import sesame
from sesame import utils

from django_tables2 import SingleTableMixin, SingleTableView
from DAFLDraft.tables import PlayerTable, RosterTable
from django_filters.views import FilterView

class EmailLoginView(FormView):
    template_name = "DAFLDraft/email_login.html"
    form_class = EmailLoginForm

    def form_valid(self, form):
        # TODO: email magic link to user.
        return render(self.request, "DAFLDraft/email_login_success.html")
    
class EmailLoginView(FormView):
    template_name = "DAFLDraft/email_login.html"
    form_class = EmailLoginForm

    def form_valid(self, form):
        email = form.cleaned_data["email"]

        User = get_user_model()
        user = User.objects.get(email=email)

        link = reverse("login")
        link = self.request.build_absolute_uri(link)
        link += sesame.utils.get_query_string(user)
        print("magic link:", link)

        return render(self.request, "DAFLDraft/email_login_success.html")

@login_required
def TeamProtectionList(request, teamId = None):
    if teamId:
        team = Team.objects.get(id = teamId)
    else:
        owner = get_object_or_404(Owner, username=request.user.username)
        team = get_object_or_404(Team, owner_id=owner.id)
        teamId = team.id
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
    return render(request, "DAFLDraft/team_protection_list_form.html", context)
# def AllProtectionLists(request):
#     # Create the HttpResponse object with the appropriate CSV header.
#     response = HttpResponse(
#         content_type="text/csv",
#         headers={"Content-Disposition": 'attachment; filename="allprotectionlists.csv"'},
#     )

#     writer = csv.writer(response)
#     writer.writerow(["team", "player", "salary", "year"])
#     roster_data = Roster.objects.all().order_by("-team")
#     for contract in roster_data:
#         if contract.active:
#             writer.writerow([contract.team.full_name, contract.player.name, contract.salary, contract.contract_year])

#     return response

# def AllRosters(request):
#     # Create the HttpResponse object with the appropriate CSV header.
#     response = HttpResponse(
#         content_type="text/csv",
#         headers={"Content-Disposition": 'attachment; filename="allrosters.csv"'},
#     )

#     writer = csv.writer(response)
#     writer.writerow(["id", "team_id", "player_id", "team", "player", "salary", "contract_year", "active", "position", "date_added"])
#     roster_data = Roster.objects.all().order_by("-team")
#     for contract in roster_data:
#         active = 0
#         if contract.active:
#             active = 1
#         writer.writerow([contract.id, contract.team.id, contract.player.id, contract.team.full_name, contract.player.name, contract.salary, contract.contract_year, active, contract.position, contract.date_added])

#     return response
def DownloadProtectionLists(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="allprotectionlists.csv"'},
    )

    writer = csv.writer(response)
    writer.writerow(["team", "player", "salary", "year"])
    roster_data = Roster.objects.all().order_by("-team")
    for contract in roster_data:
        if contract.active:
            writer.writerow([contract.team.full_name, contract.player.name, contract.salary, contract.contract_year])

    return response

def DownloadRosters(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="allrosters.csv"'},
    )

    writer = csv.writer(response)
    writer.writerow(["id", "team_id", "player_id", "team", "player", "salary", "contract_year", "active", "position", "date_added"])
    roster_data = Roster.objects.all().order_by("-team")
    for contract in roster_data:
        active = 0
        if contract.active:
            active = 1
        writer.writerow([contract.id, contract.team.id, contract.player.id, contract.team.full_name, contract.player.name, contract.salary, contract.contract_year, active, contract.position, contract.date_added])

    return response

@login_required
def TeamView(request, teamId=None):
    if request.method == "POST":
        new_position = request.POST["position"]
        roster_id = request.POST["id"]
        roster = Roster.objects.all().filter(id = roster_id).first()
        if new_position == "drop":
            roster.delete()
        else:
            roster.position = new_position
            roster.save()
        if teamId:
            return redirect("team-roster", teamId)        
        else:
            return redirect("my-roster")

    if teamId:
        team = Team.objects.get(id = teamId)
    else:
        owner = get_object_or_404(Owner, username=request.user.username)
        team = get_object_or_404(Team, owner_id=owner.id)
        teamId = team.id
    roster_data = Roster.objects.all().filter(team_id = teamId, active = True).order_by("position")
    roster_data_compiled = []
    POSITIONS = ["C","1B","2B","3B","SS","OF","U","UT","P","B"]
    # sorted(roster_data, key=POSITIONS.index)
    totalSalary = 0
    playerCount = 0
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
                playerCount += 1
                totalSalary += ros.salary            
                roster_data_compiled.append(roster_dict)
        else:
            roster_dict = {"id": "", "player_id": "", "name": "", "position": pos, "salary": "", "year": "", "eligible_positions": "" }
            roster_data_compiled.append(roster_dict)

    context = {'team': team, 'roster_data': roster_data_compiled, "player_count": playerCount, "total_salary": totalSalary}
    return render(request, "DAFLDraft/team_form.html", context)

def StandingsView(request):
    allPositions = ["C","1B","2B","3B","SS","OF","U","UT","P"]
    hitterPositions = ["C","1B","2B","3B","SS","OF","U","UT"]
    roster_data = Roster.objects.all().filter(position__in=allPositions, active = True)
    hitter_stats = []
    pitcher_stats = []
    teams = Team.objects.all()
    for team in teams:
        team_ab = 0
        team_hits = 0
        team_hr = 0
        team_runs = 0
        team_rbi = 0
        team_sb = 0
        player_count = 0
        for roster in roster_data.filter(team_id=team.id, position__in=hitterPositions):
            player_count += 1
            team_ab += roster.player.AB
            team_hits += roster.player.Hits
            team_hr += roster.player.HR
            team_runs += roster.player.Runs
            team_rbi += roster.player.RBI
            team_sb += roster.player.SB
        team_avg = round(team_hits/team_ab, 4)
        team_stats = {"team_name": team.full_name, "player_count": player_count, "AB": round(team_ab), "Hits": round(team_hits), "AVG": team_avg, "HR": round(team_hr), "Runs": round(team_runs), "RBI": round(team_rbi), "SB": round(team_sb) }
        hitter_stats.append(team_stats)

        team_ip = 0
        team_er = 0
        team_wins = 0
        team_so = 0
        team_saves = 0
        team_holds = 0
        player_count = 0
        for roster in roster_data.filter(team_id=team.id, position="P"):
            player_count += 1
            team_ip += roster.player.IP
            team_er += roster.player.ER
            team_wins += roster.player.Wins
            team_so += roster.player.SO
            team_saves += roster.player.Saves
            team_holds += roster.player.Holds
        team_era = round(9.0*(team_er/team_ip), 4)
        team_stats = {"team_name": team.full_name, "player_count": player_count, "IP": round(team_ip), "ER": round(team_er), "ERA": team_era, "Wins": round(team_wins), "SO": round(team_so), "Saves": round(team_saves), "Holds": round(team_holds) }
        pitcher_stats.append(team_stats)

    target_hitter_stats = {"team_name": "Targets", "AB": 0, "Hits": 0, "AVG": .270, "HR": 235, "Runs": 770, "RBI": 750, "SB": 130 }
    # hitter_stats.append(target_hitter_stats)
    target_pitcher_stats = {"team_name": "Targets", "IP": 0, "ER": 0, "ERA": 3.6000, "Wins": 80, "SO": 1230, "Saves": 70, "Holds": 40 }
    # pitcher_stats.append(target_pitcher_stats)

    context = {'hitter_stats': hitter_stats, 'pitcher_stats': pitcher_stats, 'hitter_targets': target_hitter_stats, 'pitcher_targets': target_pitcher_stats}
    return render(request, "DAFLDraft/standings.html", context)

@register.filter(name='split')
def split(value): 
    return value.split("|")

def logout_view(request):
    logout(request)

class PlayerListView(ListView):
    model = Player
class FilteredPersonListView(SingleTableMixin, FilterView):
    model = Player
    table_class = PlayerTable
    template_name = 'DAFLDraft/players.html'
    filterset_class = PlayerFilter
class FilteredRosterListView(SingleTableMixin, FilterView):
    model = Roster
    table_class = RosterTable
    template_name = 'DAFLDraft/all_rosters.html'
    filterset_class = RosterFilter
class FilteredProtectionListView(SingleTableMixin, FilterView):
    model = Roster
    table_class = RosterTable
    template_name = 'DAFLDraft/all_protection_lists.html'
    filterset_class = PlayerFilter
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
            position = request.POST["position"]
            if position == "U":
                position = "UT"
            roster = Roster(player=player, team=team, salary=request.POST["salary"], position=position)
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
    return render(request, "DAFLDraft/roster_form.html", context)

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