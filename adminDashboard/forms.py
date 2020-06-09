from . import models


class UserRegistrationForm(models.Model):
    class Meta:
        model = user
        fields = __all__

        