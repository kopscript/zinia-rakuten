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
class AppConfig:
    browser: BrowserConfig = field(default_factory=BrowserConfig)


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

    browser_raw = raw.get("browser", {}) or {}
    return AppConfig(
        browser=BrowserConfig(**browser_raw),
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
            "user_info": {
                "company": "你的企业公司名",
                "username": "你的用户名",
                "password": "你的密码",
            },
        },
    }

    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(template, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
