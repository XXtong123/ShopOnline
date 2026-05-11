# 简易网上购物系统 - 测试代码
class User:
    """用户类"""
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.cart = []

    def add_to_cart(self, product):
        """添加商品到购物车"""
        self.cart.append(product)
        print(f"商品 {product.name} 已加入购物车")

    def show_cart(self):
        """查看购物车"""
        if not self.cart:
            print("购物车为空")
            return
        print("\n===== 购物车 =====")
        total = 0
        for idx, p in enumerate(self.cart, 1):
            print(f"{idx}. {p.name}  价格：{p.price} 元")
            total += p.price
        print(f"总计：{total} 元")
        print("==================\n")

class Product:
    """商品类"""
    def __init__(self, pid, name, price):
        self.pid = pid
        self.name = name
        self.price = price

class Order:
    """订单类"""
    def __init__(self, user, products):
        self.user = user
        self.products = products
        self.total = sum(p.price for p in products)

    def show_order(self):
        print("\n===== 订单详情 =====")
        for p in self.products:
            print(f"- {p.name}  {p.price} 元")
        print(f"订单总价：{self.total} 元")
        print("订单创建成功！")
        print("====================\n")

class ShopSystem:
    """商城系统主类"""
    def __init__(self):
        self.users = []
        self.products = []
        self.current_user = None

    def init_products(self):
        """初始化商品"""
        self.products.append(Product(1, "笔记本电脑", 4500))
        self.products.append(Product(2, "无线耳机", 399))
        self.products.append(Product(3, "机械键盘", 299))
        self.products.append(Product(4, "智能手机", 3299))
        self.products.append(Product(5, "平板电脑", 2199))

    def show_all_products(self):
        """展示所有商品"""
        print("\n===== 商品列表 =====")
        for p in self.products:
            print(f"{p.pid}. {p.name}  价格：{p.price} 元")
        print("==================\n")

    def register(self, username, password):
        """用户注册"""
        for user in self.users:
            if user.username == username:
                print("用户名已存在")
                return False
        new_user = User(username, password)
        self.users.append(new_user)
        print("注册成功！")
        return True

    def login(self, username, password):
        """用户登录"""
        for user in self.users:
            if user.username == username and user.password == password:
                self.current_user = user
                print("登录成功！")
                return True
        print("用户名或密码错误")
        return False

    def create_order(self):
        """创建订单"""
        if not self.current_user:
            print("请先登录")
            return
        if not self.current_user.cart:
            print("购物车为空，无法创建订单")
            return
        order = Order(self.current_user, self.current_user.cart)
        order.show_order()
        self.current_user.cart.clear()
        return order

# 测试运行
if __name__ == "__main__":
    # 初始化商城
    system = ShopSystem()
    system.init_products()

    # 测试功能
    print("=== 欢迎来到网上购物系统 ===")
    system.register("testuser", "123456")
    system.login("testuser", "123456")

    # 展示商品
    system.show_all_products()

    # 添加商品到购物车
    system.current_user.add_to_cart(system.products[0])
    system.current_user.add_to_cart(system.products[2])

    # 查看购物车
    system.current_user.show_cart()

    # 创建订单
    system.create_order()

    print("=== 系统测试完成 ===")
