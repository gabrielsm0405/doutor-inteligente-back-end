from rest_framework import viewsets, mixins
from rest_framework_api_key.permissions import HasAPIKey
from django.http import HttpResponse
import json
from .models import Keys, Results
from .serializers import ResultSerializer

class InferenceView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Keys.objects.all().order_by('id')
    serializer_class = ResultSerializer
    permission_classes = [HasAPIKey]
    filter_fields = '__all__'

    def makeInferece(self, request):
        key = request.POST.dict()['key']

        keyObj = Keys.objects.filter(key = key)

        if keyObj:
            if keyObj[0].counter < 10:
                originalImage = request.FILES.dict()['originalImage']

                Results.objects.create(key = keyObj[0], originalImage = originalImage)

                keyObj[0].counter = keyObj[0].counter + 1
                keyObj[0].save()

                return HttpResponse(content=json.dumps({'error: ':"The image was succesfull saved"}, ensure_ascii=False).encode('utf8'), status=200)
            else:
                return HttpResponse(content=json.dumps({'error: ':"This key was already used ten times"}, ensure_ascii=False).encode('utf8'), status=400)
        else:
            return HttpResponse(content=json.dumps({'error: ':"There is no key like that"}, ensure_ascii=False).encode('utf8'), status=400)