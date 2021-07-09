from publishers.serializer import CreatePublisherSerializer, PublisherSerializer
from publishers.models import Publisher
from django.shortcuts import render
import rest_framework
from rest_framework.viewsets import ModelViewSet
from core.permissions import GeneralPermissions

class PublisherViewSet(ModelViewSet):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    permission_classes = (GeneralPermissions, )

    def  get_queryset(self):
        data = {}
        if self.request.query_params:
            for k, v in self.request.query_params.items():
                if k == 'page':
                    continue
                data[k] = v
        return self.queryset.filter(**data)

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT']: 
            return CreatePublisherSerializer
        return PublisherSerializer