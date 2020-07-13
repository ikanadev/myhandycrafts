"""Participants ViewSet."""

# Django REST Framework
from rest_framework import mixins,viewsets
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
#permission
from rest_framework.permissions import  IsAuthenticated,IsAdminUser
from myhandycrafts.fairs.permissions import IsOwner

# Models
from myhandycrafts.fairs.models import Participant,Fair

# Serializer
from myhandycrafts.fairs.serializers import (
    ParticipantModelSerializer,
    ParticipantDetailModelSerializer,
    AddParticipantSerializer,
    UpdateAdminParticipantSerializer,
    JoinParticipantSerializer,
    UpdateParticipantSerializer,
    DeclineParticipantSerializer,
    RejoinParticipantSerializer,
)

# TIME
from django.utils import timezone

#utils
from myhandycrafts.utils.pagination import MyHandycraftsPageNumberPagination


class ParticipantAdminViewSet(mixins.CreateModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.ListModelMixin,
                         mixins.DestroyModelMixin,
                         viewsets.GenericViewSet):
    """Participant  view set
    handle admin CRUD
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = ParticipantModelSerializer
    pagination_class = MyHandycraftsPageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('user',)
    ordering_fields = ('user', 'created_at',)
    ordering = ('user','created_at')

    def dispatch(self, request, *args, **kwargs):
        """Verify that the circle exists."""
        pk = kwargs['fair_id']
        self.fair = get_object_or_404(Fair, pk=pk)
        return super(ParticipantAdminViewSet, self).dispatch(request, *args, **kwargs)


    def get_serializer_context(self):
        return {
            'request_user':self.request.user,
            'fair':self.fair
        }

    def get_serializer_class(self):
        if self.action == 'create':
            return AddParticipantSerializer
        if self.action == 'update':
            return UpdateAdminParticipantSerializer
        if self.action in ['list','retrieve']:
            return ParticipantDetailModelSerializer
        return ParticipantModelSerializer

    def get_queryset(self):
        """Return circle members."""
        return Participant.objects.filter(
            fair=self.fair,
            active=True
        )

    def perform_destroy(self, instance):
        instance.active=False
        instance.deleted_at = timezone.now()
        instance.save()
        """add policies when object is deleted"""

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        participant = serializer.save()
        data = ParticipantDetailModelSerializer(participant).data
        return Response(data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = ParticipantDetailModelSerializer(instance).data
        return Response(data)



class ParticipantViewSet(mixins.CreateModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.ListModelMixin,
                         mixins.DestroyModelMixin,
                         viewsets.GenericViewSet):
    """
    Participant  view set
    handle admin CRUD
    """
    permission_classes = [IsAuthenticated,IsOwner]
    serializer_class = ParticipantModelSerializer
    pagination_class = MyHandycraftsPageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('user',)
    ordering_fields = ('user', 'created_at',)
    ordering = ('user','created_at')

    def dispatch(self, request, *args, **kwargs):
        """Verify that the fair exists."""
        pk = kwargs['fair_id']
        self.fair = get_object_or_404(Fair, pk=pk)
        return super(ParticipantViewSet, self).dispatch(request, *args, **kwargs)


    def get_serializer_context(self):
        return {
            'request_user':self.request.user,
            'fair':self.fair
        }

    def get_serializer_class(self):
        if self.action == 'create':
            return JoinParticipantSerializer
        if self.action == 'update':
            return UpdateParticipantSerializer
        if self.action in ['list','retrieve']:
            return ParticipantDetailModelSerializer
        if self.action == 'decline':
            return DeclineParticipantSerializer
        if self.action == 'rejoin':
            return RejoinParticipantSerializer
        return ParticipantModelSerializer

    def get_queryset(self):
        """Return participant on fairs."""
        return Participant.objects.filter(
            user=self.request.user,
            active=True
        )

    def perform_destroy(self, instance):
        instance.active=False
        instance.deleted_at = timezone.now()
        instance.save()
        """add policies when object is deleted"""

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        participant = serializer.save()
        data = ParticipantDetailModelSerializer(participant).data
        return Response(data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = ParticipantDetailModelSerializer(instance).data
        return Response(data)


    @action(detail=True,methods=['get'])
    def decline(self,request,*arg,**args):
        instance = self.get_object()
        serializer = self.get_serializer(instance,
                                            data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            "state":1,
            "data":ParticipantDetailModelSerializer(instance).data,
            "message":"Declined success"
        }
        return Response(data)

    @action(detail=True, methods=['get'])
    def rejoin(self, request, *arg, **args):
        instance = self.get_object()
        serializer = self.get_serializer(instance,
                                         data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            "state": 1,
            "data": ParticipantDetailModelSerializer(instance).data,
            "message": "Re join success"
        }
        return Response(data)


