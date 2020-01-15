from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from event.api_responses import *
from event.models import Event, Invitation
from event.serializers import EventSerializer
from rest_framework.response import Response
import datetime


class EventCreateView(CreateAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            name = request.data.get('name', '')
            host = request.user
            date = request.data.get('date', '')
            duration = request.data.get('duration', 0)
            is_public = request.data.get('is_public', True)
            capacity = request.data.get('capacity', 0)
            obj = Event.objects.create(name=name, host=host, date=date, duration=duration,
                                       is_public=is_public, capacity=capacity)
            obj.save()
            data = EventSerializer(obj).data
            return Response(data)
        except Exception as e:
            return ApiResponse.bad_request(
                "Unable to add new event, something went wrong! Maybe Use YYYY-MM-DD HH:MM:SS date format")


class EventView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        event_id = self.kwargs.get('event_id', None)
        if not event_id:
            return ApiResponse.bad_request('Event ID missing')
        try:
            event = Event.objects.get(id=event_id)
        except:
            event = None

        if not event:
            return ApiResponse.bad_request("Event Doesn't exist")
        
        if event.is_public:
            data = EventSerializer(event).data
            return Response(data)

        elif event.host.id == request.user.id:
            data = EventSerializer(event).data
            return Response(data)

        elif Invitation.objects.filter(user_id=request.user.id, event_id=event.id):
            data = EventSerializer(event).data
            return Response(data)

        else:
            return ApiResponse.forbidden("You are not allow to view this information")

    def delete(self, request, *args, **kwargs):
        event = Event.objects.filter(id=self.kwargs.get('event_id', None)).first()
        if event is None:
            return ApiResponse.bad_request("Such event doesn't exist!")
        if event.host.id == request.user.id:
            event.delete()
            return ApiResponse.success("Event Deleted")
        else:
            return ApiResponse.forbidden('You are not authorized to perform this action.')


class EventListView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Event.objects.all()

    def get(self, request, *args, **kwargs):
        public_events = Event.objects.filter(is_public=True, date__gt=datetime.datetime.now())
        data = {}
        public_events = EventSerializer(public_events, many=True).data
        data['public_events'] = public_events
        private_event_invitations = Event.objects.filter(is_public=False, invitation__user=request.user)
        private_event_invitations = EventSerializer(private_event_invitations, many=True).data
        data['private_event_invitations'] = private_event_invitations
        return Response(data)


class MyHostedEvents(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        qSet = Event.objects.filter(host=request.user)
        return Response(EventSerializer(qSet, many=True).data)
