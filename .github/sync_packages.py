#!/usr/bin/env python3
"""
OpenWrt 软件包同步脚本

功能：
1. 从多个源仓库同步软件包
2. 自动去重，保留最新版本
3. 智能版本比较
4. 详细日志记录
"""

import os
import shutil
import git
import argparse
from pathlib import Path
from datetime import datetime

# 尝试导入packaging.version来处理语义化版本
try:
    from packaging.version import parse as parse_version
    HAS_PACKAGING = True
except ImportError:
    HAS_PACKAGING = False


class PackageSyncer:
    """OpenWrt 软件包同步器"""
    
    def __init__(self, work_dir, output_dir):
        """
        初始化同步器
        
        Args:
            work_dir: 临时工作目录，用于存储克隆的源仓库
            output_dir: 输出目录，用于存储同步后的软件包
        """
        self.work_dir = Path(work_dir)
        self.output_dir = Path(output_dir)
        
        # 统计信息
        self.stats = {
            "initial_count": 0,
            "new_packages": 0,
            "updated_packages": 0,
            "skipped_packages": 0
        }
        
        # 已有的软件包版本信息和目录映射
        self.existing_packages = {}
        self.package_dirs = {}  # 存储小写 PKG_NAME 到目录名的映射
        
        # 确保目录存在
        self.work_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 扫描已存在的软件包
        self._scan_existing_packages()
        self.stats["initial_count"] = len(self.existing_packages)
    
    def _scan_existing_packages(self):
        """扫描输出目录中已存在的软件包，记录版本信息和目录映射"""
        keep_items = [".git", ".github", ".gitignore", "README.md", "sync_packages.py", "temp_repos"]
        
        for item in self.output_dir.iterdir():
            if item.name in keep_items:
                continue
            
            if item.is_dir():
                makefile_path = item / "Makefile"
                if makefile_path.exists():
                    pkg_info = self._parse_makefile(makefile_path)
                    pkg_name = pkg_info.get("PKG_NAME") or item.name
                    # 统一转换为小写，避免大小写冲突
                    normalized_pkg_name = pkg_name.lower()
                    self.existing_packages[normalized_pkg_name] = {
                        "version": pkg_info.get("PKG_VERSION", "0"),
                        "release": pkg_info.get("PKG_RELEASE", "0")
                    }
                    # 记录小写 PKG_NAME 到目录名的映射
                    if normalized_pkg_name not in self.package_dirs:
                        self.package_dirs[normalized_pkg_name] = []
                    self.package_dirs[normalized_pkg_name].append(item.name)
    
    def _parse_makefile(self, makefile_path):
        """
        解析Makefile文件，提取软件包信息
        
        Args:
            makefile_path: Makefile文件路径
            
        Returns:
            dict: 包含PKG_NAME, PKG_VERSION, PKG_RELEASE的字典
        """
        pkg_info = {
            "PKG_NAME": "",
            "PKG_VERSION": "0",
            "PKG_RELEASE": "0"
        }
        
        try:
            with open(makefile_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("PKG_NAME:="):
                        pkg_info["PKG_NAME"] = line.split(":=")[1].strip()
                    elif line.startswith("PKG_VERSION:="):
                        pkg_info["PKG_VERSION"] = line.split(":=")[1].strip()
                    elif line.startswith("PKG_RELEASE:="):
                        pkg_info["PKG_RELEASE"] = line.split(":=")[1].strip()
        except Exception as e:
            print(f"解析Makefile失败 {makefile_path}: {e}")
        
        return pkg_info
    
    def _compare_versions(self, ver1, ver2):
        """
        智能版本比较逻辑，优先使用语义化版本库，回退到自定义实现
        
        Args:
            ver1: 版本字符串1
            ver2: 版本字符串2
            
        Returns:
            1: ver1 > ver2
            0: ver1 == ver2
            -1: ver1 < ver2
        """
        # 转换为字符串，确保处理一致性
        ver1 = str(ver1)
        ver2 = str(ver2)
        
        # 如果两个版本字符串完全相同，直接返回相等
        if ver1 == ver2:
            return 0
        
        # 优先使用packaging.version库进行语义化版本比较
        if HAS_PACKAGING:
            try:
                v1 = parse_version(ver1)
                v2 = parse_version(ver2)
                
                if v1 > v2:
                    return 1
                elif v1 < v2:
                    return -1
                else:
                    return 0
            except Exception:
                # 静默失败，直接使用自定义比较，减少日志噪音
                pass
        
        # 自定义版本比较逻辑，处理各种非标准格式
        def normalize(v):
            """标准化版本字符串为可比较的列表"""
            # 处理特殊情况
            if not v or v.startswith("$"):
                return [0]
            
            # 替换特殊字符为点号，统一分隔符
            normalized = v.replace("_", ".").replace("-", ".").replace("+", ".")
            
            # 处理OpenWrt特殊版本格式，如git-xxx
            if "git" in normalized:
                normalized = normalized.replace("git", "0")
            
            # 分割并标准化每个部分
            parts = []
            for part in normalized.split("."):
                part = part.strip()
                if not part:
                    continue
                try:
                    # 尝试转换为整数
                    parts.append(int(part))
                except ValueError:
                    # 如果是字符串，直接使用
                    parts.append(part)
            
            # 确保至少有一个部分，避免空列表
            return parts if parts else [0]
        
        v1_parts = normalize(ver1)
        v2_parts = normalize(ver2)
        
        # 比较对应位置的版本部分
        for a, b in zip(v1_parts, v2_parts):
            if isinstance(a, int) and isinstance(b, int):
                # 两个都是整数，直接比较
                if a < b:
                    return -1
                if a > b:
                    return 1
            else:
                # 至少有一个是字符串，转换为字符串比较
                if str(a) < str(b):
                    return -1
                if str(a) > str(b):
                    return 1
        
        # 如果前面的部分都相等，比较长度（长的版本号优先）
        if len(v1_parts) > len(v2_parts):
            return 1
        elif len(v1_parts) < len(v2_parts):
            return -1
        else:
            return 0
    
    def _clone_or_pull_repo(self, repo_url, branch="main"):
        """
        克隆或更新仓库
        
        Args:
            repo_url: 仓库URL
            branch: 分支名称
            
        Returns:
            Path: 仓库本地路径
        """
        repo_name = repo_url.split("/")[-1].replace(".git", "")
        repo_path = self.work_dir / repo_name
        
        try:
            if repo_path.exists():
                # 更新现有仓库
                repo = git.Repo(repo_path)
                origin = repo.remotes.origin
                origin.pull(branch)
                print(f"已更新仓库: {repo_name}")
            else:
                # 克隆新仓库
                git.Repo.clone_from(repo_url, repo_path, branch=branch, depth=1)
                print(f"已克隆仓库: {repo_name}")
            return repo_path
        except Exception as e:
            print(f"处理仓库失败 {repo_url}: {e}")
            return None
    
    def _find_package_dirs(self, repo_path):
        """
        查找仓库中的软件包目录
        
        Args:
            repo_path: 仓库路径
            
        Returns:
            list: 软件包目录列表
        """
        package_dirs = []
        
        for item in repo_path.iterdir():
            if item.is_dir() and not item.name.startswith("."):
                makefile_path = item / "Makefile"
                if makefile_path.exists():
                    package_dirs.append(item)
                else:
                    # 递归查找子目录
                    sub_dirs = self._find_package_dirs(item)
                    package_dirs.extend(sub_dirs)
        
        return package_dirs
    

    

    
    def _sync_single_package(self, repo_name, package_dir):
        """
        同步单个软件包
        
        Args:
            repo_name: 源仓库名称
            package_dir: 软件包目录
        """
        # 解析软件包信息
        makefile_path = package_dir / "Makefile"
        pkg_info = self._parse_makefile(makefile_path)
        pkg_name = pkg_info.get("PKG_NAME") or package_dir.name
        pkg_version = pkg_info.get("PKG_VERSION", "0")
        pkg_release = pkg_info.get("PKG_RELEASE", "0")
        
        # 统一转换为小写，避免大小写冲突
        normalized_pkg_name = pkg_name.lower()
        
        # 检查是否需要更新
        if normalized_pkg_name in self.existing_packages:
            existing = self.existing_packages[normalized_pkg_name]
            if self._compare_versions(pkg_version, existing["version"]) > 0 or \
               (self._compare_versions(pkg_version, existing["version"]) == 0 and \
                self._compare_versions(pkg_release, existing["release"]) > 0):
                # 需要更新
                self._update_package(repo_name, package_dir, normalized_pkg_name, pkg_version, pkg_release)
                self.stats["updated_packages"] += 1
                print(f"更新软件包: {pkg_name} -> {normalized_pkg_name} (来自 {repo_name})，版本 {existing['version']}-{existing['release']} -> {pkg_version}-{pkg_release}")
            else:
                # 跳过，版本相同或更低
                self.stats["skipped_packages"] += 1
                print(f"跳过软件包: {pkg_name} -> {normalized_pkg_name} (来自 {repo_name})，版本相同或更低")
        else:
            # 新软件包
            self._update_package(repo_name, package_dir, normalized_pkg_name, pkg_version, pkg_release)
            self.stats["new_packages"] += 1
            print(f"同步新软件包: {pkg_name} -> {normalized_pkg_name} (来自 {repo_name})，版本 {pkg_version}-{pkg_release}")
    
    def _update_package(self, repo_name, source_dir, pkg_name, pkg_version, pkg_release):
        """
        更新或添加软件包
        
        Args:
            repo_name: 源仓库名称
            source_dir: 源软件包目录
            pkg_name: 软件包名称
            pkg_version: 软件包版本
            pkg_release: 软件包发布版本
        """
        dest_dir = self.output_dir / pkg_name
        
        # 删除所有具有相同小写 PKG_NAME 的目录
        normalized_pkg_name = pkg_name.lower()
        if normalized_pkg_name in self.package_dirs:
            for dir_name in self.package_dirs[normalized_pkg_name]:
                dir_path = self.output_dir / dir_name
                if dir_path.exists() and dir_path != dest_dir:
                    print(f"删除具有相同 PKG_NAME 的目录: {dir_name}")
                    shutil.rmtree(dir_path)
        
        # 删除目标目录（如果存在）
        if dest_dir.exists():
            shutil.rmtree(dest_dir)
        
        # 复制软件包目录，忽略悬空符号链接
        shutil.copytree(source_dir, dest_dir, ignore_dangling_symlinks=True)
        
        # 添加源信息文件
        with open(dest_dir / ".sync_source", "w") as f:
            f.write(f"repo: {repo_name}\n")
            f.write(f"package: {pkg_name}\n")
            f.write(f"version: {pkg_version}\n")
            f.write(f"release: {pkg_release}\n")
        
        # 更新目录映射
        if normalized_pkg_name not in self.package_dirs:
            self.package_dirs[normalized_pkg_name] = []
        # 移除旧的目录名，添加新的目录名
        self.package_dirs[normalized_pkg_name] = [pkg_name]
    
    def run_sync(self, source_repos):
        """
        执行同步操作，实现多源仓库合并
        
        Args:
            source_repos: 源仓库配置，格式：REPO_NAME:URL1,REPO_NAME2:URL2
        """
        print(f"开始同步 OpenWrt 软件包: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 解析源仓库配置
        repos = {}
        for line in source_repos.strip().split("\n"):
            line = line.strip()
            if line and ":" in line:
                repo_name, repo_url = line.split(":", 1)
                repos[repo_name.strip()] = repo_url.strip()
        
        # 收集所有源仓库的软件包信息
        all_packages = []
        
        for repo_name, repo_url in repos.items():
            print(f"\n=== 处理源仓库: {repo_name} ===")
            repo_path = self._clone_or_pull_repo(repo_url)
            if not repo_path:
                continue
            
            # 查找软件包目录
            package_dirs = self._find_package_dirs(repo_path)
            print(f"找到 {len(package_dirs)} 个软件包")
            
            # 收集软件包信息
            for package_dir in package_dirs:
                makefile_path = package_dir / "Makefile"
                pkg_info = self._parse_makefile(makefile_path)
                # 确保pkg_name始终有值，使用目录名作为默认值
                pkg_name = pkg_info.get("PKG_NAME") or package_dir.name
                # 统一转换为小写，避免大小写冲突
                normalized_pkg_name = pkg_name.lower()
                
                all_packages.append({
                    "name": package_dir.name,
                    "pkg_name": pkg_name,
                    "normalized_pkg_name": normalized_pkg_name,
                    "version": pkg_info.get("PKG_VERSION", "0"),
                    "release": pkg_info.get("PKG_RELEASE", "0"),
                    "path": package_dir,
                    "repo_name": repo_name
                })
        
        print(f"\n=== 合并软件包信息 ===")
        print(f"共收集到 {len(all_packages)} 个软件包")
        
        # 合并软件包，保留每个包名的最新版本
        merged_packages = {}
        
        for pkg in all_packages:
            normalized_pkg_name = pkg["normalized_pkg_name"]
            
            # 如果包名不存在，直接添加
            if normalized_pkg_name not in merged_packages:
                merged_packages[normalized_pkg_name] = pkg
            else:
                # 比较版本，保留最新版本
                existing = merged_packages[normalized_pkg_name]
                ver_compare = self._compare_versions(pkg["version"], existing["version"])
                
                if ver_compare > 0:
                    # 当前版本更高，替换
                    merged_packages[normalized_pkg_name] = pkg
                elif ver_compare == 0:
                    # 版本相同，比较release
                    rel_compare = self._compare_versions(pkg["release"], existing["release"])
                    if rel_compare > 0:
                        merged_packages[normalized_pkg_name] = pkg
        
        print(f"合并后得到 {len(merged_packages)} 个唯一软件包")
        
        # 同步合并后的软件包到输出目录
        for pkg in merged_packages.values():
            self._sync_single_package(pkg["repo_name"], pkg["path"])
        
        # 输出统计信息
        self._print_stats()
    
    def _print_stats(self):
        """打印同步统计信息"""
        print("\n=== 同步统计信息 ===")
        print(f"原有软件包: {self.stats['initial_count']}")
        print(f"新增软件包: {self.stats['new_packages']}")
        print(f"更新软件包: {self.stats['updated_packages']}")
        print(f"跳过软件包: {self.stats['skipped_packages']}")
        print(f"最终软件包: {self.stats['initial_count'] + self.stats['new_packages']}")
        print("===================")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="OpenWrt 软件包同步工具")
    parser.add_argument("--work-dir", default="./temp_repos", help="临时工作目录")
    parser.add_argument("--output-dir", default=".", help="输出目录")
    
    args = parser.parse_args()
    
    # 从环境变量获取源仓库配置
    source_repos = os.environ.get("SOURCE_REPOS", "")
    
    # 创建同步器实例并执行同步
    syncer = PackageSyncer(args.work_dir, args.output_dir)
    syncer.run_sync(source_repos)


if __name__ == "__main__":
    main()