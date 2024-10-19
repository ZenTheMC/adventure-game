from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Room, Item, PlayerState
from django.contrib.auth.models import User

# Create your views here.
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def initialize_game(request):
    user = request.user
    try:
        player_state = PlayerState.objects.get(user=user)
        return Response({'message': 'Game already initialized.'})
    except PlayerState.DoesNotExist:
        # Initialize player state
        starting_room = Room.objects.get(name='Living Room')
        player_state = PlayerState.objects.create(user=user, current_room=starting_room)
        return Response({'message': 'Game initialized.'})
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_game_state(request):
    player_state = PlayerState.objects.get(user=request.user)
    room = player_state.current_room
    items = Item.objects.filter(location=room)
    inventory_items = player_state.inventory.all()
    return Response({
        'current_room': {
            'name': room.name,
            'description': room.description,
            'items': [{'name': item.name, 'description': item.description} for item in items],
        },
        'inventory': [{'name': item.name, 'description': item.description} for item in inventory_items],
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def move(request):
    direction = request.data.get('direction')
    # Implement logic to update player_state.current_room based on direction
    # For simplicity, we'll assume the Room model has a method get_room_in_direction()
    player_state = PlayerState.objects.get(user=request.user)
    new_room = player_state.current_room.get_room_in_direction(direction)
    if new_room:
        player_state.current_room = new_room
        player_state.save()
        return Response({'message': f'Moved to {new_room.name}.'})
    else:
        return Response({'message': 'You can\'t go that way.'}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def pick_up_item(request):
    item_name = request.data.get('item_name')
    player_state = PlayerState.objects.get(user=request.user)
    try:
        item = Item.objects.get(name=item_name, location=player_state.current_room)
        player_state.inventory.add(item)
        item.location = None
        item.save()
        return Response({'message': f'Picked up {item.name}.'})
    except Item.DoesNotExist:
        return Response({'message': 'Item not found.'}, status=400)

# You'll need to implement similar endpoints for other actions like look, talk, etc.