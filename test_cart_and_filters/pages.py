"""Модуль с объектами страниц"""


class CookieNotificationElement:
    """Элемент с уведомлением о куки на сайте"""

    def __init__(self, ):
        """Метод инициализации объекта"""

        self.close_button = ("xpath", "//button[contains(@class, 'cookie-notify__button')]")


class HeaderElement:
    """Элемент шапки сайта"""

    def __init__(self, ):
        """Метод инициализации объекта"""

        self.cart_icon = ("xpath", "//a[@class='header-cart-block__minicart']")


class CartPage:
    """Страница корзины"""

    def __init__(self, ):
        """Метод инициализации объекта"""

        self.all_cart_items = ("xpath", "//div[@class='cart-item']")
        self.proceed_purchase_button = ("xpath", "//button[contains(@class, 'cart-action-confirm')]")

    def get_item_locator(self, chosen_item_ppc):
        """Метод получения локатора товара"""

        return "xpath", f"//div[@data-ppc='{chosen_item_ppc}']"

    def get_item_input_field_locator(self, chosen_item_ppc):
        """Метод получения локатора инпута товара"""

        return "xpath", f"(//div[@data-ppc='{chosen_item_ppc}'])//input[@class='cart-item__count']"

    def get_any_item_input_field_locator(self):
        """Метод получения локатора инпута любого товара"""

        return "xpath", "(//input[@class='cart-item__count']"

    def get_item_decrease_quantity_locator(self, chosen_item_ppc):
        """Метод получения локатора кнопки уменьшения количества товара"""

        return "xpath", f"//a[contains(@class, 'cart-item__increment--minus') and @data-ppc='{chosen_item_ppc}']"

    def get_item_increase_quantity_locator(self, chosen_item_ppc):
        """Метод получения локатора кнопки увеличения количества товара"""

        return "xpath", f"//a[contains(@class, 'cart-item__increment--plus') and @data-ppc='{chosen_item_ppc}']"

    def get_remove_item_locator(self, chosen_item_ppc):
        """Метод получения локатора кнопки удаления товара"""

        return "xpath", f"//a[@class='cart-item__delete' and @data-ppc='{chosen_item_ppc}']"


class CatalogLaptopsPage:
    """Страница каталога товаров 'Ноутбуки'"""

    def __init__(self):
        """Метод инициализации объекта"""

        self.accept_filters_button = ("xpath", "//button[@class='price-filter__submit']")

        self.price = self.Price()
        self.availability = self.Availability()
        self.manufacturer = self.Manufacturer()

        self.additional_filters = self.AdditionalFilters()

    class Price:
        """Блок фильтров 'Цена'"""

        def __init__(self):
            """Метод инициализации объекта"""

            self.expand_button = ("xpath", "(//details[@class='price-filter__item'])[1]")
            self.price_min = ("xpath", "//input[@id='price_min']")
            self.price_max = ("xpath", "//input[@id='price_max']")

    class Availability:
        """Блок фильтров 'Наличие'"""

        def __init__(self):
            """Метод инициализации объекта"""

            self.expand_button = ("xpath", "(//details[@class='price-filter__item'])[2]")

            self.all_stock_status = ("xpath", "//input[@id='all_stock']")
            self.all_stock_action = ("xpath", "//label[@for='all_stock']")

            self.in_stock_status = ("xpath", "//input[@id='in_stock']")
            self.in_stock_action = ("xpath", "//label[@for='in_stock']")

            self.out_stock_status = ("xpath", "//input[@id='out_stock']")
            self.out_stock_action = ("xpath", "//label[@for='out_stock']")

    class Manufacturer:
        """Блок фильтров 'Производитель'"""

        def __init__(self):
            """Метод инициализации объекта"""

            self.expand_button = ("xpath", "//details[@id='sidebar-001491']")

            self.acer_status = ("xpath", "//input[@id='prop-M5']")
            self.acer_action = ("xpath", "//label[@for='prop-M5']")

            self.apple_status = ("xpath", "//input[@id='prop-M15']")
            self.apple_action = ("xpath", "//label[@for='prop-M15']")

            self.asus_status = ("xpath", "//input[@id='prop-M1']")
            self.asus_action = ("xpath", "//label[@for='prop-M1']")

            self.colorful_status = ("xpath", "//input[@id='prop-M564']")
            self.colorful_action = ("xpath", "//label[@for='prop-M564']")

            self.hp_status = ("xpath", "//input[@id='prop-M4']")
            self.hp_action = ("xpath", "//label[@for='prop-M4']")

            self.huawei_status = ("xpath", "//input[@id='prop-M372']")
            self.huawei_action = ("xpath", "//label[@for='prop-M372']")

            self.lenovo_status = ("xpath", "//input[@id='prop-M17']")
            self.lenovo_action = ("xpath", "//label[@for='prop-M17']")

            self.lg_status = ("xpath", "//input[@id='prop-M18']")
            self.lg_action = ("xpath", "//label[@for='prop-M18']")

            self.machenike_status = ("xpath", "//input[@id='prop-M1578']")
            self.machenike_action = ("xpath", "//label[@for='prop-M1578']")

            self.maibenben_status = ("xpath", "//input[@id='prop-M1591']")
            self.maibenben_action = ("xpath", "//label[@for='prop-M1591']")

            self.mechrevo_status = ("xpath", "//input[@id='prop-M1653']")
            self.mechrevo_action = ("xpath", "//label[@for='prop-M1653']")

            self.razer_status = ("xpath", "//input[@id='prop-M270']")
            self.razer_action = ("xpath", "//label[@for='prop-M270']")

            self.thunderobot_status = ("xpath", "//input[@id='prop-M1593']")
            self.thunderobot_action = ("xpath", "//label[@for='prop-M1593']")

            self.xiaomi_status = ("xpath", "//input[@id='prop-M1006']")
            self.xiaomi_action = ("xpath", "//label[@for='prop-M1006']")

    class AdditionalFilters:
        """Блок дополнительных фильтров"""

        def __init__(self):
            """Метод инициализации объекта"""

            self.expand_button = ("xpath", "//a[@class='price-filter__showmore']")

            self.graphics_card_type = self.GraphicsCardType()

        class GraphicsCardType:
            """Блок фильтров 'Тип видеокарты'"""

            def __init__(self):
                """Метод инициализации объекта"""

                self.expand_button = ("xpath", "//details[@id='sidebar-001322']")

                self.dedicated_status = ("xpath", "//input[@id='prop-213287']")
                self.dedicated_action = ("xpath", "//label[@for='prop-213287']")

                self.integrated_status = ("xpath", "//input[@id='prop-213286']")
                self.integrated_action = ("xpath", "//label[@for='prop-213286']")
