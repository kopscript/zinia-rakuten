"""CLI 入口"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.logging import RichHandler

from .browser import ZiniaBrowser
from .rakuten import RakutenAccount

app = typer.Typer(
    name="zinia-rakuten",
    help="紫鸟浏览器自动化操作乐天店铺",
    no_args_is_help=True,
)

console = Console()


def setup_logging(verbose: bool = False) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(message)s",
        handlers=[RichHandler(console=console, rich_tracebacks=True, show_time=False)],
    )


@app.command()
def login(
    shop_id: str = typer.Option(..., "--shop-id", "-s", help="店铺ID"),
    config: Optional[Path] = typer.Option(None, "--config", "-c", help="配置文件路径"),
) -> None:
    """登录并验证"""
    from .config import load_config
    cfg = load_config(config)
    account = RakutenAccount(ZiniaBrowser(**cfg.browser))
    account.login(shop_id, cfg.credentials.login_id, cfg.credentials.password)
    console.print("[green]✓ 登录验证完成[/green]" if account.logged_in else "[red]✗ 登录失败[/red]")


@app.command()
def products(
    config: Optional[Path] = typer.Option(None, "--config", "-c", help="配置文件路径"),
    search: Optional[str] = typer.Option(None, "--search", help="搜索关键词"),
    page: int = typer.Option(1, "--page", "-p", help="页码"),
) -> None:
    """查看商品列表"""
    from .config import load_config
    cfg = load_config(config)
    with ZiniaBrowser(**cfg.browser) as browser:
        account = RakutenAccount(browser)
        account.login(cfg.credentials.shop_id, cfg.credentials.login_id, cfg.credentials.password)
        if search:
            items = account.search_product(search)
        else:
            items = account.list_products(page)
        console.print_json(data=items)


@app.command()
def orders(
    config: Optional[Path] = typer.Option(None, "--config", "-c", help="配置文件路径"),
    status: Optional[str] = typer.Option(None, "--status", help="订单状态筛选"),
    page: int = typer.Option(1, "--page", "-p", help="页码"),
) -> None:
    """查看订单列表"""
    from .config import load_config
    cfg = load_config(config)
    with ZiniaBrowser(**cfg.browser) as browser:
        account = RakutenAccount(browser)
        account.login(cfg.credentials.shop_id, cfg.credentials.login_id, cfg.credentials.password)
        orders = account.list_orders(page=page, status=status or "")
        console.print_json(data=orders)


@app.command()
def inventory(
    config: Optional[Path] = typer.Option(None, "--config", "-c", help="配置文件路径"),
) -> None:
    """查看库存"""
    from .config import load_config
    cfg = load_config(config)
    with ZiniaBrowser(**cfg.browser) as browser:
        account = RakutenAccount(browser)
        account.login(cfg.credentials.shop_id, cfg.credentials.login_id, cfg.credentials.password)
        items = account.list_inventory()
        console.print_json(data=items)


@app.command()
def reviews(
    config: Optional[Path] = typer.Option(None, "--config", "-c", help="配置文件路径"),
    page: int = typer.Option(1, "--page", "-p", help="页码"),
) -> None:
    """查看评价"""
    from .config import load_config
    cfg = load_config(config)
    with ZiniaBrowser(**cfg.browser) as browser:
        account = RakutenAccount(browser)
        account.login(cfg.credentials.shop_id, cfg.credentials.login_id, cfg.credentials.password)
        reviews = account.list_reviews(page=page)
        console.print_json(data=reviews)


@app.command()
def dashboard(
    config: Optional[Path] = typer.Option(None, "--config", "-c", help="配置文件路径"),
) -> None:
    """查看店铺仪表盘"""
    from .config import load_config
    cfg = load_config(config)
    with ZiniaBrowser(**cfg.browser) as browser:
        account = RakutenAccount(browser)
        account.login(cfg.credentials.shop_id, cfg.credentials.login_id, cfg.credentials.password)
        data = account.get_shop_dashboard()
        console.print_json(data=data)


@app.command()
def init(
    path: Path = typer.Option("config.yaml", "--path", "-p", help="配置文件保存路径"),
) -> None:
    """生成配置文件模板"""
    from .config import generate_config_template
    generate_config_template(path)
    console.print(f"[green]✓ 配置文件已生成: {path}[/green]")
    console.print("[yellow]请编辑配置文件填入你的紫鸟路径和乐天账号信息[/yellow]")


@app.command()
def version() -> None:
    """显示版本"""
    from . import __version__
    console.print(f"zinia-rakuten v{__version__}")


def main() -> None:
    app()


if __name__ == "__main__":
    main()
