from django.urls import path, re_path
from event.views import *

urlpatterns = [
    path("event/create/", EventCreateView.as_view()),
    path("event/all/", EventListView.as_view()),
    re_path(r'^event/(?P<event_id>\d+)/$', EventView.as_view()),
    path("event/invite/", EventInviteView.as_view()),
    path("event/revoke/", EventInvitationRevokeView.as_view()),
    path("event/register/", EventRegisterView.as_view()),
    path("event/unregister/", EventUnregisterView.as_view()),
    path("event/sent_invitations/", SentInvitationsView.as_view()),
    path("event/my_registrations/", MyRegisteredEventsView.as_view()),
    path("event/my_hosted_events/", MyHostedEvents.as_view())
]

# documentation = https://documenter.getpostman.com/view/10090782/SWLk4R1H
