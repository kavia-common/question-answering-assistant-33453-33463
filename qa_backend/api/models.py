from django.db import models


class QARecord(models.Model):
    """
    Stores a single Q&A interaction, including the original question, the generated
    answer, and the creation timestamp.
    """
    question = models.TextField(help_text="User-submitted question text.")
    answer = models.TextField(help_text="System-generated answer text.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the record was created.")

    def __str__(self) -> str:
        # Short representation for admin/debug
        return f"QARecord(id={self.id}, created_at={self.created_at})"
