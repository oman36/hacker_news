from django import forms

ORDER_CHOICES = (
    ('-title', '-title'),
    ('title', 'title'),
    ('-url', '-url'),
    ('url', 'url'),
    ('-created', '-created'),
    ('created', 'created'),
)


class NewsForm(forms.Form):
    order = forms.ChoiceField(choices=ORDER_CHOICES, required=False)
    limit = forms.IntegerField(required=False, min_value=1)
    offset = forms.IntegerField(required=False, min_value=0)
