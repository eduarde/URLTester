from django.urls import path
from .views import SessionsListView, SessionDetailView, SessionCreateView, SessionDeleteView, SessionLoadUrl, RunTests

urlpatterns = [
    path('<slug:category>/', SessionsListView.as_view(), name='sessions_list'),
    path('<int:pk>', SessionDetailView.as_view(), name='session_detail'),
    path('session/create/', SessionCreateView.as_view(), name='session_create'),
    path('session/delete/<int:pk>/', SessionDeleteView.as_view(), name='session_delete'),
    path('session/load/<int:pk>/', SessionLoadUrl.as_view(), name='session_load'),
    path('session/run/<int:pk>/', RunTests.as_view(), name='session_run'),
]
