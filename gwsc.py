# -*- coding: utf-8 -*-
"""
简易购物商城系统
功能：浏览商品、加入购物车、删除商品、查看购物车、结算、保存记录
"""
import os
import time

# 商品库（id, 名称, 价格）
goods = [
    {"id": 1, "name": "苹果手机", "price": 5999},
    {"id": 2, "name": "无线耳机", "price": 799},
    {"id": 3, "name": "机械键盘", "price": 329},
    {"id": 4, "name": "电竞鼠标", "price": 199},
    {"id": 5, "name": "27寸显示器", "price": 1299},
    {"id": 6, "name": "充电宝 20000mAh", "price": 129},
    {"id": 7, "name": "保温杯", "price": 89},
    {"id": 8, "name": "遮阳伞", "price": 49},
]

# 购物车
cart = []

# ---------------------- 功能函数 ----------------------

def show_goods():
    """展示所有商品"""
    print("\n============== 商品列表 ==============")
    print(f"{'ID':<6}{'商品名称':<20}{'价格（元）':<10}")
    print("-" * 42)
    for g in goods:
        print(f"{g['id']:<6}{g['name']:<20}{g['price']:<10}")
    print("-" * 42)

def add_to_cart():
    """加入购物车"""
    show_goods()
    try:
        gid = int(input("\n请输入要购买的商品ID："))
    except ValueError:
        print("❌ 输入不合法！")
        return

    # 查找商品
    find = None
    for g in goods:
        if g["id"] == gid:
            find = g
            break
    if not find:
        print("❌ 商品不存在！")
        return

    # 检查是否已在购物车
    for item in cart:
        if item["id"] == gid:
            item["count"] += 1
            print(f"✅ 已增加数量：{find['name']}，当前数量：{item['count']}")
            return

    # 新加入
    cart.append({
        "id": find["id"],
        "name": find["name"],
        "price": find["price"],
        "count": 1
    })
    print(f"✅ 成功加入购物车：{find['name']}")

def show_cart():
    """查看购物车"""
    if not cart:
        print("\n🛒 购物车空空如也～")
        return

    print("\n============== 购物车 ==============")
    print(f"{'ID':<6}{'商品名称':<20}{'单价':<10}{'数量':<8}{'小计':<10}")
    print("-" * 55)
    total = 0
    for item in cart:
        subtotal = item["price"] * item["count"]
        total += subtotal
        print(f"{item['id']:<6}{item['name']:<20}{item['price']:<10}{item['count']:<8}{subtotal:<10}")
    print("-" * 55)
    print(f"💰 总计：{total} 元")

def delete_from_cart():
    """删除购物车商品"""
    if not cart:
        print("\n🛒 购物车是空的！")
        return

    show_cart()
    try:
        gid = int(input("\n请输入要删除的商品ID："))
    except ValueError:
        print("❌ 输入不合法！")
        return

    for item in cart:
        if item["id"] == gid:
            cart.remove(item)
            print(f"✅ 已删除：{item['name']}")
            return
    print("❌ 该商品不在购物车中")

def clear_cart():
    """清空购物车"""
    cart.clear()
    print("\n🗑️ 购物车已清空！")

def checkout():
    """结算"""
    if not cart:
        print("\n🛒 购物车是空的，无法结算！")
        return

    show_cart()
    confirm = input("\n确认结算？(y/n)：")
    if confirm.lower() == "y":
        print("\n✅ 订单提交成功！")
        print("⏳ 正在支付...")
        time.sleep(1)
        print("✅ 支付成功！感谢您的购买～")
        cart.clear()
    else:
        print("🚫 已取消结算")

def save_cart():
    """保存购物车到文件"""
    try:
        with open("cart.txt", "w", encoding="utf-8") as f:
            for item in cart:
                f.write(f"{item['id']},{item['name']},{item['price']},{item['count']}\n")
        print("\n💾 购物车已保存！")
    except:
        print("❌ 保存失败")

def load_cart():
    """从文件加载购物车"""
    if not os.path.exists("cart.txt"):
        print("\n❌ 无保存记录")
        return
    try:
        cart.clear()
        with open("cart.txt", "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                d = line.split(",")
                cart.append({
                    "id": int(d[0]),
                    "name": d[1],
                    "price": float(d[2]),
                    "count": int(d[3])
                })
        print(f"\n✅ 加载成功！当前购物车共 {len(cart)} 种商品")
    except:
        print("❌ 加载失败")

def show_menu():
    """显示菜单"""
    print("\n" + "="*40)
    print("      🛍️  欢迎来到简易购物商城")
    print("="*40)
    print("1. 浏览商品")
    print("2. 加入购物车")
    print("3. 查看购物车")
    print("4. 删除购物车商品")
    print("5. 清空购物车")
    print("6. 结算订单")
    print("7. 保存购物车")
    print("8. 加载购物车")
    print("0. 退出商城")
    print("="*40)

# ---------------------- 主程序 ----------------------
def main():
    while True:
        show_menu()
        choice = input("请输入功能编号：").strip()

        if choice == "1":
            show_goods()
        elif choice == "2":
            add_to_cart()
        elif choice == "3":
            show_cart()
        elif choice == "4":
            delete_from_cart()
        elif choice == "5":
            clear_cart()
        elif choice == "6":
            checkout()
        elif choice == "7":
            save_cart()
        elif choice == "8":
            load_cart()
        elif choice == "0":
            print("\n👋 欢迎下次光临，再见！")
            break
        else:
            print("\n❌ 输入无效，请重新选择！")
        input("\n按回车键继续...")

if __name__ == "__main__":
    main()
