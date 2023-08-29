import logging
from django.test import TestCase
from WMS.models.warehouse import WmsRack, WmsArea, WmsWarehouse
from WMS.models.shipment import WmsShipmentOrderDetail

logger = logging.getLogger(__name__)


class WmsShipmentOrderDetailTestCase(TestCase):
    def setUp(self):
        logger.debug("Creating WmsShipmentOrderDetail object...")
        warehouse_obj = WmsWarehouse.objects.create(number="warehouse1", name="sdkfh")
        area_obj = WmsArea.objects.create(number="area12", name="area12", warehouse=warehouse_obj)
        rack_obj = WmsRack.objects.create(number="rack1", name="rack1", area=area_obj)
        obj = WmsShipmentOrderDetail.objects.create(is_show=False, create_time="2011-09-20 00:00:00",
                                                    edit_time="1985-11-12 00:00:00", creator=None, editor=None,
                                                    shipment_order=None, inventory=None, plan_quantity=44.0,
                                                    real_quantity=100.0, rack=rack_obj, money=3.0, status=68,
                                                    remark="内容品牌标准来源关于.")
        self.pk = obj.id
        self.assertEqual(WmsShipmentOrderDetail.objects.count(), 1)

    def test_update_WmsShipmentOrderDetail(self):
        logger.debug("Updating WmsShipmentOrderDetail object...")
        update_data = {'is_show': True, 'shipment_order': None, 'inventory': None, 'plan_quantity': 43.0,
                       'status': 71}

        # Modify the fields you want to update
        WmsShipmentOrderDetail.objects.filter(pk=self.pk).update(**update_data)

        instance = WmsShipmentOrderDetail.objects.get(pk=self.pk)
        for k, v in update_data.items():
            self.assertEqual(getattr(instance, k), update_data[k])

    def test_delete_WmsShipmentOrderDetail(self):
        logger.debug("Deleting WmsShipmentOrderDetail object...")
        self.assertEqual(WmsShipmentOrderDetail.objects.count(), 1)
        # Delete the instance
        WmsShipmentOrderDetail.objects.filter(pk=self.pk).delete()
        self.assertEqual(WmsShipmentOrderDetail.objects.count(), 0)

    # Add more test methods as needed
