import pytest
from selenium.webdriver.chrome.service import Service
from selenium import webdriver


@pytest.fixture(scope="function")
def driver():
    """pytest fixture：为每个测试函数提供独立的Chrome驱动实例
    包含浏览器初始化、配置及测试后清理，确保测试隔离性
    """

    # 初始化Chrome驱动服务
    service = Service()
    # 配置Chrome选项
    options = webdriver.ChromeOptions()
    # 启动Chrome浏览器
    driver = webdriver.Chrome(service=service, options=options)

    # 最大化窗口（确保视图一致）
    driver.maximize_window()
    # 设置10秒隐式等待（处理元素加载延迟）
    driver.implicitly_wait(10)
    # 导航到测试起始页（Swag Labs登录页）
    driver.get("https://www.saucedemo.com/")

    # 传递驱动实例给测试函数
    yield driver

    # 测试结束后关闭浏览器，释放资源
    driver.quit()