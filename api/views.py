from django.forms import model_to_dict
from django.http import JsonResponse

from api.forms import NewsForm
from api.models import News


def posts(request):
    form = NewsForm(request.GET)
    if not form.is_valid():
        return JsonResponse({'errors': form.errors}, status=400)

    data = form.cleaned_data
    offset = 0 if data['offset'] is None else data['offset']
    limit = 5 if data['limit'] is None else data['limit']
    order = data.get('order') or 'created_at'

    news = News.objects.order_by(order)[offset:offset + limit]
    return JsonResponse([model_to_dict(m) for m in news], safe=False)
