from django.urls import path

from . import views

urlpatterns = [
    path('',
         views.ComboDirectoryView.as_view(),
         name='directory'),

    path('character/<int:pk>/',
         views.CharacterDetailView.as_view(),
         name='character_detail'),

    path('character/combo/<int:pk>/',
         views.ComboDetailView.as_view(),
         name='combo_display'),

    path('builder',
         views.BuilderView.as_view(),
         name='builder'),
]
