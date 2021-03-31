import json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator

from rest_framework.views import APIView

from .models import Game, Character, Combo, Input, Command

class ComboDirectoryView(ListView):
    model = Game
    template_name = "combo_directory.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        games = Game.objects.all()
        characters = Character.objects.all()

        context['games'] = games
        context['characters'] = characters
        return context


class CharacterDetailView(DetailView):
    """This view should display all currently known Combos for a Character in
    the system.
    """
    model = Character
    template_name = "character_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        requested_character = self.object
        combos = Combo.objects.filter(character__id = requested_character.id)

        context['combos'] = combos
        return context


class ComboDetailView(DetailView):
    """This view handles the display and reordering of a Combo.
    """
    model = Combo
    template_name = "combo_display.html"

    def get_context_data(self, **kwargs):
        """We need all of the Inputs for the current Combo, as well as the
        possible Commands for the Character that owns the combo.
        """
        context = super().get_context_data(**kwargs)
        requested_combo = self.object
        inputs = Input.objects.filter(
                               combo__id = requested_combo.id).order_by('order')
        context['inputs'] = inputs
        # get the commands for the game in question
        relevant_commands = Command.objects.filter(
                               game__id = requested_combo.character.game.id)
        # get the commands that are specific to that character
        specific_commands = relevant_commands.filter(
                               character__id = requested_combo.character.id)
        # get the commands that are non character specific.
        generic_commands = relevant_commands.filter(
                               character__id = None
        )
        # the commands that are actually needed is a combined list of each.
        # TODO: might be useful to split these later for smarter display.
        context['commands'] = specific_commands | generic_commands
        return context


    def post(self, request, pk):
        """Handles POST requests. This should accept a given group of Input IDs
        for a Combo, and save their new ordering properly.
        """
        if request.method == "POST" and request.is_ajax():
            try:
                # Parse the JSON payload
                data = json.loads(request.body)[0]
                # Loop over our list order. The id equals the question id.
                # Update the order and save.
                for x,input in enumerate(data):
                    input = Input.objects.get(pk=input['id'])
                    input.order = x + 1
                    input.save()

            except KeyError:
                HttpResponseServerError("Malformed data!")

            return JsonResponse({"success": True}, status=200)
        else:
            return JsonResponse({"success": False}, status=400)


    def put(self, request, **kwargs):
        """Takes PUT requests. The goal here is to create Inputs for a Combo.
        """
        try:
            combo = Combo.objects.get(pk=kwargs['pk'])
        except Combo.DoesNotExist:
            msg = "No Combo was found for this key: {}".format(kwargs['pk'])
            return Response(data=msg, status=status.HTTP_404_NOT_FOUND)
        # the PUT should provide the ID for a command, so create a new input
        # with that ID for this combo. it should be the last in line.
        data = json.loads(request.body)[0]
        command = Command.objects.get(pk=data)
        input_location = Input.objects.filter(combo__id=combo.id).count() + 1
        new_input = Input(combo=combo)
        new_input.command = command
        new_input.order = input_location
        new_input.save()
        
        return JsonResponse({"success": True}, status=200)


class BuilderView(TemplateView):
    template_name = "builder.html"
