from import_export import resources, fields
from WMS.models import WmsInventoryHistory, WmsReceiptOrder, WmsShipmentOrder, WmsInventoryMovement, WmsItem, WmsRack
from import_export.widgets import ForeignKeyWidget
from im_export.mixins import BaseMixin, VerboseExportMixin


class WmsInventoryHistoryResource(BaseMixin, VerboseExportMixin, resources.ModelResource):
    inventory_movement = fields.Field(
        column_name='inventory_movement',
        attribute='inventory_movement',
        widget=ForeignKeyWidget(WmsInventoryMovement, field='number'))

    inventory_receipt_order = fields.Field(
        column_name='inventory_receipt_order',
        attribute='inventory_receipt_order',
        widget=ForeignKeyWidget(WmsReceiptOrder, field='number'))

    inventory_shipment_order = fields.Field(
        column_name='inventory_shipment_order',
        attribute='inventory_shipment_order',
        widget=ForeignKeyWidget(WmsShipmentOrder, field='number'))

    item = fields.Field(
        column_name='item',
        attribute='item',
        widget=ForeignKeyWidget(WmsItem, field='abs_item__name'))

    item_number = fields.Field(
        column_name='item_number',
        attribute='item',
        widget=ForeignKeyWidget(WmsItem, field='abs_item__number'))

    rack = fields.Field(
        column_name='rack',
        attribute='rack',
        widget=ForeignKeyWidget(WmsRack, field='name'))

    inventory_shipment_order__to_user = fields.Field()

    def dehydrate_inventory_shipment_order__to_user(self, history):
        if hasattr(history, 'inventory_shipment_order') and hasattr(history.inventory_shipment_order, 'to_user'):
            username = getattr(history.inventory_shipment_order.to_user, "username", "unknown")
            nickname = getattr(history.inventory_shipment_order.to_user, "nickname", "unknown")
            return '%s-%s' % (username, nickname)
        else:
            return None

    class Meta:
        model = WmsInventoryHistory
        # export_order = ('title', 'author', 'publication_year')
        exclude = ('id', 'is_show', 'edit_time', 'editor', 'operator')
        # Mixin 自定义参数，自定义字段的表头
        addon_header_dict = {"item_number": "物料编号", "inventory_shipment_order__to_user": "申请人"}
