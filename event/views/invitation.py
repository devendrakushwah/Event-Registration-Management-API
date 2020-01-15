from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from event.api_responses import *
from django.contrib.auth.models import User
from event.models import Event, Invitation, Registration
from event.serializers import InvitationSerializer


class EventInviteView(CreateAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        event_id = request.data.get('event_id', None)
        guest_id = request.data.get('guest_id', None)

        if (event_id == None) or (guest_id == None):
            return ApiResponse.bad_request("Parameter missing")

        try:
            event = Event.objects.get(id=event_id)
            guest = User.objects.get(id=guest_id)
        except:
            return ApiResponse.bad_request("Event doesn't exist or the Guest doesn't exist")

        if event.is_public:
            return ApiResponse.bad_request("Public events are open for all")

        if event.capacity == event.current_registration:
            return ApiResponse.bad_request("You cannot invite more users, maximum users registered already")

        if event.host.id != request.user.id:
            return ApiResponse.forbidden("You are not the host of this event")

        try:
            Invitation.objects.get(user_id=guest_id, event_id=event_id)
            return ApiResponse.bad_request("This user is already invited")
        except:
            obj = Invitation.objects.create(user=guest, event=event)
            obj.save()
            return ApiResponse.success("Guest invited")


class EventInvitationRevokeView(CreateAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):

        event_id = request.data.get('event_id', None)
        guest_id = request.data.get('guest_id', None)

        if (not event_id) or (not guest_id):
            return ApiResponse.bad_request("Parameter missing")

        try:
            event = Event.objects.get(id=event_id)
            guest = User.objects.get(id=guest_id)
        except:
            return ApiResponse.bad_request("Event doesn't exist or the Guest doesn't exist")

        if event.host.id != request.user.id:
            return ApiResponse.forbidden("You are not the host of this event")

        try:
            obj = Invitation.objects.get(user_id=guest_id, event_id=event_id)
            obj.delete()
            try:
                reg = Registration.objects.get(user_id=guest_id, event_id=event_id)
                reg.delete()
                event.current_registration = event.current_registration - 1
                event.save()
            except:
                pass
            return ApiResponse.success("Invitaion revoked")
        except:
            return ApiResponse.bad_request("No such invitation")


class SentInvitationsView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        data = Invitation.objects.filter(event__host=request.user)
        return Response(InvitationSerializer(data, many=True).data)
