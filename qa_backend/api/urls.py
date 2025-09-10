from django.urls import path
from .views import health, ask_question, qa_history

urlpatterns = [
    path('health/', health, name='Health'),
    path('qa/ask', ask_question, name='qa_ask'),
    path('qa/history', qa_history, name='qa_history'),
]
