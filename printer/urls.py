from django.urls import path

from printer.views import PrintableObjectView

urlpatterns = [
    path('detail/<pk>', PrintableObjectView.as_view(), name='printer'),
]
