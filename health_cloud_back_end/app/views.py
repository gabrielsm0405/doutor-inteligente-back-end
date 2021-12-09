from rest_framework import viewsets, mixins
from rest_framework_api_key.permissions import HasAPIKey
from django.http import HttpResponse
import json
from .models import Keys, Results
from .serializers import ResultSerializer
from .AImodel.model import get_results

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

                ResultObj = Results.objects.create(key = keyObj[0], originalImage = originalImage)
                keyObj[0].counter = keyObj[0].counter + 1
                keyObj[0].save()
                
                try: 
                    results = get_results(ResultObj.originalImage.path)

                    for result in results:
                        ResultObj.heatmaps_links.create(pathology = result['pathology'], link=result['heatmap_link'])
                    ResultObj.save()

                    return HttpResponse(content=json.dumps(results, ensure_ascii=False).encode('utf8'), status=200)
                except Exception as e:
                    print(str(e))

                    ResultObj.delete()

                    return HttpResponse(content=json.dumps({'error':"Falha executando o modelo"}, ensure_ascii=False).encode('utf8'), status=400)
            else:
                return HttpResponse(content=json.dumps({'error':"Essa chave de acesso foi utilizada 10 vezes"}, ensure_ascii=False).encode('utf8'), status=400)
        else:
            return HttpResponse(content=json.dumps({'error':"Chave de acesso inválida"}, ensure_ascii=False).encode('utf8'), status=400)