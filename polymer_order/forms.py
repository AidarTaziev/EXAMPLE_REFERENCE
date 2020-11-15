from django.forms import ModelForm
from polymer_order.models import Orders

class PolymerOrderForm(ModelForm):
    class Meta:
        model = Orders
        fields = ['idgoods', 'numbers', 'consignee', 'shipment_from', 'shipment_to', 'idshipment_conditions', 'idshipment_methods',
                  'address', 'contact_name', 'contact_phone', 'contact_email', 'message', 'order_datetime']