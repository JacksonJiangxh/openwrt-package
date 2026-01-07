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
openwrt-packages/
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


## OpenWrt 插件/工具功能说明大全


## 一、 【LuCI 应用】（333个）
LuCI 应用是带 Web 管理界面的功能插件，可直接在 OpenWrt 后台配置。
| 插件名称 | 核心功能 |
| ---- | ---- |
| luci-app-3cat | 一款网络工具类插件，用于网络参数检测与调试 |
| luci-app-3ginfo-lite | 精简版 3G/4G 调制解调器信息监控，显示信号强度、运营商、连接状态等 |
| luci-app-3proxy | 3proxy 代理服务器的 Web 管理界面，支持 HTTP/SOCKS 等代理协议 |
| luci-app-LingTiGameAcc | 玲珑游戏加速器的 OpenWrt 客户端，优化游戏网络连接 |
| luci-app-UUGameAcc | UU 游戏加速器的 OpenWrt 客户端，降低游戏延迟 |
| luci-app-accesscontrol-plus | 增强版访问控制，可按设备、时间段限制网络访问 |
| luci-app-adguardhome | AdGuard Home 的 Web 管理界面，实现广告过滤、自定义 DNS、防篡改 |
| luci-app-advanced | 系统高级设置插件，拓展 OpenWrt 原生未提供的系统参数配置项 |
| luci-app-advancedplus | 比 `advanced` 功能更全的系统高级配置插件 |
| luci-app-aihelper | 集成 AI 功能的辅助工具（如网络诊断、配置建议等） |
| luci-app-airconnect | 无线网桥/中继配置工具，简化多设备无线组网 |
| luci-app-aliddns | 阿里云 DDNS 客户端，实现公网 IP 变化时自动更新域名解析 |
| luci-app-alist | Alist 文件列表工具的 Web 界面，支持挂载阿里云盘、百度网盘等多种存储 |
| luci-app-alpha-config | Alpha 路由器专属配置优化插件 |
| luci-app-alwaysonline | 网络保活插件，防止拨号/网络连接意外断开 |
| luci-app-ap-modem | 把路由器作为 AP 模式的调制解调器管理工具 |
| luci-app-apfree-wifidog | 开源热点认证系统，用于公共 WiFi 认证计费 |
| luci-app-arcadia | 网络流量分析与监控插件 |
| luci-app-argone-config | Argone 主题的配置插件，自定义主题外观与功能 |
| luci-app-at-socat | AT 指令与 socat 工具的集成管理，用于串口/网络数据转发 |
| luci-app-atcommands | 调制解调器 AT 指令发送与调试工具 |
| luci-app-atinout | AT 指令测试工具，用于调试 3G/4G 模块 |
| luci-app-autoipsetadder | 自动将指定 IP/域名添加到 ipset 规则集，配合防火墙实现批量管控 |
| luci-app-autorepeater | 自动中继插件，优化无线中继的稳定性与切换速度 |
| luci-app-autoshell | 自动执行 Shell 脚本的插件，支持定时/触发式执行 |
| luci-app-autoupdate | 固件自动更新插件，支持检测指定源并自动下载刷机 |
| luci-app-bandix | 网络带宽控制与优化工具 |
| luci-app-bandwidthd | 带宽流量统计插件，按设备统计实时/历史流量使用情况 |
| luci-app-banmac-ipt | 基于 iptables 的 MAC 地址封禁工具，禁止指定设备联网 |
| luci-app-banmac-nft | 基于 nftables 的 MAC 地址封禁工具（新一代防火墙框架） |
| luci-app-beardropper | 设备接入检测与管控工具，可自动踢除未授权设备 |
| luci-app-bitsrunlogin-go | 校园网锐捷认证的 Go 语言客户端（适配多校园网环境） |
| luci-app-bridge | 网络桥接配置工具，简化多网口桥接设置 |
| luci-app-broadbandacc | 宽带加速插件，优化网络传输协议提升速度 |
| luci-app-bypass | 智能分流代理插件，支持按域名/IP 规则分流网络流量 |
| luci-app-caddy | Caddy 服务器的 Web 管理界面，支持反向代理、静态文件服务、HTTPS 自动配置 |
| luci-app-campusnet | 通用校园网认证客户端，适配多种校园网拨号协议 |
| luci-app-cd8021x | CDMA 802.1X 认证插件，用于企业/校园网的身份认证 |
| luci-app-cellled | 蜂窝网络（4G/5G）状态指示灯控制插件 |
| luci-app-cellularstatus | 蜂窝网络信号与状态监控插件 |
| luci-app-change-mac | 快速修改网口/WiFi MAC 地址的工具 |
| luci-app-chatgpt-web | ChatGPT Web 界面集成插件，可在路由器后台直接使用 AI 对话 |
| luci-app-chinadns-ng | ChinaDNS-NG 的 Web 管理界面，解决 DNS 污染问题 |
| luci-app-chinesesubfinder | 中文字幕自动搜索下载工具的后台管理插件 |
| luci-app-chongyoung | 冲浪加速器客户端，支持网络代理与分流 |
| luci-app-chongyoung2.0 | 冲浪加速器 2.0 版本，功能优化升级 |
| luci-app-cifs | CIFS/Samba 网络共享配置工具，挂载局域网共享文件夹 |
| luci-app-clash | Clash 代理客户端的 Web 管理界面，支持规则分流、节点订阅 |
| luci-app-cloudflarespeedtest | Cloudflare 节点测速工具的 Web 界面，筛选最快 CF IP |
| luci-app-cloudreve | Cloudreve 网盘系统的管理插件，自建私人网盘 |
| luci-app-codeserver | Code-Server（网页版 VS Code）的管理插件，在路由器上编写代码 |
| luci-app-control-timewol | 定时 Wake on LAN（WOL）唤醒插件，定时远程开机设备 |
| luci-app-control-webrestriction | 网页访问限制插件，屏蔽指定网站/关键词 |
| luci-app-control-weburl | URL 过滤插件，精准管控 HTTP/HTTPS 访问地址 |
| luci-app-coredns | CoreDNS 服务器的 Web 管理界面，灵活配置 DNS 解析规则 |
| luci-app-cpe | CPE（客户前置设备）管理插件，适配运营商定制设备 |
| luci-app-cpu-perf | CPU 性能监控与调优插件，显示 CPU 负载、频率等 |
| luci-app-cpu-status | CPU 状态实时监控插件，可视化显示使用率、温度 |
| luci-app-cpu-status-mini | 精简版 CPU 状态监控插件，占用更少系统资源 |
| luci-app-cpulimit | CPU 使用率限制插件，防止单个进程占用过多资源 |
| luci-app-cqustdotnet | 重庆邮电大学校园网认证客户端 |
| luci-app-csshnpd | 基于 SSH 的远程开机与管理插件 |
| luci-app-cupsd | CUPS 打印服务器的管理插件，实现路由器共享打印机 |
| luci-app-dae | DAE（DNS 与流量增强）插件，优化 DNS 解析与网络转发 |
| luci-app-daed | Daed 代理客户端，支持多种代理协议 |
| luci-app-daed-next | Daed 下一代代理客户端，功能更全面 |
| luci-app-ddnsto | DDNSTO 内网穿透工具的管理界面，无需公网 IP 访问内网设备 |
| luci-app-demon | 系统守护进程管理插件，监控关键服务运行状态 |
| luci-app-disks-info | 磁盘信息监控插件，显示硬盘分区、容量、挂载状态 |
| luci-app-dnscrypt-proxy2 | DNSCrypt-Proxy 2 的 Web 管理界面，加密 DNS 查询防止劫持 |
| luci-app-dnsfilter | DNS 过滤插件，屏蔽广告/恶意域名解析 |
| luci-app-dnsleaktest | DNS 泄漏检测工具，检查网络是否存在 DNS 泄漏风险 |
| luci-app-dnsmasq-ipset | DNSMASQ 与 ipset 集成插件，自动将解析结果加入 ipset 规则 |
| luci-app-dnspod | DNSPod DDNS 客户端，自动更新域名解析记录 |
| luci-app-dnsproxy | DNS 代理转发插件，自定义 DNS 服务器转发规则 |
| luci-app-dogcom | 校园网 Dr.COM 认证客户端 |
| luci-app-domain-proxy | 基于域名的反向代理插件 |
| luci-app-dpanel | 路由器控制面板插件，集成常用功能快捷入口 |
| luci-app-drawio | Draw.io 流程图工具的 Web 集成插件，在路由器后台绘制网络拓扑 |
| luci-app-droidmodem | 安卓手机调制解调器共享插件，将手机网络共享给路由器 |
| luci-app-droidnet | 安卓设备网络管理插件，实现路由器与安卓设备的联动 |
| luci-app-dsvpn | DS VPN 客户端，搭建点对点虚拟专用网络 |
| luci-app-dufs | Dufs 轻量级文件服务器的管理插件，支持网页上传/下载文件 |
| luci-app-dynv6 | Dynv6 DDNS 客户端，适配 IPv6 地址自动更新 |
| luci-app-easyconfig-transfer | 配置文件快速备份/迁移插件 |
| luci-app-easytier | EasyTier 内网穿透工具，支持多设备组网 |
| luci-app-easyupdate | 简易固件更新插件，手动选择固件包升级 |
| luci-app-einat | EINAT 网络加速插件，优化 TCP 传输协议 |
| luci-app-emby | Emby 媒体服务器管理插件，搭建家庭影音库 |
| luci-app-eqosplus | 增强版智能 QoS 插件，按设备/应用分配带宽优先级 |
| luci-app-excalidraw | Excalidraw 手绘风格绘图工具的 Web 集成插件 |
| luci-app-fakemesh | 虚拟 Mesh 组网插件，让普通路由器支持 Mesh 功能 |
| luci-app-fan | 路由器风扇控制插件，手动调节风扇转速 |
| luci-app-fancontrol | 智能风扇温控插件，根据 CPU 温度自动调节风扇转速 |
| luci-app-fastnet | 快速网络配置插件，一键设置常用网络参数 |
| luci-app-fchomo | 网络代理工具，支持多种协议转发 |
| luci-app-feishuvpn | 飞书 VPN 客户端，适配企业飞书组网环境 |
| luci-app-fileassistant | 文件管理助手，支持网页端上传/下载/删除路由器文件 |
| luci-app-filebrowser | FileBrowser 文件管理器的 Web 界面，管理路由器存储文件 |
| luci-app-filebrowser-go | Go 语言版 FileBrowser 管理插件，轻量化高性能 |
| luci-app-floatip | 浮动 IP 地址管理插件，用于多线接入环境的 IP 切换 |
| luci-app-forcedata | 数据强制转发插件，确保特定流量按指定规则传输 |
| luci-app-fullconenat | FullCone NAT 配置插件，优化 P2P 网络连接（如游戏、下载） |
| luci-app-gecoosac | Gecoos 加速器客户端，支持全球网络加速 |
| luci-app-glorytun-tcp | Glorytun TCP 协议 VPN 客户端，安全加密传输 |
| luci-app-glorytun-udp | Glorytun UDP 协议 VPN 客户端，低延迟传输 |
| luci-app-go-aliyundrive-webdav | 阿里云盘 WebDAV 服务插件，将阿里云盘挂载为本地磁盘 |
| luci-app-gobinetmodem | Go 语言编写的宽带调制解调器管理工具 |
| luci-app-gogs | Gogs 自建 Git 服务器管理插件，搭建私人代码仓库 |
| luci-app-gost | GOST 代理工具的 Web 管理界面，支持多种代理协议嵌套 |
| luci-app-gowebdav | Go 语言版 WebDAV 服务插件，轻量化文件共享 |
| luci-app-gpioled | GPIO 引脚指示灯控制插件，自定义指示灯状态 |
| luci-app-gpsysupgrade | 保留配置的系统升级插件，刷机不丢失配置 |
| luci-app-heimdall | Heimdall 应用仪表盘管理插件，聚合内网服务入口 |
| luci-app-homeassistant | Home Assistant 智能家居控制中心的管理插件 |
| luci-app-homebox | HomeBox 家庭资产管理工具的 Web 界面 |
| luci-app-homebridge | HomeBridge 插件，让非苹果设备接入苹果 HomeKit 生态 |
| luci-app-homeproxy | 家庭网络代理插件，支持规则分流与广告过滤 |
| luci-app-homeredirect | 家庭网络流量重定向插件，统一管理内网服务访问地址 |
| luci-app-htreader | HTML 文本阅读器插件，在路由器后台查看网页源码 |
| luci-app-hypercpe | 高性能 CPE 设备管理插件 |
| luci-app-hypermodem | 高速调制解调器管理插件，优化宽带连接速度 |
| luci-app-ikoolproxy | iKoolProxy 广告过滤插件，支持自定义规则 |
| luci-app-immich | Immich 照片备份工具的管理插件，搭建家庭照片库 |
| luci-app-interfaces-statistics | 网络接口流量统计插件，分网口显示上传/下载数据 |
| luci-app-internet-detector | 网络连通性检测插件，断网时自动触发指定操作（如重启拨号） |
| luci-app-iperf | iperf 网络测速工具的 Web 界面，测试局域网带宽 |
| luci-app-iperf3-server | iperf3 测速服务器插件，允许其他设备测试与路由器的连接速度 |
| luci-app-ipinfo | IP 地址信息查询插件，显示 IP 归属地、运营商等 |
| luci-app-iptvhelper | IPTV 助手插件，解决 IPTV 与路由器多网口冲突问题 |
| luci-app-ipv6clientfilter | IPv6 客户端过滤插件，管控 IPv6 设备的网络访问 |
| luci-app-istoredup | iStore 应用商店升级插件 |
| luci-app-istoreenhance | iStore 应用商店增强插件，拓展应用库 |
| luci-app-istorego | iStore Go 轻量级应用商店，适配低配路由器 |
| luci-app-istorepanel | iStore 应用商店控制面板 |
| luci-app-istorex | iStore X 应用商店，支持更多第三方插件 |
| luci-app-ittools | IT 工具集插件，集成 ping、traceroute 等网络诊断工具 |
| luci-app-jackett | Jackett 私服索引工具的管理插件，辅助下载工具检索资源 |
| luci-app-jederproxy | JederProxy 代理插件，支持多种协议 |
| luci-app-jellyfin | Jellyfin 媒体服务器管理插件，搭建家庭影音中心 |
| luci-app-k3screenctrl | 斐讯 K3 路由器屏幕控制插件，自定义屏幕显示内容 |
| luci-app-k3usb | 斐讯 K3 USB 端口管理插件，优化 USB 设备兼容性 |
| luci-app-koolproxyR | KoolProxyR 广告过滤插件，支持 HTTPS 广告拦截 |
| luci-app-kucat-config | Kucat 主题配置插件，自定义主题样式 |
| luci-app-lanraragi | Lanraragi 漫画服务器管理插件，搭建私人漫画库 |
| luci-app-libreswan | Libreswan IPsec VPN 服务器管理插件，搭建企业级 VPN |
| luci-app-linkease | 易有云插件，实现内网穿透、文件同步、远程管理 |
| luci-app-lite-watchdog | 精简版系统看门狗插件，监控服务状态并自动重启异常服务 |
| luci-app-log-viewer | 系统日志查看器，在网页端查看/导出路由器日志 |
| luci-app-lorawan-basicstation | LoRaWAN 基站管理插件，适配物联网 LoRa 设备 |
| luci-app-mac | MAC 地址管理插件，批量查看/修改设备 MAC |
| luci-app-macvlan | MACVLAN 虚拟网卡配置插件，创建多虚拟网口 |
| luci-app-mail | 邮件通知插件，系统事件（如断网、升级）触发邮件提醒 |
| luci-app-memos | Memos 备忘录工具的 Web 界面，在路由器后台记录笔记 |
| luci-app-mentohust | 校园网锐捷认证客户端（Mentohust 版本） |
| luci-app-mergerfs | MergerFS 磁盘合并插件，将多个磁盘合并为一个目录 |
| luci-app-mfun | 多功能工具插件，集成网络诊断、系统信息查询等 |
| luci-app-microsocks | MicroSocks 代理服务器管理插件，轻量化 SOCKS 代理 |
| luci-app-minieap | 迷你 802.1X 认证客户端，适配校园网/企业网认证 |
| luci-app-miniproxy | 迷你代理服务器插件，占用资源少 |
| luci-app-mlvpn | MLVPN 多链路 VPN 插件，聚合多条宽带提升带宽 |
| luci-app-mmconfig | 调制解调器多模式配置插件，切换 4G/5G 网络模式 |
| luci-app-mnh | 网络健康监控插件，检测网络延迟、丢包率 |
| luci-app-modem | 通用调制解调器管理插件，配置拨号参数、信号调试 |
| luci-app-modemband | 调制解调器频段锁定插件，手动选择 4G/5G 频段提升信号 |
| luci-app-modeminfo | 调制解调器详细信息插件，显示 IMEI、信号强度、基站信息等 |
| luci-app-momo | 网络代理工具，支持 SOCKS5 协议 |
| luci-app-mproxy | 多协议代理服务器插件 |
| luci-app-mptcp | MPTCP（多路径 TCP）配置插件，聚合多条网络链路传输数据 |
| luci-app-msd_lite | MSD Lite 协议插件，优化设备发现与通信 |
| luci-app-mtphotos | 美图相册管理插件，搭建私人照片存储服务 |
| luci-app-multiaccountdial | 多账号拨号插件，支持同时拨号多个宽带账号 |
| luci-app-mwan3-ledhelper | MWAN3 多线负载均衡的指示灯辅助插件，显示线路状态 |
| luci-app-mwol | 多设备 Wake on LAN 插件，批量远程唤醒局域网设备 |
| luci-app-my-dnshelper | 自定义 DNS 助手插件，灵活配置 DNS 转发规则 |
| luci-app-mymind | 思维导图工具的 Web 集成插件，在路由器后台绘制思维导图 |
| luci-app-nastools | NAS 工具集插件，集成媒体整理、下载管理等功能 |
| luci-app-nat6-helper | NAT6 辅助插件，优化 IPv6 网络的 NAT 转发 |
| luci-app-natmap | NATMap 内网穿透插件，无需公网 IP 实现端口映射 |
| luci-app-natmapt | NATMap 工具的 Web 管理界面 |
| luci-app-natter | Natter 内网穿透工具，支持 TCP/UDP 端口转发 |
| luci-app-natter2 | Natter 2.0 版本，功能优化 |
| luci-app-navidrome | Navidrome 音乐服务器管理插件，搭建私人音乐库 |
| luci-app-neko | Neko 远程桌面插件，实现浏览器远程控制设备 |
| luci-app-nekobox | Nekobox 代理客户端，支持多种代理协议 |
| luci-app-netkeeper-interception | 校园网闪讯认证拦截插件，适配闪讯拨号环境 |
| luci-app-netspeedtest | 网络速度测试插件，在网页端测试下载/上传速度 |
| luci-app-nettask | 网络任务调度插件，定时执行网络相关任务（如测速、重启） |
| luci-app-nextcloud | NextCloud 私有云盘管理插件，搭建个人云存储 |
| luci-app-nezha-agentv1 | 哪吒监控 Agent 插件，远程监控路由器状态 |
| luci-app-nginx | Nginx 服务器管理插件，配置反向代理、虚拟主机 |
| luci-app-nginx-ha | Nginx 高可用配置插件，实现双机热备 |
| luci-app-nginx-manager | Nginx 可视化管理插件，简化配置文件编写 |
| luci-app-nginx-pingos | Nginx 集成 PingOS 插件，支持流媒体服务 |
| luci-app-ngrokc | Ngrok 客户端管理插件，实现内网穿透 |
| luci-app-nikki | 网络优化插件，提升网页加载速度 |
| luci-app-njitclient | 南京邮电大学校园网认证客户端 |
| luci-app-nodogsplash | 开源热点认证插件，无需数据库即可实现 WiFi 认证 |
| luci-app-npc | NPC 内网穿透客户端，配合 frp 服务端使用 |
| luci-app-nvr | NVR（网络视频录像机）管理插件，管理监控摄像头 |
| luci-app-oaf | Open App Filter 应用过滤插件，按应用程序管控网络访问 |
| luci-app-oneapi | OneAPI 多平台 AI 接口聚合插件，统一调用多种 AI 服务 |
| luci-app-onliner | 在线设备监控插件，实时显示连接到路由器的设备列表 |
| luci-app-openclash | OpenClash 增强版 Clash 插件，支持更多功能与规则 |
| luci-app-openwebui | OpenWebUI 管理插件，适配大语言模型前端界面 |
| luci-app-oscam | OSCam 卫星电视解码服务器管理插件 |
| luci-app-ota | OTA（空中下载）升级插件，支持设备固件远程升级 |
| luci-app-owntone | Owntone 音乐服务器插件，支持 AirPlay 音频传输 |
| luci-app-package-manager | 软件包管理器插件，在线安装/卸载 OpenWrt 插件 |
| luci-app-packagesync | 软件包同步插件，同步路由器与指定源的软件包版本 |
| luci-app-packet-capture | 网络抓包工具插件，捕获并分析网络数据包 |
| luci-app-parentcontrol | 家长控制插件，限制儿童设备的上网时间与内容 |
| luci-app-partexp | 分区扩展插件，扩展路由器存储分区大小 |
| luci-app-passwall2 | PassWall 2 代理插件，支持多种协议，规则分流更灵活 |
| luci-app-pcimodem | PCIe 调制解调器管理插件，适配 PCIe 接口的 4G/5G 模块 |
| luci-app-penpot | Penpot 设计工具的 Web 集成插件，在线 UI/UX 设计 |
| luci-app-photoprism | PhotoPrism 照片管理插件，AI 分类整理照片 |
| luci-app-pikpak-webdav | 阿里云盘 PikPak WebDAV 服务插件 |
| luci-app-pingcontrol | Ping 监控插件，定时 Ping 指定 IP，断网时触发告警 |
| luci-app-plex | Plex 媒体服务器管理插件，搭建家庭影音中心，支持多设备同步 |
| luci-app-poweroff | 路由器关机插件，网页端一键关闭路由器 |
| luci-app-poweroffdevice | 设备断电控制插件，配合智能插座远程关闭设备电源 |
| luci-app-pppoe-server | PPPoE 服务器插件，让路由器作为 PPPoE 拨号服务端 |
| luci-app-pppoe-user | PPPoE 账号管理插件，添加/删除 PPPoE 拨号用户 |
| luci-app-pptpd | PPTP VPN 服务器插件，搭建基础 VPN 服务 |
| luci-app-public-ip-monitor | 公网 IP 监控插件，IP 变化时触发通知（邮件/短信） |
| luci-app-pve | Proxmox VE 管理插件，远程管理 PVE 虚拟化平台 |
| luci-app-qos-emong | 增强版 QoS 流量控制插件，优化带宽分配 |
| luci-app-qosmate | QoS 伴侣插件，辅助优化流量优先级 |
| luci-app-quickstart | 快速配置向导插件，新路由器一键设置网络参数 |
| luci-app-redsocks | RedSocks 代理工具管理插件，支持透明代理 |
| luci-app-routerdog | 路由器看门狗插件，监控系统负载，过载时自动重启 |
| luci-app-rtbwmon | 实时带宽监控插件，显示当前各设备的带宽使用情况 |
| luci-app-rtorrent | rTorrent 下载工具管理插件，支持 BT/PT 下载 |
| luci-app-runmynas | 私人 NAS 搭建插件，集成文件共享、下载等功能 |
| luci-app-rustdesk-server | RustDesk 远程桌面服务器插件，搭建私人远程控制服务 |
| luci-app-school | 通用校园网插件，适配多种校园网认证协议 |
| luci-app-scutclient | 华南理工大学校园网认证客户端 |
| luci-app-shadowrt | ShadowRT 代理插件，支持 RT 协议 |
| luci-app-shadowsocks | Shadowsocks 代理客户端管理插件，经典加密代理协议 |
| luci-app-shadowsocks-rust | Rust 语言版 Shadowsocks 插件，性能更高 |
| luci-app-shanligong | 山里工代理插件，支持多种协议 |
| luci-app-shortcutmenu | 快捷菜单插件，在 LuCI 后台添加常用功能快捷入口 |
| luci-app-shutdown | 路由器重启/关机插件，网页端一键操作 |
| luci-app-smartvpn | 智能 VPN 插件，自动选择最优节点连接 |
| luci-app-smbuser | Samba 共享用户管理插件，添加/删除共享账号 |
| luci-app-sms-tool | 短信工具插件，通过 4G/5G 模块发送/接收短信 |
| luci-app-sms-tool-js | JS 版短信工具插件，界面更友好 |
| luci-app-snmpd | SNMP 服务器插件，允许网络管理软件监控路由器状态 |
| luci-app-spdmodem | 高速调制解调器插件，优化 5G 网络传输速度 |
| luci-app-speedtest-web | Speedtest 网页版测速插件，测试宽带真实速度 |
| luci-app-spotifyd | Spotifyd 音乐服务插件，将 Spotify 音乐流传输到音频设备 |
| luci-app-sqm-autorate | SQM 智能队列管理插件，自动调整队列参数优化网络 |
| luci-app-squid-adv | 增强版 Squid 代理服务器插件，支持缓存、访问控制 |
| luci-app-ss-redir | Shadowsocks 透明代理插件，实现全局代理 |
| luci-app-ssr-mudb-server | SSR Mudb 服务器插件，搭建 ShadowsocksR 服务端 |
| luci-app-ssr-plus | ShadowsocksR Plus+ 插件，集成多种代理协议与规则分流 |
| luci-app-ssw | SSW 代理插件，简化 Shadowsocks 配置 |
| luci-app-store | OpenWrt 官方应用商店插件，在线安装插件 |
| luci-app-strongswan-swanctl | StrongSwan IPsec VPN 客户端管理插件，适配 IKEv2 协议 |
| luci-app-subconverter | SubConverter 订阅转换插件，将不同格式的代理订阅转换为统一格式 |
| luci-app-sunpanel | 向日葵远程控制插件，实现外网远程控制路由器 |
| luci-app-supervisord | Supervisord 进程管理插件，监控并自动重启指定进程 |
| luci-app-suselogin | 苏大校园网认证客户端 |
| luci-app-switch-lan-play | LAN Play 联机插件，支持 Switch 游戏机局域网联机 |
| luci-app-switchtools | 交换机工具插件，配置网口 VLAN、端口镜像等 |
| luci-app-syncthing | Syncthing 文件同步插件，实现多设备文件自动同步 |
| luci-app-synology | 群晖 NAS 管理插件，远程管理群晖设备 |
| luci-app-syscontrol | 系统控制插件，调整系统内核参数、优化性能 |
| luci-app-systools | 系统工具集插件，集成系统信息、硬件检测等功能 |
| luci-app-sysuh3c | 华中科技大学 H3C 校园网认证客户端 |
| luci-app-tailscale | Tailscale 组网工具插件，搭建零配置虚拟局域网 |
| luci-app-tailscale-community | 社区版 Tailscale 插件，适配更多架构 |
| luci-app-taskplan | 任务计划插件，定时执行自定义 Shell 脚本 |
| luci-app-tasks | 系统任务管理插件，查看/管理后台运行的任务 |
| luci-app-taskschedule | 高级任务调度插件，支持复杂的定时规则 |
| luci-app-tcpdump | TCPDump 抓包工具的 Web 界面，捕获网络数据包并导出 |
| luci-app-telegrambot | Telegram 机器人插件，通过 Telegram 远程控制路由器 |
| luci-app-temp-status | 温度状态监控插件，显示 CPU/主板温度 |
| luci-app-tencentcloud-cos | 腾讯云 COS 对象存储插件，备份路由器配置/文件到云端 |
| luci-app-tencentddns | 腾讯云 DDNS 客户端，自动更新域名解析 |
| luci-app-timecontrol | 时间控制插件，按时间段开启/关闭指定功能 |
| luci-app-timedreboot | 定时重启插件，设置路由器定时自动重启 |
| luci-app-timewol | 定时 Wake on LAN 插件，定时唤醒指定设备 |
| luci-app-tinyfilemanager | 迷你文件管理器插件，轻量化文件管理 |
| luci-app-tn-lldpd | LLDP 协议插件，发现局域网内的网络设备 |
| luci-app-tn-netports | 网络端口监控插件，显示端口占用情况 |
| luci-app-torbp | Tor 网络网桥插件，接入 Tor 匿名网络 |
| luci-app-trojan-server | Trojan 代理服务器插件，搭建 Trojan 服务端 |
| luci-app-ttl | TTL 值修改插件，调整网络数据包的 TTL 值 |
| luci-app-ttnode | 甜糖星愿节点插件，共享宽带获取积分 |
| luci-app-typecho | Typecho 博客系统管理插件，在路由器上搭建个人博客 |
| luci-app-ua2f | UA2F 插件，模拟 HTTP/2 指纹，提升网络兼容性 |
| luci-app-ubuntu | Ubuntu 系统容器插件，在路由器上运行 Ubuntu 系统 |
| luci-app-ubuntu2 | Ubuntu 系统容器 2.0 版本，功能优化 |
| luci-app-udp2raw | UDP2RAW 工具管理插件，将 UDP 流量伪装成 TCP 传输 |
| luci-app-unblockneteasemusic | 解锁网易云音乐灰色歌曲插件，支持无损音质播放 |
| luci-app-unifi | UniFi 设备管理插件，管理 Ubiquiti UniFi 系列设备 |
| luci-app-unishare | 统一共享插件，整合多种存储设备的共享服务 |
| luci-app-uptimekuma | Uptime Kuma 监控插件，监控内网/外网服务的在线状态 |
| luci-app-usb3disable | USB 3.0 端口禁用插件，解决 USB 3.0 对 WiFi 的干扰问题 |
| luci-app-usbmodem | USB 调制解调器管理插件，适配 USB 4G/5G 模块 |
| luci-app-v2raya | V2RayA 代理客户端插件，可视化配置 V2Ray 规则 |
| luci-app-vaultwarden | Vaultwarden 密码管理器插件，搭建私人密码库 |
| luci-app-vnt | VNT 虚拟组网插件，实现多设备互联互通 |
| luci-app-wan-mac | WAN 口 MAC 地址修改插件，快速修改拨号口 MAC |
| luci-app-watchdog | 系统看门狗插件，监控系统状态，异常时自动重启 |
| luci-app-webd | WebDAV 服务器插件，实现文件网络共享 |
| luci-app-webrestriction | 网页访问限制插件，屏蔽指定网站 |
| luci-app-webviewdev | WebView 开发调试插件，适配网页开发场景 |
| luci-app-webvirtcloud | WebVirtCloud 虚拟机管理插件，远程管理 KVM 虚拟机 |
| luci-app-wechatpush | 微信推送插件，系统事件触发微信消息提醒 |
| luci-app-wifidog | WiFiDog 热点认证插件，用于公共 WiFi 认证 |
| luci-app-wizard | 新手配置向导插件，引导用户完成路由器初始化配置 |
| luci-app-wolplus | 增强版 Wake on LAN 插件，支持远程唤醒外网设备 |
| luci-app-wxedge | 网心云边缘计算插件，共享宽带获取收益 |
| luci-app-xclient | XClient 代理客户端，支持多种协议 |
| luci-app-xjay | XJay 代理插件，优化网络传输速度 |
| luci-app-xray | Xray 代理客户端管理插件，支持 VLESS、Trojan 等协议 |
| luci-app-xray-geodata | Xray 地理数据库插件，用于 IP 地理位置分流 |
| luci-app-xray-status | Xray 连接状态监控插件，显示节点延迟、流量使用情况 |
| luci-app-xteve | Xteve 直播流转发插件，整合 IPTV 直播源 |
| luci-app-xunlei | 迅雷下载插件，在路由器上进行 BT/磁力链接下载 |
| luci-app-xunyou | 迅游加速器客户端，优化游戏网络 |
| luci-app-xupnpd | XUPnP 插件，实现 UPnP 协议端口映射 |
| luci-app-xwan | XWAN 多线聚合插件，提升网络带宽与稳定性 |
| luci-app-yggdrasil | Yggdrasil 去中心化网络插件，接入加密 IPv6 网络 |
| luci-app-ympd | ympd 音乐播放器插件，网页端控制音乐播放 |
| luci-app-yt-dlp | yt-dlp 视频下载工具插件，下载 YouTube 等平台视频 |
| luci-app-zdinnav | ZDIN 导航页插件，搭建内网服务导航主页 |

