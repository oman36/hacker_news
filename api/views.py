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
    order = data.get('order') or 'created'

    news = News.objects.order_by(order)[offset:offset + limit]
    dicts = []
    for item in news:
        dicts.append({
            'id': item.id,
            'title': item.title,
            'url': item.url,
            'created': item.created.isoformat(),
        })
    return JsonResponse(dicts, safe=False)
