from django import forms
from django.conf import settings
from .models import Product
from django.core.exceptions import ValidationError


def validate_no_spam(value):
    """Проверяет, нет ли в тексте запрещенных слов"""
    for word in settings.FORBIDDEN_WORDS:
        if word in value.lower():
            raise forms.ValidationError(f'Запрещенное слово: {word}')


class ProductForm(forms.ModelForm):
    name = forms.CharField(validators=[validate_no_spam])
    description = forms.CharField(widget=forms.Textarea, validators=[validate_no_spam])

    class Meta:
        model = Product
        exclude = ('created_at', 'updated_at')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'autofocus': True,
            'placeholder': 'Название товара'
        })

        self.fields['price'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Цена (руб.)'
        })

        self.fields['description'].widget.attrs.update({
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Краткое описание товара'
        })

        self.fields['image'].widget.attrs.update({
            'class': 'form-control custom-file-input',
            'data-bs-toggle': 'tooltip',
            'title': 'Загрузите фотографию товара'
        })

        self.fields['category'].widget.attrs.update({
            'class': 'form-select'
        })


        self.fields['name'].help_text = 'Названия должны быть уникальными.'
        self.fields['price'].help_text = 'Цена должна быть положительной.'
        self.fields['image'].help_text = 'Рекомендуемый размер: 800×600 px.'


    def clean_price(self):
        """Проверяет, что цена положительна"""
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise ValidationError('Цена должна быть положительной.')
        return price