## 二、 【其他工具】（172个）
此类为**命令行工具/后台服务**，无 Web 界面，需通过 SSH 或脚本调用，是 LuCI 应用的底层依赖或独立功能工具。
| 工具名称 | 核心功能 |
| ---- | ---- |
| 3ginfo | 命令行版 3G/4G 调制解调器信息查询工具 |
| 7z | 7-Zip 压缩/解压工具，支持多种格式 |
| CloudflareSpeedTest | 命令行版 Cloudflare 节点测速工具 |
| DaoNet | 道网络优化工具，提升网络传输效率 |
| HomeRedirect | 后台版家庭网络流量重定向服务 |
| LingTiGameAcc | 玲珑加速器后台服务程序 |
| RHash | 哈希值计算工具，支持 MD5、SHA 等算法 |
| ShadowVPN | ShadowVPN 后台服务，轻量级加密 VPN |
| Toolkit | 多功能命令行工具集，集成网络诊断、系统信息等 |
| aihelper | AI 助手后台服务程序 |
| airconnect | 无线桥接后台服务，实现多设备无线组网 |
| alac | ALAC 音频解码工具，支持无损音频格式 |
| alwaysonline | 网络保活后台服务，防止连接断开 |
| amule | aMule P2P 下载工具，支持 eDonkey 网络 |
| atinout | AT 指令测试工具，调试 4G/5G 模块 |
| autokick-wiwiz | 自动踢除未授权设备的后台服务 |
| autoshare-ksmbd | KSMBD 协议自动共享服务，优化 Samba 性能 |
| autoupdate | 固件自动更新后台服务 |
| bandix | 带宽控制后台工具 |
| boltbrowser | 命令行版文件浏览器 |
| brlaser | 兄弟打印机驱动工具 |
| caddy | Caddy 服务器后台程序 |
| cellled | 蜂窝网络指示灯控制后台服务 |
| cloudreve | Cloudreve 网盘后台服务 |
| cpulimit-ng | CPU 使用率限制工具（下一代版本） |
| cups-bjnp | CUPS 打印机 BJNP 协议支持工具 |
| daed-next | Daed 代理后台服务（下一代版本） |
| dcc2-wiwiz | Wiwiz 热点认证 DCC2 协议支持工具 |
| dhrystone | CPU 性能基准测试工具 |
| docker-lan-bridge | Docker 局域网桥接工具，让容器接入局域网 |
| docs | 文档生成工具，生成 OpenWrt 配置文档 |
| dogcom | 校园网 Dr.COM 认证后台程序 |
| duperemove | 重复文件查找与删除工具 |
| einat-ebpf | EINAT 网络加速的 eBPF 程序，优化内核网络转发 |
| eqos | 智能 QoS 后台服务，分配带宽优先级 |
| fail2banop | Fail2Ban 后台操作工具，防止暴力破解 |
| fan2go | 智能风扇控制工具，支持多传感器温控 |
| fancontrol | 风扇控制后台服务 |
| fastfetch | 系统信息快速查询工具，替代 neofetch |
| fastnet | 快速网络配置后台工具 |
| ffmpeg-remux | FFmpeg 视频格式转换工具，仅处理封装格式不重新编码 |
| ffmpeg-static | 静态编译版 FFmpeg，无需依赖库即可运行 |
| files | 轻量级文件管理工具 |
| flash_fox | 闪存优化工具，延长路由器闪存寿命 |
| floatip | 浮动 IP 地址管理后台服务 |
| gallery-dl | 图片批量下载工具，支持多个图片网站 |
| gecoosac | Gecoos 加速器后台服务 |
| glorytun | Glorytun VPN 协议核心程序 |
| glorytun-udp | Glorytun UDP 协议实现程序 |
| gn | GN 构建系统工具，用于编译大型项目 |
| go-nats | Go 语言版 NATS 消息队列客户端 |
| go-stun | Go 语言版 STUN 协议工具，获取公网 NAT 类型 |
| go-wol | Go 语言版 Wake on LAN 工具 |
| gotop | Go 语言版系统监控工具，可视化显示系统资源 |
| grpcurl | gRPC 服务调试工具，发送 gRPC 请求 |
| homebox | HomeBox 资产管后台服务 |
| hv-tools | 硬件虚拟化工具集 |
| ifmetric | 网络接口优先级设置工具，调整路由优先级 |
| internet-detector | 网络连通性检测后台服务 |
| internet-detector-mod-email | 网络检测邮件通知模块，断网时发送邮件 |
| internet-detector-mod-modem-restart | 网络检测调制解调器重启模块，断网时重启拨号 |
| internet-detector-mod-telegram | 网络检测 Telegram 通知模块，断网时发送消息 |
| ipcalc | IP 地址计算工具，计算子网掩码、网关等 |
| ipset-lists | ipset 规则集管理工具，批量导入/导出规则 |
| iptvhelper | IPTV 助手后台服务，解决多网口冲突 |
| istoreenhance | iStore 应用商店增强后台服务 |
| joker | 网络测试工具，模拟各种网络请求 |
| jpcre2 | PCRE2 正则表达式库的 Java 绑定 |
| lcdsimple | 简易 LCD 屏幕控制工具 |
| libcron | Cron 定时任务库，用于开发定时功能插件 |
| libdouble-conversion | 浮点数转换库，用于高精度数值处理 |
| linkease | 易有云后台服务程序 |
| linkmount | 网络存储挂载工具，挂载云盘/局域网共享 |
| lmotool | 调制解调器锁频工具，锁定 4G/5G 频段 |
| lua-ipops | Lua 语言 IP 地址操作库，用于插件开发 |
| lua-maxminddb | Lua 语言 MaxMind DB 数据库库，用于 IP 地理查询 |
| lux | 命令行视频下载工具，支持多个平台 |
| maxminddb-dump-country | MaxMind DB 国家数据库导出工具 |
| mergerfs | MergerFS 磁盘合并工具，合并多个磁盘目录 |
| mhz | 频率检测工具，检测 CPU/内存频率 |
| mihomo | 米哈游代理工具后台服务 |
| minisign | 轻量级数字签名工具，验证文件完整性 |
| mnh | 网络健康监控后台服务 |
| modeminfo | 调制解调器信息查询命令行工具 |
| momo | Momo 代理后台服务 |
| mptcp | MPTCP 协议核心模块，实现多路径 TCP 传输 |
| mrtg | MRTG 网络流量监控工具，生成流量统计图 |
| mwan3-ledhelper | MWAN3 多线负载均衡指示灯辅助后台服务 |
| my-default-settings | 自定义默认配置工具，修改路由器出厂设置 |
| nanohatoled | NanoHat OLED 屏幕控制工具 |
| natflow | NAT 流量统计工具，分析 NAT 转发数据 |
| natmapt | NATMap 内网穿透后台服务 |
| natter | Natter 内网穿透后台服务 |
| natter2 | Natter 2.0 后台服务 |
| ndisc6 | IPv6 邻居发现工具，诊断 IPv6 网络 |
| netkeeper | 校园网闪讯认证后台程序 |
| netkeeper-interception | 闪讯认证拦截后台服务 |
| netmaker | Netmaker 组网工具后台服务，搭建虚拟局域网 |
| netspeedtest | 网络速度测试命令行工具 |
| neturl | URL 解析库，用于插件开发 |
| nexttrace | 高级路由追踪工具，显示节点 IP 归属地 |
| nezha-agentv1 | 哪吒监控 Agent 后台服务 |
| nvtop | NVIDIA GPU 监控工具，适配带 GPU 的路由器 |
| oaf | Open App Filter 后台服务，实现应用过滤 |
| ookla-speedtest | Ookla Speedtest 官方测速工具，精准测试宽带速度 |
| opencode | 开源代码编译辅助工具 |
| openlist2 | 开源列表管理工具，用于维护域名/IP 规则列表 |
| openwrt-dist-luci | OpenWrt 发行版 LuCI 依赖库 |
| pcat-mgr | 进程捕获与管理工具 |
| peanut | 轻量级网络代理工具 |
| pingcontrol | Ping 监控后台服务 |
| po2lmo | PO 翻译文件转 LMO 格式工具，用于 LuCI 界面本地化 |
| q | 命令行 JSON 处理工具，格式化/查询 JSON 数据 |
| qosmate | QoS 伴侣后台服务，优化带宽分配 |
| qt6base | Qt6 基础库，用于开发图形界面插件 |
| qt6tools | Qt6 开发工具集 |
| quickjspp | QuickJS++ 脚本引擎，增强 Lua 插件的功能 |
| quickstart | 快速配置后台服务 |
| rapidjson | RapidJSON 库，高性能 JSON 解析器 |
| redsocks2 | RedSocks2 代理工具，支持透明代理 |
| rgmac | MAC 地址随机生成工具 |
| rkp-ipid | IPID 优化工具，提升网络隐蔽性 |
| routergo | 路由器网络优化工具，基于 Go 语言 |
| rrm-nr-distributor | 无线资源管理分布式工具，优化 WiFi 信号 |
| rtl8189es | RTL8189ES 无线网卡驱动工具 |
| rust-bindgen | Rust 语言绑定生成工具，用于 Rust 与 C 语言交互 |
| speedtest-cli | Speedtest 命令行版测速工具 |
| speedtestcli | 第三方 Speedtest 命令行工具 |
| sqm-autorate | SQM 智能队列管理后台服务 |
| stuntman | STUN 协议测试工具，获取 NAT 信息 |
| subconverter | SubConverter 订阅转换后台服务 |
| sunpanel | 向日葵远程控制后台服务 |
| supervisor | Supervisord 进程管理工具，监控后台进程 |
| switch-lan-play | LAN Play 联机后台服务，支持 Switch 联机 |
| taskd | 任务调度后台服务 |
| tcp-brutal | TCP 协议优化工具，提升传输速度 |
| tcptraceroute | TCP 协议路由追踪工具，诊断网络故障 |
| telegrambot | Telegram 机器人后台服务 |
| tinyPortMapper | 轻量级端口映射工具，实现内网穿透 |
| tinymembench | 内存性能基准测试工具 |
| toml11 | TOML 配置文件解析库 |
| torrserver | Torrent 流媒体服务器，边下载边播放 |
| totd | DNS 轮询工具，实现 DNS 负载均衡 |
| tracebox | 高级网络追踪工具，检测网络中间设备 |
| transfer | 文件传输工具，支持多种协议 |
| tsping | TCP 协议 Ping 工具，测试 TCP 端口连通性 |
| tuic-server | TUIC 代理服务器后台程序 |
| tun2socks | TUN 设备转 SOCKS 代理工具，实现全局代理 |
| tvhelper | 电视直播辅助工具，优化 IPTV 流 |
| udp2raw | UDP2RAW 后台服务，伪装 UDP 流量 |
| unishare | 统一共享后台服务 |
| upx-static | 静态编译版 UPX 压缩工具，压缩可执行文件 |
| vmease | 虚拟网络测量工具 |
| watchdog | 系统看门狗后台服务，监控系统状态 |
| wifidog-wiwiz | WiFiDog 与 Wiwiz 认证集成工具 |
| wrtbwmon | 实时带宽监控后台服务 |
| xmm-modem | XMM 调制解调器管理工具 |
| xt_tls | Linux 内核 TLS 模块，用于网络加密 |
| xtables-wgobfs | iptables 插件，伪装 WireGuard 流量 |
| xunyou | 迅游加速器后台服务 |
| ykdl | 优酷视频下载工具 |
| ympd | ympd 音乐播放器后台服务 |
| you-get | 命令行视频下载工具，支持多个国内平台 |
| z8102 | Z8102 芯片驱动工具，适配特定硬件 |

