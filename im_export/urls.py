from django.urls import path
from im_export.views import ExportWmsInventoryHistoryView

urlpatterns = [
    path('export_inventory_changes/', ExportWmsInventoryHistoryView.as_view(), name='export-inventory-changes'),
]
