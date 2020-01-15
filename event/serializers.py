from rest_framework import serializers
from event.models import Event, Invitation


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        exclude = ('is_public', )

class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = '__all__'