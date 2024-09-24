from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import SignupSerializer, SigninSerializer, UserSerializer, UserLocationRecordSerializer
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, UserLocationRecordTable


class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.save(), status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SigninView(APIView):
    permission_classes = [AllowAny]

    def patch(self, request):
        serializer = SigninSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class GetAllUserTokensView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        users_with_tokens = User.objects.filter(has_token=True)
        data = []
        
        for user in users_with_tokens:
            refresh = RefreshToken.for_user(user)
            user_data = {
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            data.append(user_data)

        return Response(data, status=status.HTTP_200_OK)
    

# POST API to add user location
class PostUserLocationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = UserLocationRecordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # Assign the authenticated user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# GET API to retrieve all locations of the authenticated user
class GetUserLocationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        locations = UserLocationRecordTable.objects.filter(user=request.user)
        serializer = UserLocationRecordSerializer(locations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
