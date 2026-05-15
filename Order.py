"""
网上购物系统 - 订单管理模块
功能：创建订单、订单支付、取消订单、超时自动关闭、查询订单、状态管理
符合实验3：代码规范、功能完整、可上传Git进行配置管理
"""
import time
from enum import Enum
from typing import List, Dict, Optional


# 订单状态枚举
class OrderStatus(Enum):
    PENDING_PAY = "待支付"
    PAID = "已支付"
    CANCELED = "已取消"
    TIMEOUT_CLOSED = "超时关闭"
    SHIPPED = "已发货"
    COMPLETED = "已完成"


# 订单类
class Order:
    def __init__(
            self,
            order_id: str,
            user_id: str,
            product_list: List[Dict],
            total_price: float
    ):
        self.order_id = order_id
        self.user_id = user_id
        self.product_list = product_list
        self.total_price = total_price
        self.status = OrderStatus.PENDING_PAY
        self.create_time = time.time()
        self.pay_time: Optional[float] = None
        self.cancel_time: Optional[float] = None

    def to_dict(self):
        return {
            "order_id": self.order_id,
            "user_id": self.user_id,
            "product_list": self.product_list,
            "total_price": self.total_price,
            "status": self.status.value,
            "create_time": time.ctime(self.create_time),
            "pay_time": time.ctime(self.pay_time) if self.pay_time else None,
            "cancel_time": time.ctime(self.cancel_time) if self.cancel_time else None
        }


# 订单管理核心类
class OrderManager:
    def __init__(self):
        self.order_map: Dict[str, Order] = {}  # 订单存储
        self.TIME_OUT_SECONDS = 15 * 60  # 15分钟未支付自动关闭
        
    def create_order(
            self,
            order_id: str,
            user_id: str,
            product_list: List[Dict],
            total_price: float
    ) -> Order:
        if order_id in self.order_map:
            raise Exception("订单ID已存在")

        if total_price <= 0:
            raise Exception("订单金额必须大于0")

        if not product_list:
            raise Exception("订单商品不能为空")

        order = Order(order_id, user_id, product_list, total_price)
        self.order_map[order_id] = order
        print(f"订单创建成功：{order_id}")
        return order

    # 支付订单
    def pay_order(self, order_id: str) -> bool:
        if order_id not in self.order_map:
            raise Exception("订单不存在")

        order = self.order_map[order_id]

        if order.status != OrderStatus.PENDING_PAY:
            raise Exception(f"当前订单状态：{order.status.value}，无法支付")

        # 检查是否超时
        if time.time() - order.create_time > self.TIME_OUT_SECONDS:
            order.status = OrderStatus.TIMEOUT_CLOSED
            raise Exception("订单已超时，自动关闭，无法支付")

        order.status = OrderStatus.PAID
        order.pay_time = time.time()
        print(f"订单支付成功：{order_id}")
        return True

    # 用户主动取消订单
    def cancel_order(self, order_id: str) -> bool:
        if order_id not in self.order_map:
            raise Exception("订单不存在")

        order = self.order_map[order_id]

        if order.status != OrderStatus.PENDING_PAY:
            raise Exception(f"仅待支付订单可取消，当前状态：{order.status.value}")

        order.status = OrderStatus.CANCELED
        order.cancel_time = time.time()
        print(f"订单已取消：{order_id}")
        return True

    # 系统自动关闭超时订单
    def auto_close_timeout_orders(self):
        current = time.time()
        closed_count = 0

        for order_id, order in self.order_map.items():
            if order.status == OrderStatus.PENDING_PAY:
                if current - order.create_time > self.TIME_OUT_SECONDS:
                    order.status = OrderStatus.TIMEOUT_CLOSED
                    closed_count += 1

        print(f"自动关闭超时订单 {closed_count} 个")
        return closed_count

    # 根据订单ID查询订单
    def get_order_by_id(self, order_id: str) -> Optional[Dict]:
        if order_id not in self.order_map:
            return None
        return self.order_map[order_id].to_dict()

    # 查询用户所有订单
    def get_user_orders(self, user_id: str) -> List[Dict]:
        res = []
        for order in self.order_map.values():
            if order.user_id == user_id:
                res.append(order.to_dict())
        return res

    # 展示所有订单（管理员）
    def show_all_orders(self):
        if not self.order_map:
            print("暂无订单")
            return

        print("\n========== 所有订单 ==========")
        for o in self.order_map.values():
            info = o.to_dict()
            print(f"订单号：{info['order_id']}")
            print(f"用户ID：{info['user_id']}")
            print(f"总金额：{info['total_price']}")
            print(f"订单状态：{info['status']}")
            print(f"创建时间：{info['create_time']}")
            print("-" * 40)


# ===================== 测试入口 =====================
if __name__ == '__main__':
    # 初始化订单管理器
    order_service = OrderManager()

    # 模拟商品列表
    products = [
        {"product_id": "p001", "name": "高性能笔记本", "price": 5999, "count": 1},
        {"product_id": "p002", "name": "无线鼠标", "price": 129, "count": 1}
    ]

    # 1. 创建订单
    try:
        order_service.create_order(
            order_id="ORDER_20260511_001",
            user_id="user_001",
            product_list=products,
            total_price=5999 + 129
        )
    except Exception as e:
        print("创建订单失败：", e)

    # 2. 查询订单
    order_info = order_service.get_order_by_id("ORDER_20260511_001")
    print("\n查询到订单信息：")
    for k, v in order_info.items():
        print(f"{k}: {v}")

    # 3. 支付订单
    try:
        order_service.pay_order("ORDER_20260511_001")
    except Exception as e:
        print("支付失败：", e)

    # 4. 查看所有订单
    order_service.show_all_orders()

    # 5. 模拟自动关闭超时订单
    order_service.auto_close_timeout_orders()

    # 6. 查询某个用户的所有订单
    user_orders = order_service.get_user_orders("user_001")
    print(f"\n用户 user_001 共有 {len(user_orders)} 个订单")
