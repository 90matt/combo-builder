from django.db import models

# base objects to work with
class Game(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Character(models.Model):
    name = models.CharField(max_length=255)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Command(models.Model):
    """
    A Command is an option that is available to all either all Characters in
    a Game, or a single Character within that Game. This can be as simple as
    pressing forward or backwards, or as detailed as a complete attack.
    """
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    character = models.ForeignKey(Character,
                                  blank=True,
                                  null=True,
                                  on_delete=models.CASCADE)
    # how should this be stored...? a string representation and image pairing?
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text


# combo oriented objects
class Combo(models.Model):
    """
    A Combo can be defined for a single Character as the Sequence of Inputs
    required to perform the Combo.
    """
    character = models.ForeignKey(Character, on_delete=models.CASCADE)

    def __str__(self):
        combo_text = ""
        inputs = Input.objects.filter(combo__id = self.id).order_by('order')
        for input in inputs:
            combo_text += input.command.text + " "
        if not combo_text:
            combo_text = "{} - No inputs available.".format(self.character.name)
        return combo_text


class Input(models.Model):
    command = models.ForeignKey(Command, on_delete=models.CASCADE)
    combo = models.ForeignKey(Combo, on_delete=models.CASCADE, default=None)
    order = models.IntegerField()

    class Meta():
        ordering = ['order',]
