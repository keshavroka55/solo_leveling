from django.urls import path
from .views import PersonListCreate, PersonRetrieveUpdateDelete

urlpatterns = [
    path('people/', PersonListCreate.as_view(), name='person-list-create'),
    path('people/<int:pk>/', PersonRetrieveUpdateDelete.as_view(), name='person-rud'),
]
