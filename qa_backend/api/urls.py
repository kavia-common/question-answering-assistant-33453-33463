from django.urls import path
from .views import health, ask_question, qa_history

# Explicit app namespace for reverse lookups and clarity
app_name = "api"

urlpatterns = [
    # Health endpoint remains with trailing slash
    path('health/', health, name='Health'),

    # Ensure QA endpoints include trailing slashes for consistency under /api/
    # Final routes:
    #   POST /api/qa/ask/
    #   GET  /api/qa/history/
    path('qa/ask/', ask_question, name='qa_ask'),
    path('qa/history/', qa_history, name='qa_history'),
]
