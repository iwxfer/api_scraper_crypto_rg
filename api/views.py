import json

from django.views.generic import View
from api.models import Scraper 
from django.http.response import JsonResponse
from django.utils.timezone import now

class ScraperAPI(View):
    def get(self, request):
        scrapers = Scraper.objects.all()
        scrapers_list = Scraper.to_list(scrapers)
        response = {'scrapers': scrapers_list}
        return JsonResponse(response, safe=False)

    def post(self, request):
        try:
            data = json.loads(request.body)
            scraper = Scraper.objects.create(**data)
            return JsonResponse(scraper.to_dict(), status=200, safe=False) 
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400, safe=False)

    def put(self, request):
        try:
            data = json.loads(request.body)
            if not 'id' in data:
                return JsonResponse({'msg': 'ID is required.'}, status=400)
            
            scraper = Scraper.objects.get(id=data['id'])
            
            for k, v in data.items():
                if k == 'currency':
                    scraper.currency = v
                if k == 'frequency':
                    scraper.frequency = v
                if k == 'value':
                    scraper.value = v
                    scraper.value_updated_at = now
                
            scraper.save()

            return JsonResponse({'msg': 'Scraper updated'}, status=200) 
        except Exception as e:
            import traceback
            return JsonResponse({'error': str(e) + str(traceback.format_exc())}, status=400)


    def delete(self, request):
        try:
            data = json.loads(request.body)
            if not 'id' in data:
                return JsonResponse({'msg': 'ID is required.'}, status=400)
            
            scraper = Scraper.objects.get(id=data['id'])
            scraper.delete()
            
            return JsonResponse({'msg': 'Scraper deleted'}, status=200) 
        except Exception as e:
            
            return JsonResponse({'error': str(e)}, status=400)