# openWMS

## openWMS 仓储物流系统

### 仓库架构：

仓库 - 库区 - 货架

### 物料结构

```
一级分类

   二级分类(可无)

       三级分类（可无）

           物料
```

### 当前库存

WmsInventory 用来存储当前所有品类库存，不直接修改，任何单据导致的库存变化都通过信号传递过来

### 出入库流程

* 入库

入库分为 采购和调仓

入库单状态：0: 按计划入库, 1: 待入库, 2: 取消入库, 3:部分入库， 其中 0: 所有物料按照计划数量入库 3：可能某种物料未入库或者某种物料未按照计划数量入库

入库详情状态：0: 按计划入库, 1: 待入库, 2: 取消入库, 3:部分入库， 其中 3：未按照计划数量入库

* 出库

出库分为 领用（发货）和调仓

出库单状态：-1: 审批拒绝，0: 按计划出库, 1: 出库审批中, 2: 待出库, 3: 部分出库, 4: 取消出库 其中：3：可能某种物料未入库或者某种物料未按照计划数量入库

出库详情状态：-1: 审批拒绝，0: 按计划出库, 1: 出库审批中, 2: 待出库, 3: 部分出库, 4: 取消出库

无论是入库（0、3）、出库（0，3）和调整，都要立即更改库存（WmsInventory）

发货记录属于附加功能

### 移动库存流程

移库单状态： -1：审核拒绝，0: 待审核，1：待移动，2：移动完成，3：取消移动

### 库存盘点

用来记录当期库存盈亏

### 库存变动记录

用来记录所有库存变动记录，跟当前库存一样 不直接修改，任何单据导致的库存变化都通过信号传递过来