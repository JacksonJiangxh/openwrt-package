# OpenWrt 软件包自动同步工具

这是一个用于自动同步多个OpenWrt仓库软件包的工具，支持定时同步、自动去重和自动化工作流。

## 功能特性

- ��� 支持从多个源仓库同步OpenWrt软件包
- �� 自动去重，避免重复软件包
- ⏰ 支持GitHub Actions定时同步
- ��� 支持多种文件类型和目录结构
- ��� 可配置的同步规则
- ��� 详细的同步日志

## 支持的源仓库

- **small-package**：包含丰富的OpenWrt软件包
- **helloworld**：包含Shadowsocks、V2Ray等网络工具
- **modem_feeds**：包含4G/5G modem相关的驱动和应用

## 目录结构

```
openwrt-packages-sync/
├── .github/
│   └── workflows/
│       └── sync-packages.yml  # GitHub Actions工作流
├── packages/                  # 同步后的软件包存储目录
├── temp_repos/                # 临时存储克隆的源仓库（自动创建）
├── sync_packages.py           # 同步脚本
├── .gitignore                # Git忽略文件
└── README.md                 # 项目说明文档
```

## 安装和配置

### 1. 克隆仓库

```bash
git clone https://github.com/your-username/openwrt-packages-sync.git
cd openwrt-packages-sync
```

### 2. 安装依赖

```bash
pip install GitPython
```

### 3. 配置源仓库

修改`sync_packages.py`文件中的`SOURCE_REPOS`配置，添加或修改源仓库信息：

```python
SOURCE_REPOS = {
    "small-package": {
        "url": "https://github.com/xxx/small-package",
        "branch": "master"
    },
    # 添加更多源仓库...
}
```

### 4. 配置同步规则

修改`sync_packages.py`文件中的同步规则，调整需要同步的软件包类型。

## 使用方法

### 手动运行同步

```bash
python sync_packages.py
```

### 自定义参数

```bash
# 指定临时工作目录和输出目录
python sync_packages.py --work-dir ./my_temp --output-dir ./my_packages
```

### 参数说明

- `--work-dir`：临时工作目录，用于存储克隆的源仓库（默认：`./temp_repos`）
- `--output-dir`：输出目录，用于存储同步后的软件包（默认：`./packages`）

## GitHub Actions 自动同步

### 配置步骤

1. 将此仓库推送到GitHub
2. 在GitHub仓库中启用Actions
3. 工作流会自动按照配置的时间（每天凌晨2点）执行同步

### 手动触发同步

1. 进入GitHub仓库的Actions页面
2. 选择"Sync OpenWrt Packages"工作流
3. 点击"Run workflow"按钮

## 去重机制

同步工具使用以下机制确保软件包的唯一性：

1. **目录哈希**：计算每个软件包目录的内容哈希值
2. **哈希比对**：如果哈希值已存在，则跳过该软件包
3. **智能判断**：仅同步包含有效Makefile或符合OpenWrt软件包结构的目录

## 同步规则

### 有效软件包判断

一个目录被视为有效软件包的条件：

1. 包含`Makefile`文件
2. 或为`luci-app-*`目录且包含`luasrc`或`root`子目录
3. 或符合OpenWrt软件包的标准结构

### 特殊处理

- **modem_feeds**：特殊处理其`application`、`luci`、`driver`目录
- **luci应用**：自动识别并同步符合luci应用结构的目录

## 日志和监控

- 同步过程会输出详细的日志信息
- 同步结果会显示同步的软件包数量
- GitHub Actions会保存完整的运行日志

## 注意事项

1. 确保源仓库可访问
2. 首次运行会克隆所有源仓库，可能需要较长时间
3. 建议定期清理临时目录
4. 确保有足够的磁盘空间存储同步的软件包

## 故障排除

### 常见问题

1. **同步失败**：检查源仓库URL是否正确，网络连接是否正常
2. **去重不工作**：检查软件包目录结构是否符合标准
3. **GitHub Actions推送失败**：确保仓库有正确的推送权限

### 日志查看

```bash
# 查看GitHub Actions日志
# 进入仓库 -> Actions -> 选择对应的工作流运行 -> 查看日志
```

## 自定义配置

### 修改定时时间

编辑`.github/workflows/sync-packages.yml`文件中的`cron`表达式：

```yaml
schedule:
  - cron: '0 2 * * *'  # 每天凌晨2点运行
```

### 添加新的源仓库

1. 在`SOURCE_REPOS`中添加新仓库配置
2. 确保仓库包含符合OpenWrt标准的软件包结构

## 贡献

欢迎提交Issue和Pull Request来改进这个工具！

## 许可证

[MIT License](LICENSE)
