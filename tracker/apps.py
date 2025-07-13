from django.apps import AppConfig


class TrackerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tracker'

#I want to award scores to everyone upon their carbon footprints. The people with low carbon footprint scores more and the people with higher carbon footprint scores less. Then the person entering with their accounts can input only once a day .  Give 