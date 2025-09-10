from rest_framework import serializers
from .models import QARecord


class QARecordSerializer(serializers.ModelSerializer):
    """
    Serializer for reading QA records.
    Includes id, question, answer, and created_at fields.
    """

    class Meta:
        model = QARecord
        fields = ["id", "question", "answer", "created_at"]
        read_only_fields = ["id", "answer", "created_at"]


class AskQuestionSerializer(serializers.Serializer):
    """
    Serializer for accepting a question submission.
    Only includes the 'question' field.
    """
    question = serializers.CharField(
        allow_blank=False,
        trim_whitespace=True,
        help_text="The user question to be answered."
    )
