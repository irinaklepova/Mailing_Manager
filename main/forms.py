from django import forms

from main.models import Client, Message, Mailing


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, forms.BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class ClientForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Client
        exclude = ('owner',)


class MessageForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Message
        exclude = ('owner',)


class MailingForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Mailing
        exclude = ('owner', 'status', 'next_time',)
