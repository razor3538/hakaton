from django.urls import path

from .views import TetrisView

urlpatterns = [
    path('calculate', TetrisView.as_view()),
]