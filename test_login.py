import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 页面URL常量（便于维护）
LOGIN_PAGE_URL = "https://www.saucedemo.com/"
INVENTORY_PAGE_URL = "https://www.saucedemo.com/inventory.html"

# 页面元素定位器
USERNAME_INPUT = (By.ID, "user-name")  # 用户名输入框
PASSWORD_INPUT = (By.ID, "password")  # 密码输入框
LOGIN_BUTTON = (By.ID, "login-button")  # 登录按钮
ERROR_MESSAGE_CONTAINER = (By.CSS_SELECTOR, "h3[data-test='error']")  # 错误消息容器
MENU_BUTTON = (By.ID, "react-burger-menu-btn")  # 登录后菜单按钮
SHOPPING_CART_LINK = (By.CLASS_NAME, "shopping_cart_link")  # 登录后购物车链接


def perform_login(driver, username, password):
    """执行登录操作：输入用户名、密码并点击登录按钮"""
    driver.find_element(*USERNAME_INPUT).send_keys(username)
    driver.find_element(*PASSWORD_INPUT).send_keys(password)
    driver.find_element(*LOGIN_BUTTON).click()


@pytest.mark.parametrize(
    "username",
    [
        ("standard_user"),  # TC-01: 标准用户登录
        ("problem_user"),  # TC-04: 问题用户登录
    ]
)
def test_successful_login(driver, username):
    """测试成功登录：验证跳转至商品列表页，且菜单、购物车元素可见"""
    perform_login(driver, username, "secret_sauce")

    # 等待页面跳转（5秒超时）
    WebDriverWait(driver, 5).until(EC.url_to_be(INVENTORY_PAGE_URL))

    # 验证登录成功
    assert driver.find_element(*MENU_BUTTON).is_displayed()
    assert driver.find_element(*SHOPPING_CART_LINK).is_displayed()


def test_tc06_performance_glitch_user_login(driver):
    """测试性能问题用户登录（需更长等待时间）：验证跳转及元素显示"""
    perform_login(driver, "performance_glitch_user", "secret_sauce")

    # 10秒超时应对性能延迟
    WebDriverWait(driver, 10).until(EC.url_to_be(INVENTORY_PAGE_URL))

    assert driver.find_element(*MENU_BUTTON).is_displayed()
    assert driver.find_element(*SHOPPING_CART_LINK).is_displayed()


@pytest.mark.parametrize(
    "username, password, expected_error_message",
    [
        ("123456", "secret_sauce", "Epic sadface: Username and password do not match any user in this service"),
        # TC-02: 用户名错误
        ("standard_user", "123456", "Epic sadface: Username and password do not match any user in this service"),
        # TC-03: 密码错误
        ("locked_out_user", "secret_sauce", "Epic sadface: Sorry, this user has been locked out."),  # TC-05: 锁定用户
        ("", "secret_sauce", "Epic sadface: Username is required"),  # TC-07: 用户名空
        ("standard_user", "", "Epic sadface: Password is required"),  # TC-07: 密码空
        ("", "", "Epic sadface: Username is required"),  # TC-07: 两者均空
    ]
)
def test_failed_login_scenarios(driver, username, password, expected_error_message):
    """测试登录失败场景：验证错误消息及页面未跳转"""
    perform_login(driver, username, password)

    # 等待错误消息显示
    error_element = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located(ERROR_MESSAGE_CONTAINER)
    )

    assert error_element.text == expected_error_message
    assert driver.current_url == LOGIN_PAGE_URL