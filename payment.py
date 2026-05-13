import uuid
from datetime import datetime
from typing import Dict, Optional

class Payment:
    """模拟支付处理类"""
    
    def __init__(self, user_balance: float = 0.0):
        """
        初始化用户账户
        :param user_balance: 用户当前余额（元）
        """
        self.user_balance = user_balance
        self.transaction_records: Dict[str, Dict] = {}
    
    def check_balance(self, amount: float) -> bool:
        """检查余额是否足够支付订单"""
        if amount <= 0:
            raise ValueError("支付金额必须大于0")
        return self.user_balance >= amount
    
    def process_payment(self, order_id: str, amount: float) -> Dict:
        """
        处理支付
        :param order_id: 订单ID
        :param amount: 支付金额（元）
        :return: 支付结果字典
        """
        try:
            # 验证金额
            if amount <= 0:
                return {
                    "success": False,
                    "message": "支付金额无效，必须大于0",
                    "order_id": order_id
                }
            
            # 检查余额
            if not self.check_balance(amount):
                return {
                    "success": False,
                    "message": "余额不足，请充值后再试",
                    "order_id": order_id,
                    "current_balance": self.user_balance,
                    "required_amount": amount
                }
            
            # 扣除金额
            self.user_balance -= amount
            
            # 生成交易记录
            transaction_id = str(uuid.uuid4())[:8]
            transaction_info = {
                "transaction_id": transaction_id,
                "order_id": order_id,
                "amount": amount,
                "payment_method": "balance",
                "status": "success",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "remaining_balance": self.user_balance
            }
            
            self.transaction_records[transaction_id] = transaction_info
            
            return {
                "success": True,
                "message": "支付成功",
                "transaction_info": transaction_info
            }
            
        except ValueError as e:
            return {
                "success": False,
                "message": str(e),
                "order_id": order_id
            }
    
    def refund(self, order_id: str, amount: float) -> Dict:
        """
        退款处理（模拟）
        :param order_id: 订单ID
        :param amount: 退款金额
        :return: 退款结果
        """
        if amount <= 0:
            return {
                "success": False,
                "message": "退款金额无效"
            }
        
        self.user_balance += amount
        
        return {
            "success": True,
            "message": f"退款成功，已退还 {amount} 元",
            "current_balance": self.user_balance
        }
    
    def get_balance(self) -> float:
        """查询当前余额"""
        return self.user_balance
    
    def get_transaction_history(self) -> list:
        """获取所有交易记录"""
        return list(self.transaction_records.values())


class Order:
    """订单类（简化示例）"""
    
    def __init__(self, order_id: str, total_amount: float):
        self.order_id = order_id
        self.total_amount = total_amount
        self.status = "pending"  # pending, paid, cancelled
    
    def to_dict(self) -> Dict:
        return {
            "order_id": self.order_id,
            "total_amount": self.total_amount,
            "status": self.status
        }


# ---------------- 使用示例 ----------------
if __name__ == "__main__":
    # 1. 创建支付实例（假设用户余额为 500 元）
    payment = Payment(user_balance=500.0)
    
    # 2. 创建订单（模拟订单ID和金额）
    order1 = Order(order_id="ORD_001", total_amount=129.9)
    order2 = Order(order_id="ORD_002", total_amount=599.0)
    
    print(f"初始余额: {payment.get_balance()} 元\n")
    
    # 3. 支付订单1（余额充足）
    print(f"--- 支付订单 {order1.order_id}，金额 {order1.total_amount} 元 ---")
    result1 = payment.process_payment(order1.order_id, order1.total_amount)
    if result1["success"]:
        print("支付成功:", result1["transaction_info"])
        order1.status = "paid"
    else:
        print("支付失败:", result1["message"])
    print(f"当前余额: {payment.get_balance()} 元\n")
    
    # 4. 支付订单2（余额可能不足）
    print(f"--- 支付订单 {order2.order_id}，金额 {order2.total_amount} 元 ---")
    result2 = payment.process_payment(order2.order_id, order2.total_amount)
    if result2["success"]:
        print("支付成功:", result2["transaction_info"])
        order2.status = "paid"
    else:
        print("支付失败:", result2["message"])
        print(f"当前余额: {result2.get('current_balance')} 元，所需金额: {result2.get('required_amount')} 元")
    print()
    
    # 5. 查询交易记录
    print("--- 交易记录 ---")
    for trans in payment.get_transaction_history():
        print(f"  交易ID: {trans['transaction_id']}, 金额: {trans['amount']} 元, 状态: {trans['status']}, 时间: {trans['timestamp']}")
    print()
    
    # 6. 退款演示
    print("--- 退款订单 ORD_001 ---")
    refund_result = payment.refund(order1.order_id, order1.total_amount)
    print(refund_result["message"])
    print(f"退款后余额: {payment.get_balance()} 元")
