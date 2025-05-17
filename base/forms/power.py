from django import forms


class FromImageForm(forms.Form):
    from_image = forms.ImageField(required=False, label='Распарсить из картинки')
