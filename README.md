# open WMS 系统

## 企业仓储物流系统

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

库存扣减时机：单据审批完成之后减掉库存

WmsInventory 用来存储当前所有品类库存，不直接修改，任何单据导致的库存变化都通过信号传递过来

### 出入库流程

* 入库

入库分为 采购和调仓

入库单状态：-2: 取消入库，1: 待入库, 2:部分入库，3:按计划入库， 其中 3: 所有物料按照计划数量入库 2：可能某种物料未入库或者某种物料未按照计划数量入库

入库详情状态：-2: 取消入库，1: 待入库, 2:部分入库，3:按计划入库， 其中 2：未按照计划数量入库

入库（1、2）和调整，都要立即更改库存（WmsInventory）

* 出库

出库分为 领用（发货）和调仓

出库类型： 1、物料申请单 2、出库单

出库单状态：-2：取消出库，-1: 审批拒绝，0: 出库审批中, 1: 待出库, 2: 部分出库， 3: 按计划出库 其中：2：可能某种物料未入库或者某种物料未按照计划数量入库

出库详情状态：-2：取消出库，-1: 审批拒绝，0: 出库审批中, 1: 待出库, 2: 部分出库， 3: 按计划出库

出库（2、3）和调整，都要立即更改库存（WmsInventory）

发货记录属于附加功能

### 移动库存流程

移库单状态： -2：取消移动， -1：审核拒绝，0: 移库审批中，1：待移动，2：部分移动，3：按计划移动，2 和 3 不允许切换

### 库存盘点

用来记录当期库存盈亏

### 库存变动记录

 -2：取消出库，-1: 取消入库，1:入库, 2 出库, 3: 移库, 4: 手动调整, 5:过期丢弃, 6: 其他

用来记录所有库存变动记录，跟当前库存一样 不直接修改，任何单据导致的库存变化都通过信号传递过来


### 测试

大部分是自动化生成的 粗犷的测试，更细腻的测试需要手动编写

model test: `python manage.py test WMS`

api test: `python manage.py test api`

测试特定接口 `python manage.py test api.tests.WmsInventoryCheckTestCase `

### 侵入权限

由于前端一些特殊页面/控件有特殊需求，所以在一定情况下还是要侵入默认权限来决定前端菜单/控件显示权限

| 名称    |  内容类型                    |  代码名称| 说明 ｜ 
| ------ | ------ | ------ |
| Custom | Can check 入库单	WMS          | 入库单	check_wmsreceiptorder| 入库单审核权限 ｜


### Celery 定时任务

celery -A OpenWMS beat --loglevel=debug

celery -A OpenWMS worker --loglevel=debug

### 参考资料

http://wms.ichengle.top/

https://github.com/zccbbg/wms-ruoyi


## Usage

### 安装步骤

* 建议创建虚拟环境，不介意的话可以直接安装
* `pip install -r requirements.txt`
* `python manage.py createsuperuser`
* `python manage.py runserver`

### url

* 后台：`http://localhost:8000`
* api：`http://localhost:8000/api/v1/swagger`
* doc: `http://localhost:8000/api/v1/docs`


Licensing

![GPL v3](https://www.gnu.org/graphics/gplv3-with-text-136x68.png)

The source code is licensed under GPL v3. License is available here.