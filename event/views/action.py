from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from event.api_responses import *
from event.models import Event, Invitation, Registration
from event.serializers import EventSerializer
from rest_framework.response import Response
import datetime


class EventRegisterView(CreateAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            event_id = request.data.get('event_id', None)

            if not event_id:
                return ApiResponse.bad_request("Event ID missing")

            event = Event.objects.get(id=event_id)

            is_invited = False
            invitation = None
            try:
                invitation = Invitation.objects.get(user_id=request.user.id, event_id=event_id)
                is_invited = True
            except:
                pass

            if event.is_public or is_invited:
                if event.current_registration == event.capacity:
                    return ApiResponse.bad_request("Seats full for this event!")

                if Registration.objects.filter(user_id=request.user.id, event_id=event_id):
                    return ApiResponse.bad_request("Already registered")

                already_registered_events = Registration.objects.filter(user_id=request.user.id)

                start = event.date
                end = start + datetime.timedelta(minutes=event.capacity)

                for registration in already_registered_events:
                    registered_event = Event.objects.get(id=registration.event_id)
                    s = registered_event.date
                    e = s + datetime.timedelta(minutes=registered_event.capacity)

                    if end < s or start > e:
                        continue
                    else:
                        return ApiResponse.bad_request("Event overlapping with previously registered event :"+str("event id : "+str(registered_event.id)+" "+registered_event.name))

                obj = Registration.objects.create(user_id=request.user.id, event_id=event_id)
                obj.save()

                event.current_registration = event.current_registration + 1
                event.save()

                if is_invited:
                    invitation.is_accepted = True
                    invitation.save()

                return Response(EventSerializer(event).data)

            else:
                return ApiResponse.forbidden("You are not invited to this private event")

        except Exception as e:
            return ApiResponse.bad_request("Event doesn't exist")


class EventUnregisterView(CreateAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            event_id = request.data.get('event_id', None)
            if not event_id:
                return ApiResponse.bad_request("Event ID missing")

            try:
                obj = Registration.objects.get(event_id=event_id, user_id=request.user.id)
            except:
                obj = None

            if obj:
                obj.delete()
                try:
                    invite = Invitation.objects.get(event_id=event_id, user_id=request.user.id)
                except:
                    invite = None

                if invite:
                    invite.is_accepted = False
                    invite.save()
                event = Event.objects.get(id=event_id)
                event.current_registration = event.current_registration - 1
                event.save()
                return ApiResponse.success("Successfully unregistered")
            else:
                return ApiResponse.forbidden("Not registered to this event")

        except Exception as e:
            return ApiResponse.bad_request("Something went wrong")

class MyRegisteredEventsView(RetrieveAPIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        qSet = Event.objects.filter(registration__user=request.user)
        return Response(EventSerializer(qSet, many=True).data)