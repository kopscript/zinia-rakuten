# 紫鸟浏览器 — 乐天店铺自动化

基于紫鸟浏览器 WebDriver SDK 的乐天 RMS 店铺自动化工具。本地运行。

## 安装

```bash
# 克隆仓库
git clone https://github.com/kopscript/zinia-rakuten.git
cd zinia-rakuten

# 创建虚拟环境
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 安装依赖
pip install -e .
```

## 配置

1. 生成配置文件模板：

```bash
zinia-rakuten init
```

2. 编辑 `config.yaml` 填入紫鸟客户端路径和乐天账号信息：

```yaml
browser:
  client_path: "D:\\ziniao\\ziniao.exe"  # 紫鸟客户端路径
  webdriver_path: "D:\\webdriver"       # chromedriver 路径（可选）
  version: "v6"                          # v5 或 v6
  headless: false                         # 无头模式
  proxy: null

credentials:
  shop_id: "你的店铺ID"
  login_id: "你的登录ID"
  password: "你的密码"
```

## 使用

```bash
# 查看帮助
zinia-rakuten --help

# 登录验证
zinia-rakuten login --shop-id YOUR_SHOP_ID

# 查看商品列表
zinia-rakuten products

# 搜索商品
zinia-rakuten products --search "关键词"

# 查看订单列表
zinia-rakuten orders

# 查看库存
zinia-rakuten inventory

# 查看评价
zinia-rakuten reviews

# 查看仪表盘
zinia-rakuten dashboard
```

## 功能

- [x] 登录乐天 RMS 后台
- [x] 商品列表 / 搜索
- [x] 订单列表
- [x] 库存列表
- [x] 评价列表
- [x] 店铺仪表盘
- [ ] 商品创建 / 编辑 / 删除
- [ ] 订单状态更新（发货/取消）
- [ ] 数据导出
- [ ] 自动定时任务

## 依赖

- Python 3.10+
- 紫鸟浏览器客户端（需安装）
- chromedriver（可选，自动下载）

## 注意事项

- 紫鸟客户端必须**本机安装**（Windows/Mac/Linux 桌面端）
- 需要开通紫鸟 **WebDriver 权限**（参考紫鸟官方文档）
- 选择器基于乐天 RMS 页面结构，页面改版可能需要调整

## License

MIT
