#!/usr/bin/env python3
import os
import shutil
import git
import hashlib
import argparse
from pathlib import Path

# 从环境变量读取上游源配置
SOURCE_REPOS = {}
if os.environ.get("SOURCE_REPOS"):
    for line in os.environ["SOURCE_REPOS"].strip().split("\n"):
        line = line.strip()
        if line and not line.startswith("#"):
            if ":" in line:
                repo_name, repo_url = line.split(":", 1)
                SOURCE_REPOS[repo_name.strip()] = {"url": repo_url.strip()}

class PackageSyncer:
    def __init__(self, work_dir, output_dir):
        self.work_dir = Path(work_dir)
        self.output_dir = Path(output_dir)
        self.package_versions = {}
        self.all_packages = []
        
        # 统计变量
        self.stats = {
            "initial_count": 0,
            "new_packages": 0,
            "updated_packages": 0,
            "skipped_packages": 0
        }
        
        self.work_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self._scan_existing_packages()
        self.stats["initial_count"] = self.initial_package_count

    def _scan_existing_packages(self):
        # 扫描仓库中已有的软件包 - 仅输出统计信息
        keep_items = [".git", ".github", ".gitignore", "README.md", "sync_packages.py", "temp_repos"]
        
        for item in self.output_dir.iterdir():
            if item.name in keep_items:
                continue
                
            if item.is_dir():
                makefile_path = item / "Makefile"
                if makefile_path.exists():
                    pkg_info = self._parse_makefile_version(makefile_path)
                    pkg_name = pkg_info["PKG_NAME"] or item.name
                    version = pkg_info["PKG_VERSION"]
                    release = pkg_info["PKG_RELEASE"]
                    
                    # 使用pkg_name作为键存储已有的软件包版本信息
                    self.package_versions[pkg_name] = (version, release)
        
        # 记录初始软件包数量，用于后续统计
        self.initial_package_count = len(self.package_versions)

    def _compare_versions(self, ver1, ver2):
        try:
            def normalize(v):
                v = str(v)
                if "$" in v or "(" in v or ")" in v or "call" in v or "subst" in v:
                    return [v]
                parts = []
                for part in v.split("."):
                    try:
                        parts.append(int(part))
                    except ValueError:
                        parts.append(part)
                return parts
            
            v1 = normalize(ver1)
            v2 = normalize(ver2)
            
            for a, b in zip(v1, v2):
                if isinstance(a, int) and isinstance(b, int):
                    if a > b:
                        return 1
                    elif a < b:
                        return -1
                elif isinstance(a, str) and isinstance(b, str):
                    if a > b:
                        return 1
                    elif a < b:
                        return -1
                else:
                    if str(a) > str(b):
                        return 1
                    elif str(a) < str(b):
                        return -1
            
            if len(v1) > len(v2):
                return 1
            elif len(v1) < len(v2):
                return -1
            else:
                return 0
        except Exception as e:
            # 版本比较失败时不打印详细信息
            return -2

    def _parse_makefile_version(self, makefile_path):
        result = {
            "PKG_NAME": None,
            "PKG_VERSION": "0",
            "PKG_RELEASE": "0"
        }
        
        try:
            with open(makefile_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("PKG_NAME:="):
                        result["PKG_NAME"] = line.split(":=")[1].strip()
                    elif line.startswith("PKG_VERSION:="):
                        result["PKG_VERSION"] = line.split(":=")[1].strip()
                    elif line.startswith("PKG_RELEASE:="):
                        result["PKG_RELEASE"] = line.split(":=")[1].strip()
        except Exception as e:
            # 解析Makefile错误时不打印详细信息
            pass
        
        return result

    def _clone_or_pull_repo(self, repo_name, repo_url, branch=None):
        repo_path = self.work_dir / repo_name
        
        if repo_path.exists():
            # 更新仓库时不打印日志
            repo = git.Repo(repo_path)
            origin = repo.remotes.origin
            if branch:
                origin.pull(branch)
            else:
                origin.pull()
        else:
            # 克隆仓库时不打印日志
            clone_options = {
                "depth": 1,
                "single_branch": True
            }
            if branch:
                clone_options["branch"] = branch
            
            repo = git.Repo.clone_from(repo_url, repo_path, **clone_options)
        
        return repo_path

    def _is_valid_package_dir(self, dir_path):
        dir_path = Path(dir_path)
        return (dir_path / "Makefile").exists()

    def sync_package(self, package_path, repo_name):
        package_name = package_path.name
        makefile_path = package_path / "Makefile"
        
        pkg_info = self._parse_makefile_version(makefile_path)
        pkg_name = pkg_info["PKG_NAME"] or package_name
        version = pkg_info["PKG_VERSION"]
        release = pkg_info["PKG_RELEASE"]
        
        # 收集软件包信息，不直接复制
        self.all_packages.append({
            "name": package_name,
            "pkg_name": pkg_name,
            "version": version,
            "release": release,
            "path": package_path,
            "repo_name": repo_name
        })

    def _find_all_package_dirs(self, root_path):
        package_dirs = []
        
        for item in root_path.iterdir():
            if item.is_dir():
                if item.name.startswith(".") or item.name == "temp" or item.name == "tmp":
                    continue
                    
                if self._is_valid_package_dir(item):
                    package_dirs.append(item)
                else:
                    sub_packages = self._find_all_package_dirs(item)
                    package_dirs.extend(sub_packages)
        
        return package_dirs

    def sync_from_repo(self, repo_name, repo_config):
        repo_path = self._clone_or_pull_repo(
            repo_name, 
            repo_config["url"], 
            repo_config.get("branch")
        )
        
        package_dirs = self._find_all_package_dirs(repo_path)
        
        for package_path in package_dirs:
            self.sync_package(package_path, repo_name)

    def _process_all_packages(self):
        """处理所有收集到的软件包，进行去重和版本比较，然后统一复制"""
        # 不打印收集到的软件包数量，减少冗余日志
        
        # 去重并保留每个包名的最新版本
        best_packages = {}
        
        for pkg in self.all_packages:
            pkg_name = pkg["pkg_name"]
            version = pkg["version"]
            release = pkg["release"]
            
            # 检查是否已存在该包名
            if pkg_name not in best_packages:
                # 如果不存在，直接添加
                best_packages[pkg_name] = pkg
            else:
                # 如果已存在，比较版本
                existing = best_packages[pkg_name]
                existing_version = existing["version"]
                existing_release = existing["release"]
                
                # 比较主版本
                ver_compare = self._compare_versions(version, existing_version)
                
                # 版本比较失败，保留已有的包
                if ver_compare == -2:
                    continue
                
                # 如果当前版本更高，更新
                if ver_compare > 0:
                    best_packages[pkg_name] = pkg
                elif ver_compare == 0:
                    # 主版本相同，比较 release 版本
                    rel_compare = self._compare_versions(release, existing_release)
                    # release 版本比较失败，保留已有的包
                    if rel_compare == -2:
                        continue
                    # 如果当前 release 版本更高，更新
                    if rel_compare > 0:
                        best_packages[pkg_name] = pkg
        
        # 不去重后的软件包数量，减少冗余日志
        
        # 复制最佳版本的软件包到输出目录
        for pkg in best_packages.values():
            package_path = pkg["path"]
            package_name = pkg["name"]
            repo_name = pkg["repo_name"]
            version = pkg["version"]
            release = pkg["release"]
            
            # 检查是否需要更新已存在的包
            update_needed = False
            
            # 使用pkg_name进行对比，确保同一个软件包即使目录名不同也能正确比较
            if pkg_name in self.package_versions:
                existing_version, existing_release = self.package_versions[pkg_name]
                ver_compare = self._compare_versions(version, existing_version)
                
                if ver_compare == -2:
                    print("版本比较失败，跳过软件包: {0} (来自 {1})" .format(package_name, repo_name))
                    self.stats["skipped_packages"] += 1
                    continue
                
                if ver_compare > 0:
                    update_needed = True
                    print("更新软件包: {0} (来自 {1})，版本 {2} -> {3}" .format(package_name, repo_name, existing_version, version))
                    self.stats["updated_packages"] += 1
                elif ver_compare == 0:
                    rel_compare = self._compare_versions(release, existing_release)
                    
                    if rel_compare == -2:
                        print("Release 版本比较失败，跳过软件包: {0} (来自 {1})" .format(package_name, repo_name))
                        self.stats["skipped_packages"] += 1
                        continue
                    
                    if rel_compare > 0:
                        update_needed = True
                        print("更新软件包: {0} (来自 {1})，版本 {2}-{3} -> {4}-{5}" .format(package_name, repo_name, existing_version, existing_release, version, release))
                        self.stats["updated_packages"] += 1
                    else:
                        print("跳过版本更低的软件包: {0} (来自 {1})" .format(package_name, repo_name))
                        self.stats["skipped_packages"] += 1
                        continue
                else:
                    print("跳过版本更低的软件包: {0} (来自 {1})" .format(package_name, repo_name))
                    self.stats["skipped_packages"] += 1
                    continue
            else:
                update_needed = True
                print("同步新软件包: {0} (来自 {1})，版本 {2}-{3}" .format(package_name, repo_name, version, release))
                self.stats["new_packages"] += 1
            
            if update_needed:
                # 复制软件包到输出目录
                dest_path = self.output_dir / package_name
                
                # 如果目标目录已存在，先删除
                if dest_path.exists():
                    shutil.rmtree(dest_path)
                
                # 复制软件包目录
                shutil.copytree(package_path, dest_path)
                
                # 更新版本记录，使用pkg_name作为键
                self.package_versions[pkg_name] = (version, release)
                
                # 添加源仓库信息文件
                with open(dest_path / ".sync_source", "w", encoding="utf-8") as f:
                    f.write("repo: {0}\n" .format(repo_name))
                    f.write("package: {0}\n" .format(package_name))
                    f.write("version: {0}\n" .format(version))
                    f.write("release: {0}\n" .format(release))

    def run_sync(self):
        print("开始同步 OpenWrt 软件包...")
        
        # 第一步：从所有仓库收集软件包信息
        for repo_name, repo_config in SOURCE_REPOS.items():
            try:
                self.sync_from_repo(repo_name, repo_config)
            except Exception as e:
                # 同步仓库出错时不打印详细日志，减少冗余
                pass
        
        # 第二步：统一处理所有收集到的软件包
        self._process_all_packages()
        
        print("同步完成！最终得到 {0} 个软件包" .format(len(self.package_versions)))
        # 打印统计信息
        print("\n=== 同步统计信息 ===")
        print("原有软件包数量: {0}" .format(self.stats["initial_count"]))
        print("新增软件包数量: {0}" .format(self.stats["new_packages"]))
        print("更新软件包数量: {0}" .format(self.stats["updated_packages"]))
        print("跳过软件包数量: {0}" .format(self.stats["skipped_packages"]))
        print("最终软件包数量: {0}" .format(len(self.package_versions)))
        print("==================\n")

def main():
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
    
    syncer = PackageSyncer(args.work_dir, args.output_dir)
    syncer.run_sync()

if __name__ == "__main__":
    main()