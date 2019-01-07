from django.urls import path
from .views import SessionsListView, SessionDetailView

urlpatterns = [
    path('', SessionsListView.as_view(), name='sessions_list'),
    path('<int:pk>', SessionDetailView.as_view(), name='session_detail'),
]