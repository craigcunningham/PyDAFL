import datetime
from decimal import Decimal
from django.utils.timezone import now
from django.urls import reverse
from django.db import models

class Owner(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    username = models.CharField(max_length=15, default="")
    class Meta:
        ordering = ["-name"]
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse("owner-list")
class Season(models.Model):
    year = models.IntegerField()
    protection_lists_locked = models.BooleanField()
    
class Team(models.Model):
    full_name = models.CharField(max_length=50, default="")
    short_name = models.CharField(max_length=10, default="")
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    class Meta:
        ordering = ["-full_name"]
    def __str__(self):
        return self.full_name
    def get_absolute_url(self):
        return reverse("team-list")

class Player(models.Model):
    name = models.CharField(max_length=100)
    eligible_positions = models.CharField(max_length=30)
    fangraphs_id = models.CharField(max_length=30)
    cbs_id = models.IntegerField()
    mlb_id = models.IntegerField()
    adp = models.FloatField(default=9999)
    value = models.FloatField(default=0)
    stat1 = models.FloatField(default=0) #HR or Wins
    stat2 = models.FloatField(default=0) #SB or Saves
    stat3 = models.FloatField(default=0) #RBI or SO
    stat4 = models.FloatField(default=0) #Runs or Holds
    stat5 = models.FloatField(default=0) #AB or IP
    stat6 = models.FloatField(default=0) #Hits or ER
    class Meta:
        ordering = ["adp", "-value"]
    
    @property
    def isPitcher(self):
        if "P" in self.eligible_positions:
            return True
        else:
            return False

    @property
    def BA(self):
        if self.stat5 == 0:
            return 0
        else:
            return self.stat6/self.stat5
        
    @property
    def ERA(self):
        if self.stat5 == 0:
            return 0
        else:
            return (self.stat6/self.stat5) * 9.0
        
    @property
    def isPlayerAvailable(self):
        ros = Roster.objects.filter(player_id = self.id, active=True).first()
        if ros:
            return False
        else:
            return True
        
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse("player-detail", kwargs={"pk": self.pk})

class Roster(models.Model):
    POSITIONS = [("P","P"),("C","C"),("1B","1B"),("2B","2B"),("3B","3B"),("SS","SS"),("OF","OF"),("U","U")]
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    position = models.CharField(max_length=2, choices=POSITIONS)
    # position = models.ForeignKey(Position, on_delete=models.CASCADE)
    salary = models.IntegerField()
    contract_year = models.IntegerField(default=1)
    active = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now=True)
    def __str__(self):
        return  self.team.full_name + " - " +self.player.name + " - " + self.position
    def get_absolute_url(self):
        return reverse("roster-list")

# class ModelChoiceIteratorValue:
#     def __init__(self, value, instance):
#         self.value = value
#         self.instance = instance

#     def __str__(self):
#         return str(self.value)

#     def __hash__(self):
#         return hash(self.value)

#     def __eq__(self, other):
#         if isinstance(other, ModelChoiceIteratorValue):
#             other = other.value
#         return self.value == other

# class ModelChoiceIterator:
#     def __init__(self, field):
#         self.field = field
#         self.queryset = field.queryset

#     def __iter__(self):
#         if self.field.empty_label is not None:
#             yield ("", self.field.empty_label)
#         queryset = self.queryset
#         # Can't use iterator() when queryset uses prefetch_related()
#         if not queryset._prefetch_related_lookups:
#             queryset = queryset.iterator()
#         for obj in queryset:
#             yield self.choice(obj)

#     def __len__(self):
#         # count() adds a query but uses less memory since the QuerySet results
#         # won't be cached. In most cases, the choices will only be iterated on,
#         # and __len__() won't be called.
#         return self.queryset.count() + (1 if self.field.empty_label is not None else 0)

#     def __bool__(self):
#         return self.field.empty_label is not None or self.queryset.exists()

#     def choice(self, obj):
#         return (
#             ModelChoiceIteratorValue(self.field.prepare_value(obj), obj),
#             self.field.label_from_instance(obj),
#         )
# class ModelChoiceField(ChoiceField):
#     """A ChoiceField whose choices are a model QuerySet."""

#     # This class is a subclass of ChoiceField for purity, but it doesn't
#     # actually use any of ChoiceField's implementation.
#     default_error_messages = {
#         "invalid_choice": _(
#             "Select a valid choice. That choice is not one of the available choices."
#         ),
#     }
#     iterator = ModelChoiceIterator

#     def __init__(
#         self,
#         queryset,
#         *,
#         empty_label="---------",
#         required=True,
#         widget=None,
#         label=None,
#         initial=None,
#         help_text="",
#         to_field_name=None,
#         limit_choices_to=None,
#         blank=False,
#         **kwargs,
#     ):
#         # Call Field instead of ChoiceField __init__() because we don't need
#         # ChoiceField.__init__().
#         Field.__init__(
#             self,
#             required=required,
#             widget=widget,
#             label=label,
#             initial=initial,
#             help_text=help_text,
#             **kwargs,
#         )
#         if (required and initial is not None) or (
#             isinstance(self.widget, RadioSelect) and not blank
#         ):
#             self.empty_label = None
#         else:
#             self.empty_label = empty_label
#         self.queryset = queryset
#         self.limit_choices_to = limit_choices_to  # limit the queryset later.
#         self.to_field_name = to_field_name

#     def get_limit_choices_to(self):
#         """
#         Return ``limit_choices_to`` for this form field.

#         If it is a callable, invoke it and return the result.
#         """
#         if callable(self.limit_choices_to):
#             return self.limit_choices_to()
#         return self.limit_choices_to

