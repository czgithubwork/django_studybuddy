from base.models import Room
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.serializer import RoomSerializer
# Create your views here.

@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/rooms/',
        'GET /api/rooms/:id'
        ]
    
    return Response(routes, status=status.HTTP_200_OK)

@api_view(['GET'])
def listRoom(request):
    rooms = Room.objects.all()
    return Response(RoomSerializer(rooms, many=True).data, status=status.HTTP_200_OK)


@api_view(['GET'])
def getRoom(request, pk):
    room = Room.objects.filter(pk=pk)

    if room.exists():
        room = RoomSerializer(room[0])
        return Response(room.data, status=status.HTTP_200_OK)

    return Response({}, status=status.HTTP_404_NOT_FOUND)