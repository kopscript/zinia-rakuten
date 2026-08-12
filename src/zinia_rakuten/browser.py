"""紫鸟浏览器驱动封装"""

from __future__ import annotations

import logging
import subprocess
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Generator, Optional

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

logger = logging.getLogger(__name__)


class ZiniaBrowserError(Exception):
    pass


class ZiniaBrowser:
    """紫鸟浏览器 WebDriver 封装"""

    def __init__(
        self,
        client_path: str,
        webdriver_path: str | None = None,
        version: str = "v6",
        headless: bool = False,
        proxy: str | None = None,
        user_info: dict | None = None,
    ) -> None:
        self.client_path = Path(client_path)
        self.webdriver_path = Path(webdriver_path) if webdriver_path else None
        self.version = version
        self.headless = headless
        self.proxy = proxy
        self.user_info = user_info  # { company, username, password }
        self._driver: WebDriver | None = None

        if not self.client_path.exists():
            raise ZiniaBrowserError(f"紫鸟客户端路径不存在: {self.client_path}")

    def _build_options(self) -> ChromeOptions:
        opts = ChromeOptions()
        opts.binary_location = str(self.client_path)

        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument("--disable-gpu")
        opts.add_argument("--disable-extensions")
        opts.add_argument("--disable-infobars")
        opts.add_argument("--window-size=1920,1080")
        opts.add_argument("--lang=ja-JP")
        opts.add_argument("--disable-blink-features=AutomationControlled")
        opts.add_experimental_option("excludeSwitches", ["enable-automation"])
        opts.add_experimental_option("useAutomationExtension", False)

        if self.headless:
            opts.add_argument("--headless=new")

        if self.proxy:
            opts.add_argument(f"--proxy-server={self.proxy}")

        return opts

    @property
    def driver(self) -> WebDriver:
        if self._driver is None:
            raise ZiniaBrowserError("浏览器未启动，请先调用 start()")
        return self._driver

    def start(self) -> WebDriver:
        """启动紫鸟浏览器"""
        logger.info("正在启动紫鸟浏览器 v%s ...", self.version)
        options = self._build_options()

        if self.webdriver_path and self.webdriver_path.exists():
            service = webdriver.chrome.service.Service(str(self.webdriver_path))
            self._driver = webdriver.Chrome(service=service, options=options)
        else:
            self._driver = webdriver.Chrome(options=options)

        self._driver.implicitly_wait(10)
        logger.info("紫鸟浏览器已启动")
        return self._driver

    def stop(self) -> None:
        if self._driver:
            self._driver.quit()
            self._driver = None
            logger.info("紫鸟浏览器已关闭")

    def __enter__(self) -> "ZiniaBrowser":
        self.start()
        return self

    def __exit__(self, *args) -> None:
        self.stop()

    # ---- 便捷操作 ----

    def open(self, url: str) -> None:
        logger.info("打开页面: %s", url)
        self.driver.get(url)

    def find(self, selector: str, by: By = By.CSS_SELECTOR, timeout: int = 15) -> WebElement:
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by, selector))
        )

    def find_clickable(self, selector: str, by: By = By.CSS_SELECTOR, timeout: int = 15) -> WebElement:
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((by, selector))
        )

    def click(self, selector: str, by: By = By.CSS_SELECTOR) -> None:
        el = self.find_clickable(selector, by)
        el.click()

    def type_text(self, selector: str, text: str, clear: bool = True, by: By = By.CSS_SELECTOR) -> None:
        el = self.find(selector, by)
        if clear:
            el.clear()
        el.send_keys(text)

    def wait(self, seconds: float) -> None:
        time.sleep(seconds)

    def screenshot(self, path: str) -> None:
        self.driver.save_screenshot(path)
        logger.info("截图已保存: %s", path)


@contextmanager
def zinia_session(
    client_path: str,
    webdriver_path: str | None = None,
    headless: bool = False,
    proxy: str | None = None,
) -> Generator[ZiniaBrowser, None, None]:
    browser = ZiniaBrowser(
        client_path=client_path,
        webdriver_path=webdriver_path,
        headless=headless,
        proxy=proxy,
    )
    try:
        browser.start()
        yield browser
    finally:
        browser.stop()