## 三、 【LuCI 主题】（17个）
LuCI 主题是 **Web 界面的皮肤**，仅改变后台的外观样式，不影响功能，可根据喜好选择。
| 主题名称 | 风格特点 |
| ---- | ---- |
| luci-theme-argon | 简洁现代风格，支持自定义背景、暗色模式 |
| luci-theme-argon-dark | Argon 主题的暗色版本 |
| luci-theme-argon-light | Argon 主题的亮色版本 |
| luci-theme-atmaterial | 仿 Material Design 风格，扁平化界面 |
| luci-theme-bootstrap | OpenWrt 原生默认主题，简洁朴素 |
| luci-theme-darkmatter | 深色主题，高对比度，护眼 |
| luci-theme-edge | 边缘风格主题，简约流畅 |
| luci-theme-ifit | 适配 IFIT 路由器的主题 |
| luci-theme-inas | 清新风格主题，浅色基调 |
| luci-theme-kucat | 卡通风格主题，界面活泼 |
| luci-theme-lightblue | 浅蓝色主题，简洁明快 |
| luci-theme-material3 | 基于 Material You 设计的主题，支持动态色彩 |
| luci-theme-merona | 暖色调主题，温馨风格 |
| luci-theme-openmptcprouter | 适配 OpenMPTCProuter 的主题 |
| luci-theme-opentopd | 仿 Topd 路由器界面风格 |
| luci-theme-routerich | 仿华硕路由器界面风格 |
| luci-theme-spectra | 多彩主题，支持多种配色方案 |
| luci-theme-teleofis | 仿电信光猫界面风格 |
| luci-theme-tomato | 仿 Tomato 路由器界面风格 |

