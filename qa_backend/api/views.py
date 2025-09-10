from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema


from .models import QARecord
from .serializers import QARecordSerializer, AskQuestionSerializer


@api_view(['GET'])
def health(request):
    """
    Simple health check endpoint.

    Returns:
        200 OK with a JSON payload indicating server status.
    """
    return Response({"message": "Server is up!"})


# PUBLIC_INTERFACE
@swagger_auto_schema(
    method="post",
    operation_id="qa_ask_question",
    operation_summary="Submit a question",
    operation_description=(
        "Accepts a user question and returns an answer. For MVP, the answer is generated using "
        "a simple echo pattern. The created Q&A record is returned."
    ),
    request_body=AskQuestionSerializer,
    responses={
        201: QARecordSerializer,
        400: "Bad Request: invalid input"
    },
    tags=["qa"]
)
@api_view(["POST"])
def ask_question(request):
    """
    Submit a question; returns answer and record.

    Body:
        JSON object:
        - question (string): The user question to be answered.

    Returns:
        201 Created:
            QARecord object with fields: id, question, answer, created_at.
        400 Bad Request:
            When the input payload is invalid.
    """
    serializer = AskQuestionSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    question_text = serializer.validated_data["question"]
    # Dummy answer logic (MVP): echo the question with a prefix.
    answer_text = f"You asked: {question_text}"

    record = QARecord.objects.create(question=question_text, answer=answer_text)
    output = QARecordSerializer(record)
    return Response(output.data, status=status.HTTP_201_CREATED)


# PUBLIC_INTERFACE
@swagger_auto_schema(
    method="get",
    operation_id="qa_history",
    operation_summary="Get Q&A history",
    operation_description=(
        "Returns the list of Q&A records sorted by most recent first."
    ),
    responses={200: QARecordSerializer(many=True)},
    tags=["qa"]
)
@api_view(["GET"])
def qa_history(request):
    """
    Get recent Q&A history.

    Query Params:
        None

    Returns:
        200 OK:
            Array of QARecord items sorted by descending created_at.
    """
    records = QARecord.objects.all().order_by("-created_at")
    output = QARecordSerializer(records, many=True)
    return Response(output.data, status=status.HTTP_200_OK)
