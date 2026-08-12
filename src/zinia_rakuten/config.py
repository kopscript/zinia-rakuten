"""配置管理"""

from __future__ import annotations

from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional

import yaml


@dataclass
class BrowserConfig:
    client_path: str = ""
    webdriver_path: Optional[str] = None
    version: str = "v6"
    headless: bool = False
    proxy: Optional[str] = None


@dataclass
class CredentialsConfig:
    shop_id: str = ""
    login_id: str = ""
    password: str = ""


@dataclass
class AppConfig:
    browser: BrowserConfig = field(default_factory=BrowserConfig)
    credentials: CredentialsConfig = field(default_factory=CredentialsConfig)


def load_config(path: Optional[Path] = None) -> AppConfig:
    """加载配置文件"""
    if path is None:
        path = Path("config.yaml")

    if not path.exists():
        raise FileNotFoundError(
            f"配置文件不存在: {path}\n"
            "请运行 `zinia-rakuten init` 生成配置模板"
        )

    with open(path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f) or {}

    return AppConfig(
        browser=BrowserConfig(**(raw.get("browser", {}) or {})),
        credentials=CredentialsConfig(**(raw.get("credentials", {}) or {})),
    )


def generate_config_template(path: Path) -> None:
    """生成配置文件模板"""
    template = {
        "browser": {
            "client_path": "D:\\\\ziniao\\\\ziniao.exe",
            "webdriver_path": "D:\\\\webdriver",
            "version": "v6",
            "headless": False,
            "proxy": None,
        },
        "credentials": {
            "shop_id": "你的店铺ID",
            "login_id": "你的登录ID",
            "password": "你的密码",
        },
    }

    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(template, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