## 四、 【网络工具】（12个）
独立的**网络代理/VPN 核心工具**，无 Web 界面，需配合 LuCI 应用使用，或通过配置文件手动配置。
| 工具名称 | 核心功能 |
| ---- | ---- |
| dsvpn | DS VPN 协议核心程序，搭建点对点 VPN |
| koolproxy | KoolProxy 广告过滤核心程序，支持 HTTP/HTTPS 广告拦截 |
| mlvpn | MLVPN 多链路 VPN 核心程序，聚合多条宽带 |
| mproxy | 多协议代理核心程序，支持 HTTP/SOCKS 等 |
| mtproxy | MTProxy 协议核心程序，代理 Telegram 流量 |
| openvpn-dns-hotplug | OpenVPN DNS 热插拔工具，VPN 连接时自动切换 DNS |
| ss-redir | Shadowsocks 透明代理核心程序 |
| ssd1306 | SSD1306 OLED 屏幕驱动工具，用于显示网络状态 |
| ssocks | SSocks 代理工具，支持 SOCKS4/5 协议 |
| ssw | SSW 代理核心程序，简化 Shadowsocks 配置 |
| trojan-go | Go 语言版 Trojan 代理程序，性能更高 |
| v2ray-core | V2Ray 代理核心程序，支持多种协议 |

