from django import forms

ORDER_CHOICES = (
    ('-title', '-title'),
    ('title', 'title'),
    ('-url', '-url'),
    ('url', 'url'),
    ('-created_at', '-created_at'),
    ('created_at', 'created_at'),
)


class NewsForm(forms.Form):
    order = forms.ChoiceField(choices=ORDER_CHOICES, required=False)
    limit = forms.IntegerField(required=False)
    offset = forms.IntegerField(required=False)
