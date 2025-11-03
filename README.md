# swag_labs_automation

这是一个针对 [Swag Labs](https://www.saucedemo.com/) 登录页面编写的 Web 自动化测试项目。

项目基于 **Python** + **Selenium** + **Pytest** 框架，展示了如何构建一个基础、稳定且易于维护的自动化测试脚本。

<img src="D:\GitHubNote\swag_labs_automation\attachments\image-20251103141450352.png" alt="image-20251103141450352" style="zoom: 33%;" />

## 🧪 覆盖的测试场景

本项目主要覆盖了 Swag Labs 登录页的以下测试用例：

1.  **成功登录 (Successful Logins):**
    * `standard_user` (标准用户)
    * `problem_user` (问题用户)
    * `performance_glitch_user` (性能延迟用户，测试中使用了更长的等待时间)

2.  **失败场景 (Failed Logins):**
    * `locked_out_user` (被锁定的用户)
    * 用户名错误
    * 密码错误
    * 用户名为空
    * 密码为空
    * 用户名和密码均为空

### 