## 五、 【其他 LuCI 包】（9个）
LuCI 插件的**依赖库/扩展模块**，为其他 LuCI 应用提供功能支持，一般无需单独编译（依赖时会自动选中）。
| 包名称 | 功能作用 |
| ---- | ---- |
| luci-lib-iform | LuCI 表单扩展库，简化插件表单开发 |
| luci-lib-mac-vendor | MAC 地址厂商查询库，显示设备品牌 |
| luci-lib-taskd | LuCI 任务调度库，用于开发定时任务功能 |
| luci-lib-xterm | LuCI 终端模拟器库，在网页端实现 SSH 终端 |
| luci-lighttpd | Lighttpd 服务器 LuCI 集成库 |
| luci-mod-istorenext | iStore 应用商店扩展模块 |
| luci-mod-listening-ports | 监听端口显示模块，查看路由器开放的端口 |
| luci-nginxer | Nginx 服务器 LuCI 集成库 |
| luci-themedog | LuCI 主题开发工具库，辅助主题开发 |

## 六、 【LuCI 协议】（7个）
为 LuCI 提供**特定网络协议的配置支持**，用于配置拨号、认证等协议，需配合对应硬件/服务使用。
| 协议名称 | 适用场景 |
| ---- | ---- |
| luci-proto-minieap | 迷你 802.1X 认证协议配置，适配校园网 |
| luci-proto-netkeeper | 闪讯校园网认证协议配置 |
| luci-proto-quectel | 移远通信 4G/5G 模块协议配置 |
| luci-proto-tinc | Tinc VPN 协议配置 |
| luci-proto-tun2socks | TUN2SOCKS 协议配置，实现全局代理 |
| luci-proto-wwan | 无线广域网（4G/5G）协议配置 |
| luci-proto-xmm | XMM 调制解调器协议配置 |

