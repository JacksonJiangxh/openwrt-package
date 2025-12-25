# OpenWrt 软件包自动同步工具

这是一个用于自动同步多个OpenWrt仓库软件包的工具，通过GitHub Actions实现定时同步、自动去重和自动化工作流。

## 功能特性

- 📦 支持从多个源仓库同步OpenWrt软件包
- 🔄 自动去重，保留每个软件包的最新版本
- ⏰ 支持GitHub Actions定时同步（每天凌晨2点）
- 🎯 基于版本号比较的智能同步机制
- 📋 详细的同步日志和源信息跟踪
- 🚀 高效的浅克隆优化，减少存储空间占用
- 🎛️ 支持手动触发同步

## 支持的源仓库

当前配置的源仓库：

- **small-package**：https://github.com/kenzok8/small-package.git
- **helloworld**：https://github.com/fw876/helloworld.git
- **modem_feeds**：https://github.com/FUjr/modem_feeds.git

## 目录结构

```
openwrt-packages-sync/
├── .github/
│   └── workflows/
│       └── sync-packages.yml  # GitHub Actions工作流配置
├── temp_repos/                # 临时存储克隆的源仓库（自动创建和清理）
├── .gitignore                 # Git忽略文件
└── README.md                  # 项目说明文档
```

**注意**：
- 同步后的软件包直接存储在仓库根目录
- 同步脚本由GitHub Actions动态生成，不持久化存储
- 临时目录会在工作流结束时自动清理

## GitHub Actions 自动同步

### 触发条件

- **定时执行**：每天凌晨2点（UTC时间）自动运行
- **手动触发**：可通过GitHub UI手动触发
- **代码推送**：当代码推送到`main`分支时自动触发

### 工作流执行流程

1. **代码检出**：从GitHub仓库检出最新代码
2. **环境准备**：设置Python环境并安装依赖
3. **Git配置**：配置Git用户名和邮箱用于后续提交
4. **同步执行**：
   - 动态生成同步脚本
   - 克隆或更新源仓库
   - 扫描源仓库中的软件包
   - 解析软件包Makefile获取版本信息
   - 去重处理，保留每个软件包的最新版本
   - 比较版本，只同步需要更新的软件包
   - 为每个同步的软件包添加源信息文件
5. **变更检查**：检查是否有文件变更
6. **提交推送**：如有变更，提交并推送到仓库
7. **清理工作**：删除临时目录

## 核心同步机制

### 版本比较逻辑

同步工具使用智能版本比较算法：

1. **解析Makefile**：提取`PKG_NAME`、`PKG_VERSION`和`PKG_RELEASE`
2. **版本字符串规范化**：处理不同格式的版本号
3. **主版本比较**：比较`PKG_VERSION`
4. **发布版本比较**：如主版本相同，比较`PKG_RELEASE`
5. **决策逻辑**：只保留和同步最新版本

### 去重机制

1. **基于PKG_NAME去重**：使用软件包的`PKG_NAME`而非目录名作为唯一标识
2. **版本优先级**：同一软件包保留最高版本
3. **增量同步**：只同步需要更新的软件包

### 源信息跟踪

每个同步的软件包目录中会创建`.sync_source`文件，记录：
- 源仓库名称
- 软件包名称
- 版本信息
- 发布版本

## 手动运行（本地开发）

### 1. 克隆仓库

```bash
git clone https://github.com/your-username/openwrt-packages-sync.git
cd openwrt-packages-sync
```

### 2. 安装依赖

```bash
pip install GitPython
```

### 3. 创建并运行同步脚本

手动创建同步脚本（基于GitHub Actions工作流中的脚本内容），然后运行：

```bash
python sync_packages.py --work-dir ./temp_repos --output-dir .
```

### 命令行参数

- `--work-dir`：临时工作目录，用于存储克隆的源仓库（默认：`./temp_repos`）
- `--output-dir`：输出目录，用于存储同步后的软件包（默认：`.`）

## 自定义配置

### 修改源仓库

编辑`.github/workflows/sync-packages.yml`文件，在`SOURCE_REPOS`配置中添加或修改源仓库信息：

```python
SOURCE_REPOS = {
    "repo-name": {
        "url": "https://github.com/user/repo.git",
        "branch": "main"  # 可选，默认为仓库默认分支
    },
    # 添加更多源仓库...
}
```

### 修改定时时间

编辑`.github/workflows/sync-packages.yml`文件中的`cron`表达式：

```yaml
schedule:
  - cron: '0 2 * * *'  # 每天凌晨2点（UTC时间）运行
```

### 调整同步规则

可以修改工作流中生成的同步脚本，调整以下逻辑：
- 软件包发现规则
- 版本比较算法
- 去重逻辑
- 输出目录结构

## 注意事项

1. **仓库权限**：确保GitHub Actions有写入仓库的权限
2. **源仓库可访问性**：确保配置的源仓库可以正常访问
3. **磁盘空间**：首次运行会克隆所有源仓库，建议确保有足够的磁盘空间
4. **版本号格式**：软件包的Makefile中需包含标准的`PKG_NAME`、`PKG_VERSION`和`PKG_RELEASE`定义
5. **同步频率**：根据源仓库的更新频率调整定时任务的执行频率

## 故障排除

### 常见问题

1. **同步失败**：
   - 检查源仓库URL是否正确
   - 确认源仓库可访问
   - 查看GitHub Actions日志获取详细错误信息

2. **软件包未更新**：
   - 检查源仓库中软件包的版本号是否确实高于当前版本
   - 确认软件包的Makefile格式正确
   - 查看同步日志中的版本比较结果

3. **GitHub Actions推送失败**：
   - 检查仓库的Actions权限设置
   - 确保`contents: write`权限已正确配置

### 查看日志

1. 进入GitHub仓库的Actions页面
2. 选择"Sync OpenWrt Packages"工作流
3. 点击具体的运行记录查看详细日志

## 贡献

欢迎提交Issue和Pull Request来改进这个工具！

## 许可证

[MIT License](LICENSE)
