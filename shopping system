# 商城购物系统
import time

# 初始化商品数据（商品ID: {名称, 价格, 库存}）
goods = {
    1: {"name": "华为Mate70", "price": 5999, "stock": 20},
    2: {"name": "苹果iPhone16", "price": 7999, "stock": 15},
    3: {"name": "小米15", "price": 4299, "stock": 30},
    4: {"name": "无线蓝牙耳机", "price": 399, "stock": 50},
    5: {"name": "20000mAh充电宝", "price": 129, "stock": 40}
}

# 初始化购物车（存储商品ID和购买数量）
shopping_cart = {}

# 打印欢迎界面
def print_welcome():
    print("=" * 50)
    print("      欢迎来到Python控制台购物商城")
    print("=" * 50)
    time.sleep(0.5)

# 展示所有商品
def show_goods():
    print("\n【商品列表】")
    print("-" * 50)
    print(f"{'商品ID':<8}{'商品名称':<15}{'单价(元)':<10}{'库存':<8}")
    print("-" * 50)
    for gid, info in goods.items():
        print(f"{gid:<8}{info['name']:<15}{info['price']:<10}{info['stock']:<8}")
    print("-" * 50)

# 添加商品到购物车
def add_to_cart():
    try:
        gid = int(input("请输入要购买的商品ID："))
        if gid not in goods:
            print("❌ 商品ID不存在！")
            return
        
        # 检查库存
        if goods[gid]["stock"] <= 0:
            print(f"❌ {goods[gid]['name']} 已售罄！")
            return
        
        num = int(input("请输入购买数量："))
        if num <= 0:
            print("❌ 购买数量必须大于0！")
            return
        if num > goods[gid]["stock"]:
            print(f"❌ 库存不足，当前库存：{goods[gid]['stock']}")
            return
        
        # 添加/更新购物车
        if gid in shopping_cart:
            shopping_cart[gid] += num
        else:
            shopping_cart[gid] = num
        print(f"✅ 成功添加 {num} 个 {goods[gid]['name']} 到购物车！")
    except ValueError:
        print("❌ 输入错误，请输入数字！")

# 查看购物车
def show_cart():
    if not shopping_cart:
        print("\n🛒 购物车为空！")
        return
    
    total_price = 0
    print("\n【购物车详情】")
    print("-" * 60)
    print(f"{'商品ID':<8}{'商品名称':<15}{'单价':<10}{'数量':<8}{'小计(元)':<10}")
    print("-" * 60)
    
    for gid, num in shopping_cart.items():
        name = goods[gid]["name"]
        price = goods[gid]["price"]
        subtotal = price * num
        total_price += subtotal
        print(f"{gid:<8}{name:<15}{price:<10}{num:<8}{subtotal:<10}")
    
    print("-" * 60)
    print(f"💰 购物车总金额：{total_price} 元")
    return total_price

# 删除购物车商品
def delete_from_cart():
    if not shopping_cart:
        print("\n🛒 购物车为空，无需删除！")
        return
    
    try:
        gid = int(input("请输入要删除的商品ID："))
        if gid not in shopping_cart:
            print("❌ 该商品不在购物车中！")
            return
        
        del shopping_cart[gid]
        print(f"✅ 成功删除商品！")
    except ValueError:
        print("❌ 输入错误，请输入数字！")

# 结算支付
def checkout():
    total = show_cart()
    if not total:
        return
    
    print(f"\n💳 需支付金额：{total} 元")
    confirm = input("确认支付？(y/n)：")
    if confirm.lower() == "y":
        # 扣减库存
        for gid, num in shopping_cart.items():
            goods[gid]["stock"] -= num
        
        # 清空购物车
        shopping_cart.clear()
        print("\n✅ 支付成功！感谢您的购买，祝您生活愉快！")
        time.sleep(1)
    else:
        print("\n❌ 已取消支付")

# 主菜单
def main_menu():
    print_welcome()
    while True:
        print("\n===== 主菜单 =====")
        print("1. 查看商品列表")
        print("2. 添加商品到购物车")
        print("3. 查看购物车")
        print("4. 删除购物车商品")
        print("5. 结算支付")
        print("0. 退出系统")
        print("================")
        
        try:
            choice = int(input("请输入操作序号："))
            if choice == 1:
                show_goods()
            elif choice == 2:
                show_goods()
                add_to_cart()
            elif choice == 3:
                show_cart()
            elif choice == 4:
                show_cart()
                delete_from_cart()
            elif choice == 5:
                checkout()
            elif choice == 0:
                print("\n👋 感谢使用购物商城，再见！")
                break
            else:
                print("❌ 请输入有效序号！")
        except ValueError:
            print("❌ 输入错误，请输入数字！")

# 启动系统
if __name__ == "__main__":
    main_menu()
