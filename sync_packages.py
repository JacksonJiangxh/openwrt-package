#!/usr/bin/env python3
"""
OpenWrt 软件包同步脚本
用于从多个仓库同步 OpenWrt 编译文件夹，并进行去重处理
"""

import os
import shutil
import git
import hashlib
import argparse
from pathlib import Path

# 配置多个源仓库信息
SOURCE_REPOS = {
    "small-package": {
        "url": "https://github.com/kenzok8/small-package.git",
        "branch": "master"
    },
    "helloworld": {
        "url": "https://github.com/fw876/helloworld.git",
        "branch": "master"
    },
    "modem_feeds": {
        "url": "https://github.com/FUjr/modem_feeds.git",
        "branch": "master"
    }
}

class PackageSyncer:
    """OpenWrt 软件包同步器"""
    
    def __init__(self, work_dir, output_dir):
        """
        初始化同步器
        
        Args:
            work_dir: 工作目录，用于临时存储克隆的仓库
            output_dir: 输出目录，用于存储同步后的软件包
        """
        self.work_dir = Path(work_dir)
        self.output_dir = Path(output_dir)
        self.package_hashes = set()  # 用于存储已同步的包的哈希值
        
        # 创建目录
        self.work_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def _calculate_dir_hash(self, dir_path):
        """
        计算目录的哈希值，用于去重
        
        Args:
            dir_path: 目录路径
            
        Returns:
            str: 目录的哈希值
        """
        hasher = hashlib.md5()
        
        try:
            # 遍历目录中的所有文件
            for root, _, files in os.walk(dir_path):
                for file in sorted(files):  # 排序确保顺序一致
                    file_path = os.path.join(root, file)
                    if os.path.isfile(file_path):
                        # 读取文件内容并更新哈希
                        with open(file_path, 'rb') as f:
                            hasher.update(f.read())
        except Exception as e:
            print(f"计算目录 {dir_path} 哈希时出错: {e}")
            return None
        
        return hasher.hexdigest()
    
    def _clone_or_pull_repo(self, repo_name, repo_url, branch):
        """
        克隆或更新仓库
        
        Args:
            repo_name: 仓库名称
            repo_url: 仓库 URL
            branch: 分支名称
            
        Returns:
            Path: 仓库本地路径
        """
        repo_path = self.work_dir / repo_name
        
        if repo_path.exists():
            # 如果仓库已存在，执行 pull 更新
            print(f"更新仓库: {repo_name}")
            repo = git.Repo(repo_path)
            origin = repo.remotes.origin
            origin.pull(branch)
        else:
            # 如果仓库不存在，执行 clone 克隆
            print(f"克隆仓库: {repo_name}")
            repo = git.Repo.clone_from(repo_url, repo_path, branch=branch)
        
        return repo_path
    
    def _is_valid_package_dir(self, dir_path):
        """
        判断是否为有效的 OpenWrt 软件包目录
        
        Args:
            dir_path: 目录路径
            
        Returns:
            bool: 是否为有效的软件包目录
        """
        dir_path = Path(dir_path)
        
        # 检查是否包含 Makefile
        if not (dir_path / "Makefile").exists():
            # 检查是否为 luci 应用目录，luci 应用的 Makefile 通常在根目录或子目录
            if "luci-app-" in dir_path.name:
                # 检查 luci 应用特有的文件结构
                if (dir_path / "luasrc").exists() or (dir_path / "root").exists():
                    return True
            return False
        
        return True
    
    def sync_package(self, package_path, repo_name):
        """
        同步单个软件包
        
        Args:
            package_path: 软件包路径
            repo_name: 源仓库名称
        """
        package_name = package_path.name
        
        # 计算软件包哈希值
        package_hash = self._calculate_dir_hash(package_path)
        if not package_hash:
            return
        
        # 检查是否已存在相同的软件包
        if package_hash in self.package_hashes:
            print(f"跳过已存在的软件包: {package_name} (来自 {repo_name})")
            return
        
        # 添加到已同步列表
        self.package_hashes.add(package_hash)
        
        # 目标路径
        dest_path = self.output_dir / package_name
        
        # 如果目标目录已存在，先删除
        if dest_path.exists():
            shutil.rmtree(dest_path)
        
        # 复制软件包目录
        print(f"同步软件包: {package_name} (来自 {repo_name})")
        shutil.copytree(package_path, dest_path)
        
        # 添加源仓库信息文件
        with open(dest_path / ".sync_source", "w", encoding="utf-8") as f:
            f.write(f"repo: {repo_name}\n")
            f.write(f"package: {package_name}\n")
            f.write(f"hash: {package_hash}\n")
    
    def _find_all_package_dirs(self, root_path):
        """
        递归查找所有有效的软件包目录
        
        Args:
            root_path: 根目录路径
            
        Returns:
            list: 有效的软件包目录列表
        """
        package_dirs = []
        
        for item in root_path.iterdir():
            if item.is_dir():
                # 跳过临时目录和隐藏目录
                if item.name.startswith('.') or item.name == 'temp' or item.name == 'tmp':
                    continue
                    
                # 检查是否为有效的软件包目录
                if self._is_valid_package_dir(item):
                    package_dirs.append(item)
                else:
                    # 递归查找子目录
                    sub_packages = self._find_all_package_dirs(item)
                    package_dirs.extend(sub_packages)
        
        return package_dirs
    
    def sync_from_repo(self, repo_name, repo_config):
        """
        从单个仓库同步软件包
        
        Args:
            repo_name: 仓库名称
            repo_config: 仓库配置
        """
        # 克隆或更新仓库
        repo_path = self._clone_or_pull_repo(repo_name, repo_config["url"], repo_config["branch"])
        
        # 递归查找所有有效的软件包目录
        package_dirs = self._find_all_package_dirs(repo_path)
        
        # 同步找到的所有软件包
        for package_path in package_dirs:
            self.sync_package(package_path, repo_name)
    
    def run_sync(self):
        """
        执行同步操作
        """
        print("开始同步 OpenWrt 软件包...")
        
        # 清空输出目录，保留重要文件和目录
        if self.output_dir.exists():
            # 需要保留的文件和目录列表
            keep_items = ['.git', '.github', '.gitignore', 'README.md', 'sync_packages.py', 'temp_repos']
            
            for item in self.output_dir.iterdir():
                # 跳过需要保留的项目
                if item.name in keep_items:
                    continue
                    
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()
        
        # 遍历所有源仓库
        for repo_name, repo_config in SOURCE_REPOS.items():
            try:
                self.sync_from_repo(repo_name, repo_config)
            except Exception as e:
                print(f"同步仓库 {repo_name} 时出错: {e}")
        
        print(f"同步完成！共同步 {len(self.package_hashes)} 个软件包")
        print(f"同步结果存储在: {self.output_dir}")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="OpenWrt 软件包同步脚本")
    parser.add_argument(
        "--work-dir", 
        default="./temp_repos", 
        help="临时工作目录，用于存储克隆的仓库"
    )
    parser.add_argument(
        "--output-dir", 
        default=".", 
        help="输出目录，用于存储同步后的软件包（默认当前目录）"
    )
    
    args = parser.parse_args()
    
    # 创建同步器实例并执行同步
    syncer = PackageSyncer(args.work_dir, args.output_dir)
    syncer.run_sync()

if __name__ == "__main__":
    main()