#     def __deepcopy__(self, memo):
#         result = super(ChoiceField, self).__deepcopy__(memo)
#         # Need to force a new ModelChoiceIterator to be created, bug #11183
#         if self.queryset is not None:
#             result.queryset = self.queryset.all()
#         return result

#     def _get_queryset(self):
#         return self._queryset

#     def _set_queryset(self, queryset):
#         self._queryset = None if queryset is None else queryset.all()
#         self.widget.choices = self.choices

#     queryset = property(_get_queryset, _set_queryset)

#     # this method will be used to create object labels by the QuerySetIterator.
#     # Override it to customize the label.
#     def label_from_instance(self, obj):
#         """
#         Convert objects into strings and generate the labels for the choices
#         presented by this object. Subclasses can override this method to
#         customize the display of the choices.
#         """
#         return str(obj)

#     def _get_choices(self):
#         # If self._choices is set, then somebody must have manually set
#         # the property self.choices. In this case, just return self._choices.
#         if hasattr(self, "_choices"):
#             return self._choices

#         # Otherwise, execute the QuerySet in self.queryset to determine the
#         # choices dynamically. Return a fresh ModelChoiceIterator that has not been
#         # consumed. Note that we're instantiating a new ModelChoiceIterator *each*
#         # time _get_choices() is called (and, thus, each time self.choices is
#         # accessed) so that we can ensure the QuerySet has not been consumed. This
#         # construct might look complicated but it allows for lazy evaluation of
#         # the queryset.
#         return self.iterator(self)

#     choices = property(_get_choices, ChoiceField._set_choices)

#     def prepare_value(self, value):
#         if hasattr(value, "_meta"):
#             if self.to_field_name:
#                 return value.serializable_value(self.to_field_name)
#             else:
#                 return value.pk
#         return super().prepare_value(value)

#     def to_python(self, value):
#         if value in self.empty_values:
#             return None
#         try:
#             key = self.to_field_name or "pk"
#             if isinstance(value, self.queryset.model):
#                 value = getattr(value, key)
#             value = self.queryset.get(**{key: value})
#         except (ValueError, TypeError, self.queryset.model.DoesNotExist):
#             raise ValidationError(
#                 self.error_messages["invalid_choice"],
#                 code="invalid_choice",
#                 params={"value": value},
#             )
#         return value

#     def validate(self, value):
#         return Field.validate(self, value)

#     def has_changed(self, initial, data):
#         if self.disabled:
#             return False
#         initial_value = initial if initial is not None else ""
#         data_value = data if data is not None else ""
#         return str(self.prepare_value(initial_value)) != str(data_value)


# class ModelMultipleChoiceField(ModelChoiceField):
#     """A MultipleChoiceField whose choices are a model QuerySet."""

#     widget = SelectMultiple
#     hidden_widget = MultipleHiddenInput
#     default_error_messages = {
#         "invalid_list": _("Enter a list of values."),
#         "invalid_choice": _(
#             "Select a valid choice. %(value)s is not one of the available choices."
#         ),
#         "invalid_pk_value": _("“%(pk)s” is not a valid value."),
#     }

#     def __init__(self, queryset, **kwargs):
#         super().__init__(queryset, empty_label=None, **kwargs)

#     def to_python(self, value):
#         if not value:
#             return []
#         return list(self._check_values(value))

#     def clean(self, value):
#         value = self.prepare_value(value)
#         if self.required and not value:
#             raise ValidationError(self.error_messages["required"], code="required")
#         elif not self.required and not value:
#             return self.queryset.none()
#         if not isinstance(value, (list, tuple)):
#             raise ValidationError(
#                 self.error_messages["invalid_list"],
#                 code="invalid_list",
#             )
#         qs = self._check_values(value)
#         # Since this overrides the inherited ModelChoiceField.clean
#         # we run custom validators here
#         self.run_validators(value)
#         return qs

#     def _check_values(self, value):
#         """
#         Given a list of possible PK values, return a QuerySet of the
#         corresponding objects. Raise a ValidationError if a given value is
#         invalid (not a valid PK, not in the queryset, etc.)
#         """
#         key = self.to_field_name or "pk"
#         # deduplicate given values to avoid creating many querysets or
#         # requiring the database backend deduplicate efficiently.
#         try:
#             value = frozenset(value)
#         except TypeError:
#             # list of lists isn't hashable, for example
#             raise ValidationError(
#                 self.error_messages["invalid_list"],
#                 code="invalid_list",
#             )
#         for pk in value:
#             try:
#                 self.queryset.filter(**{key: pk})
#             except (ValueError, TypeError):
#                 raise ValidationError(
#                     self.error_messages["invalid_pk_value"],
#                     code="invalid_pk_value",
#                     params={"pk": pk},
#                 )
#         qs = self.queryset.filter(**{"%s__in" % key: value})
#         pks = {str(getattr(o, key)) for o in qs}
#         for val in value:
#             if str(val) not in pks:
#                 raise ValidationError(
#                     self.error_messages["invalid_choice"],
#                     code="invalid_choice",
#                     params={"value": val},
#                 )
#         return qs

#     def prepare_value(self, value):
#         if (
#             hasattr(value, "__iter__")
#             and not isinstance(value, str)
#             and not hasattr(value, "_meta")
#         ):
#             prepare_value = super().prepare_value
#             return [prepare_value(v) for v in value]
#         return super().prepare_value(value)

#     def has_changed(self, initial, data):
#         if self.disabled:
#             return False
#         if initial is None:
#             initial = []
#         if data is None:
#             data = []
#         if len(initial) != len(data):
#             return True
#         initial_set = {str(value) for value in self.prepare_value(initial)}
#         data_set = {str(value) for value in data}
#         return data_set != initial_set