## 七、 【DNS/广告过滤】（5个）
专注于 **DNS 优化、广告拦截** 的工具，解决 DNS 污染、屏蔽恶意域名。
| 工具名称 | 核心功能 |
| ---- | ---- |
| appfilter | 应用层广告过滤工具，屏蔽 App 内置广告 |
| ddnsto | DDNSTO 内网穿透 DNS 工具，无需公网 IP |
| dns2socks-rust | Rust 语言版 DNS 转 SOCKS 工具，加密 DNS 查询 |
| hickory-dns | Hickory DNS 服务器，轻量级 DNS 解析工具 |
| my-dnshelper | 自定义 DNS 助手，灵活配置转发规则 |

## 八、 【文件共享】（3个）
用于 **局域网/外网文件共享** 的工具，实现文件的上传、下载、访问。
| 工具名称 | 核心功能 |
| ---- | ---- |
| autoshare-samba | Samba 自动共享工具，自动挂载磁盘并共享 |
| pikpak-webdav | 阿里云盘 PikPak WebDAV 服务，挂载云盘 |
| webdav2 | WebDAV 服务增强版，优化文件传输性能 |

## 九、 【Web 服务】（3个）
提供 **Web 服务器/相关功能**，用于搭建网站、测速、代理管理。
| 工具名称 | 核心功能 |
| ---- | ---- |
| speedtest-web | Web 版 Speedtest 测速服务，供局域网设备测速 |
| sub-web | 代理订阅管理 Web 服务，可视化管理订阅链接 |
| webd | WebDAV 服务器核心程序，实现文件共享 |

## 十、 【监控工具】（1个）
| 工具名称 | 核心功能 |
| ---- | ---- |
| ethstatus | 以太网接口状态监控工具，显示网口连接状态、速度 |

## 十一、 【下载工具】（1个）
| 工具名称 | 核心功能 |
| ---- | ---- |
| qBittorrent-Enhanced-Edition | 增强版 qBittorrent 下载工具，支持 BT/PT 下载，功能更丰富 |



## 手动运行（本地开发）

### 1. 克隆仓库

```bash
git clone --depth=1 https://github.com/JacksonJiangxh/openwrt-package.git jackson
cd jackson
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
