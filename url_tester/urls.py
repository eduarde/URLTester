from django.urls import path
from .views import SessionsListView, SessionDetailView, SessionCreateView, SessionDeleteView, SessionLoadUrl, RunTests, \
    HomeView, ProjectCreateView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('create/', ProjectCreateView.as_view(), name='project_create'),
    path('<slug:proj>/<slug:category>/', SessionsListView.as_view(), name='sessions_list'),
    path('<slug:proj>/<slug:slug>', SessionDetailView.as_view(), name='session_detail'),
    path('<slug:proj>/session/create/', SessionCreateView.as_view(), name='session_create'),
    path('<slug:proj>/session/delete/<slug:session>/', SessionDeleteView.as_view(), name='session_delete'),
    path('<slug:proj>/session/load/<slug:session>/', SessionLoadUrl.as_view(), name='session_load'),
    path('<slug:proj>/session/run/<slug:session>/', RunTests.as_view(), name='session_run'),
]
