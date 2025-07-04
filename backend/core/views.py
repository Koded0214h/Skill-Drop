from django.shortcuts import render
from django.contrib.auth import get_user_model

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions, viewsets, generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from .permissions import IsEmployer, IsStudent

from .serializers import ( 
    BadgeSerializer, RegisterSerializer,
    EmployerProfileSerializer, StudentProfileSerializer,
    GigSerializer, ApplicationSerializer,
    UserProfileSerializer, NotificationSerializer
)
from .utils.web3 import mint_badge
from .models import (
    Badge, StudentProfile,
    EmployerProfile, Gig, Application,
    Notification
)

# Create your views here.

User = get_user_model()

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def issue_badge(request):
    recipient = request.data.get("address")
    token_uri = request.data.get("token_uri")  # <-- include token_uri

    if not recipient or not token_uri:
        return Response({"error": "Missing recipient address or token_uri"}, status=400)

    result = mint_badge(recipient, token_uri)

    if result["status"] == "success":
        Badge.objects.create(
            recipient_address=result["recipient"],
            tx_hash=result["tx_hash"],
            block_number=result["blockNumber"]
        )
    return Response(result)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mint_gig_badge(request):
    user = request.user
    if user.role != 'employer':
        return Response({"error": "Only employers can mint badges."}, status=403)

    student_id = request.data.get("student_id")
    gig_id = request.data.get("gig_id")
    feedback = request.data.get("feedback")
    title = request.data.get("title", "Skill Badge")
    image_url = request.data.get("image_url", "")  # Optional

    try:
        student = User.objects.get(id=student_id, role="student")
        gig = Gig.objects.get(id=gig_id, employer=user)
    except User.DoesNotExist:
        return Response({"error": "Student not found."}, status=404)
    except Gig.DoesNotExist:
        return Response({"error": "Gig not found or not yours."}, status=404)

    metadata = {
        "name": title,
        "description": f"Feedback for {student.username} on gig '{gig.title}': {feedback}",
        "attributes": [
            {"trait_type": "Gig", "value": gig.title},
            {"trait_type": "Employer", "value": user.username},
        ],
        "image": image_url or "https://via.placeholder.com/300",  # fallback
    }

    try:
        from .utils.ipfs import upload_to_ipfs
        from .utils.web3 import mint_badge  # already exists

        token_uri = upload_to_ipfs(metadata)
        result = mint_badge(student.wallet_address, token_uri)

        if result["status"] == "success":
            Badge.objects.create(
                recipient_address=student.wallet_address,
                tx_hash=result["tx_hash"],
                block_number=result["blockNumber"]
            )
            return Response({
                "status": "success",
                "message": "Badge minted successfully.",
                "token_uri": token_uri,
                "tx": result
            })

        return Response({"error": result}, status=400)

    except Exception as e:
        return Response({"error": str(e)}, status=500)



@api_view(["GET"])
def list_badges(request):
    badges = Badge.objects.all().order_by("-created_at")
    serializer = BadgeSerializer(badges, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({"status": "success", "user_id": user.id})
    return Response(serializer.errors, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    user = request.user
    return Response({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role,
        "wallet_address": user.wallet_address
    })
    
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    user = request.user

    if request.method == 'GET':
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_student_profile(request):
    serializer = StudentProfileSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_employer_profile(request):
    serializer = EmployerProfileSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


class GigListCreateView(generics.ListCreateAPIView):
    serializer_class = GigSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Gig.objects.all()

    def perform_create(self, serializer):
        serializer.save(employer=self.request.user)


class GigDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Gig.objects.all()
    serializer_class = GigSerializer
    permission_classes = [IsAuthenticated]


class ApplicationListCreateView(generics.ListCreateAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Application.objects.filter(student=self.request.user)

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)
        
class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)