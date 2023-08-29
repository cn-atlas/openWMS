from .WmsItemType import WmsItemTypeViewSet
from .WmsItem import WmsItemViewSet
from .WmsWarehouse import WmsWarehouseViewSet
from .WmsArea import WmsAreaViewSet
from .WmsRack import WmsRackViewSet
from .WmsReceiptOrder import WmsReceiptOrderViewSet
from .WmsReceiptOrderDetail import WmsReceiptOrderDetailViewSet
from .WmsShipmentOrder import WmsShipmentOrderViewSet
from .WmsShipmentOrderDetail import WmsShipmentOrderDetailViewSet
from .WmsDelivery import WmsDeliveryViewSet
from .WmsInventory import WmsInventoryViewSet
from .WmsInventoryCheck import WmsInventoryCheckViewSet
from .WmsInventoryCheckDetail import WmsInventoryCheckDetailViewSet
from .WmsInventoryMovement import WmsInventoryMovementViewSet
from .WmsInventoryMovementDetail import WmsInventoryMovementDetailViewSet
from .WmsInventoryHistory import WmsInventoryHistoryViewSet
from .WmsAbsItem import WmsAbsItemViewSet
from .WmsSupplier import WmsSupplierViewSet

# https://qiita.com/okoppe8/items/77f7f91f6878e3f324cc
# lookup_exprに指定できる値の一覧（一部）
# ・テキスト
#
# lookup_expr	検索方法
# exact	完全一致
# contains	部分一致
# startswith	前方一致
# endswith	後方一致
# regex	正規表現
# ・数値・日時・テキスト（アスキー順）
#
# lookup_expr	検索方法
# gt	超
# lt	未満
# gte	以上
# lte	以下
# 日時
#
# ・時刻の一部に一致する検索が可能
#
# lookup_expr	検索方法
# date	日付(YYYY-M-D)
# year	年(YYYY)
# month	月(M)
# day	日(D)
# week_day	(1-7 日曜が1)
# hour	時(H)
# minute	分(m)
# second	秒(s)

