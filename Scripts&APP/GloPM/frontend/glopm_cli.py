#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import sys
import json
import time
import requests
import configparser
from pathlib import Path
from rich.console import Console
from rich.progress import Progress
from rich.panel import Panel
from rich.text import Text
from tabulate import tabulate
from datetime import datetime
import getpass
from concurrent.futures import ThreadPoolExecutor
from rich.prompt import Prompt
from rich.layout import Layout
from rich.console import Console, Group
from rich.text import Text
from rich.table import Table
from rich.box import ROUNDED

console = Console()

# 配置文件路径
CONFIG_DIR = Path.home() / ".glopm"
CONFIG_FILE = CONFIG_DIR / "config.ini"
CACHE_DIR = CONFIG_DIR / "cache"
DEFAULT_API_URL = "https://127.0.0.1:9009/api"

# 应用信息
APP_NAME = "GloPM"
APP_VERSION = "1.0.0"

def print_welcome():
    """打印欢迎信息"""
    welcome_text = Text()
    welcome_text.append(f"\n欢迎使用 {APP_NAME} ", style="bold green")
    welcome_text.append(f"v{APP_VERSION}\n", style="blue")

    panel = Panel(welcome_text, title="欢迎", border_style="green")
    console.print(panel)

def ensure_path_exists(path):
    """确保路径存在"""
    if isinstance(path, str):
        path = Path(path)
    
    if not path.exists():
        if path.suffix:  # 如果有后缀，说明是文件
            path.parent.mkdir(parents=True, exist_ok=True)
        else:  # 否则是目录
            path.mkdir(parents=True, exist_ok=True)
        return False
    return True

def check_file_exists(file_path, error_message=None):
    """检查文件是否存在，不存在则打印错误信息并返回False"""
    if not os.path.exists(file_path):
        if error_message:
            print_error(error_message)
        return False
    return True

def load_config():
    """加载配置文件"""
    config = configparser.ConfigParser()
    ensure_path_exists(CONFIG_DIR)
    
    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE)
    
    # 确保所有必要的配置节都存在
    sections = ['auth', 'settings', 'user_info']
    for section in sections:
        if section not in config:
            config[section] = {}
    
    # 设置默认值
    if 'api_url' not in config['settings']:
        config['settings']['api_url'] = DEFAULT_API_URL
    
    return config

def save_config(config):
    """保存配置文件"""
    ensure_path_exists(CONFIG_DIR)
    with open(CONFIG_FILE, 'w') as f:
        config.write(f)

def get_auth_headers():
    """获取认证头信息"""
    config = load_config()
    if 'user_id' not in config['auth'] or 'api_key' not in config['auth']:
        console.print(Panel(
            "您尚未登录，请先使用 login 命令登录。",
            title="需要登录",
            border_style="red"
        ))
        sys.exit(1)
    
    return {
        'x-user-id': config['auth']['user_id'],
        'x-api-key': config['auth']['api_key']
    }

def get_api_url():
    """获取API URL"""
    config = load_config()
    return config['settings']['api_url']

def format_date(date_str):
    """格式化日期字符串"""
    try:
        dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except:
        return date_str

def print_success(message):
    """打印成功信息"""
    console.print(Panel(
        message,
        title="操作成功",
        border_style="green"
    ))

def print_error(message):
    """打印错误信息"""
    console.print(Panel(
        message,
        title="操作失败",
        border_style="red"
    ))

def print_info(message, title="信息"):
    """打印一般信息"""
    console.print(Panel(
        message,
        title=title,
        border_style="blue"
    ))

def handle_response(response, success_handler, error_handler=None):
    """统一处理API响应"""
    if 200 <= response.status_code < 300:
        return success_handler(response)
    else:
        error = response.json().get('error', '未知错误')
        if error_handler:
            return error_handler(error)
        else:
            print_error(f"请求失败：{error}")
            return None

def api_request(method, endpoint, data=None, files=None, headers=None, stream=False, status_message=None):
    """统一的API请求处理函数"""
    api_url = get_api_url()
    url = f"{api_url}/{endpoint}"
    
    try:
        with console.status(status_message or f"[bold green]正在处理请求...[/bold green]"):
            if method.lower() == 'get':
                response = requests.get(url, headers=headers, params=data, stream=stream)
            elif method.lower() == 'post':
                response = requests.post(url, headers=headers, json=data if files is None else None, 
                                        data=None if files is None else data, files=files)
            elif method.lower() == 'put':
                response = requests.put(url, headers=headers, json=data if files is None else None, 
                                        data=None if files is None else data, files=files)
            elif method.lower() == 'delete':
                response = requests.delete(url, headers=headers)
            else:
                raise ValueError(f"不支持的请求方法: {method}")
        
        return response
    except requests.RequestException as e:
        print_error(f"网络请求错误：{str(e)}。\n请检查您的网络连接后重试。")
        sys.exit(1)

def save_auth_info(user_id, api_key, username):
    """保存认证信息到配置文件"""
    config = load_config()
    config['auth']['user_id'] = str(user_id)
    config['auth']['api_key'] = api_key
    config['user_info']['username'] = username
    save_config(config)

def clear_auth_info():
    """清除认证信息"""
    config = load_config()
    username = config['user_info'].get('username', '用户')
    config['auth'] = {}
    config['user_info'] = {}
    save_config(config)
    return username

def confirm_action(message, confirm_value=None):
    """确认操作"""
    console.print(Panel(
        Text(message, style="bold yellow"),
        title="需要确认",
        border_style="yellow"
    ))
    
    if confirm_value:
        return Prompt.ask(f"请输入 '{confirm_value}' 以确认") == confirm_value
    else:
        return ask_continue("确认操作？")

def download_file(url, output_path=None, headers=None, progress_callback=None):
    """
    通用文件下载函数
    
    参数:
        url: 下载URL
        output_path: 输出文件路径，如果为None则从响应头获取
        headers: 请求头
        progress_callback: 进度回调函数，接收已下载大小和总大小两个参数
    
    返回:
        (bool, str): (是否成功, 文件路径或错误信息)
    """
    response = api_request(
        'get',
        url,
        headers=headers,
        stream=True,
        status_message="[bold green]正在准备下载...[/bold green]"
    )
    
    def success_handler(resp):
        try:
            # 获取文件名
            if not output_path:
                content_disposition = resp.headers.get('content-disposition', '')
                if 'filename=' in content_disposition:
                    filename = content_disposition.split('filename=')[1].strip('"\'')
                else:
                    filename = f"download_{int(datetime.now().timestamp())}"
                output_file = filename
            else:
                output_file = output_path
            
            # 确保输出目录存在
            ensure_path_exists(os.path.dirname(output_file) or '.')
            
            # 获取文件大小
            total_size = int(resp.headers.get('content-length', 0))
            
            # 下载文件
            with open(output_file, 'wb') as f:
                downloaded = 0
                for chunk in resp.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if progress_callback:
                            progress_callback(downloaded, total_size)
            
            return True, output_file
            
        except Exception as e:
            if os.path.exists(output_file):
                try:
                    os.remove(output_file)  # 清理未完成的文件
                except:
                    pass
            return False, str(e)
    
    def error_handler(error):
        return False, f"下载失败：{error}"
    
    return handle_response(response, success_handler, error_handler)

def get_cached_package_info(package_name, max_age=3600):
    """获取缓存的包信息，如果缓存过期则返回None"""
    ensure_path_exists(CACHE_DIR)
    cache_file = CACHE_DIR / f"{package_name}.json"
    if os.path.exists(cache_file):
        # 检查缓存是否过期
        if time.time() - os.path.getmtime(cache_file) < max_age:
            try:
                with open(cache_file, 'r') as f:
                    return json.load(f)
            except:
                pass
    return None

def cache_package_info(package_name, info):
    """缓存包信息"""
    ensure_path_exists(CACHE_DIR)
    cache_file = CACHE_DIR / f"{package_name}.json"
    try:
        with open(cache_file, 'w') as f:
            json.dump(info, f)
    except:
        # 忽略缓存错误
        pass

def batch_operation(items, operation_func, parallel=False, max_workers=4):
    """批量执行操作，支持并行处理"""
    results = []
    
    if parallel and len(items) > 1:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(operation_func, item) for item in items]
            for future in futures:
                results.append(future.result())
    else:
        for item in items:
            results.append(operation_func(item))
    
    return results

def interactive_login():
    """交互式登录"""
    username = input("用户名: ")
    password = getpass.getpass("密码: ")
    
    response = api_request(
        'post', 
        'auth/login', 
        data={
            'username': username,
            'password': password
        },
        status_message="[bold green]正在登录，请稍候...[/bold green]"
    )
    
    def success_handler(resp):
        result = resp.json()
        config = load_config()
        config['auth']['user_id'] = result['user_id']
        config['auth']['api_key'] = result['api_key']
        config['user_info']['username'] = username
        save_config(config)
        print_success(f"欢迎回来，{username}！\n您已成功登录。")
        return True
    
    def error_handler(error):
        print_error(f"登录失败：{error}。\n请检查用户名和密码是否正确。")
        return False
    
    return handle_response(response, success_handler, error_handler)

def interactive_register():
    """交互式注册"""
    username = input("请设置用户名: ")
    password = getpass.getpass("请设置密码: ")
    confirm_password = getpass.getpass("请确认密码: ")
    
    if password != confirm_password:
        print_error("两次输入的密码不一致，请重新注册。")
        return False
    
    response = api_request(
        'post', 
        'auth/register', 
        data={
            'username': username,
            'password': password
        },
        status_message="[bold green]正在注册，请稍候...[/bold green]"
    )
    
    def success_handler(resp):
        result = resp.json()
        config = load_config()
        config['auth']['user_id'] = result['user_id']
        config['auth']['api_key'] = result['api_key']
        config['user_info']['username'] = username
        save_config(config)
        print_success(f"恭喜您，{username}！\n您已成功注册并登录。")
        return True
    
    def error_handler(error):
        print_error(f"注册失败：{error}。\n请尝试使用其他用户名。")
        return False
    
    return handle_response(response, success_handler, error_handler)

def register(args):
    """注册新用户"""
    if not args.username or not args.password:
        return interactive_register()
    
    response = api_request(
        'post', 
        'auth/register', 
        data={'username': args.username, 'password': args.password},
        status_message="[bold green]正在为您注册账户，请稍候...[/bold green]"
    )
    
    def success_handler(resp):
        result = resp.json()
        save_auth_info(result['user_id'], result['api_key'], args.username)
        print_success(f"尊敬的 {args.username}，欢迎您使用 {APP_NAME}！\n\n"
                     f"• 您的账户已成功创建。\n"
                     f"• 已为您自动登录。\n"
                     f"• 您现在可以开始发布和下载包了。")
        return True
    
    def error_handler(error):
        print_error(f"很抱歉，注册过程中遇到了问题：{error}。\n请稍后再试或联系管理员获取帮助。")
        return False
    
    return handle_response(response, success_handler, error_handler)

def login(args):
    """用户登录"""
    if not args.username or not args.password:
        return interactive_login()
    
    response = api_request(
        'post', 
        'auth/login', 
        data={'username': args.username, 'password': args.password},
        status_message="[bold green]正在验证您的身份，请稍候...[/bold green]"
    )
    
    def success_handler(resp):
        result = resp.json()
        save_auth_info(result['user_id'], result['api_key'], args.username)
        print_success(f"欢迎回来，{args.username}！\n\n您已成功登录。")
        return True
    
    def error_handler(error):
        print_error(f"登录失败：{error}。\n请检查您的用户名和密码是否正确。")
        return False
    
    return handle_response(response, success_handler, error_handler)

def logout(args):
    """退出登录"""
    username = clear_auth_info()
    print_success(f"再见，{username}！您已退出。\n期待您的再次使用。")

def interactive_publish():
    """交互式发布包"""
    headers = get_auth_headers()
    
    # 收集输入
    name = input("包名: ")
    version = input("版本号: ")
    description = input("包描述: ")
    file_path = input("文件路径: ")
    
    # 检查文件是否存在
    if not check_file_exists(file_path, "指定的文件不存在，请检查路径。"):
        return False
    
    # 确认发布
    if not confirm_action(f"您即将发布包 {name}@{version}，确认继续？"):
        print_info("已取消发布操作。", title="操作取消")
        return False
    
    # 准备文件
    files = {'file': open(file_path, 'rb')}
    data = {
        'packageName': name,
        'version': version,
        'description': description
    }
    
    response = api_request(
        'put', 
        'packages/publish', 
        data=data, 
        files=files,
        headers=headers,
        status_message=f"[bold green]正在发布包 {name}@{version}，请稍候...[/bold green]"
    )
    
    def success_handler(resp):
        result = resp.json()
        print_success(f"包 {name}@{version} 发布成功！\n\n"
                     f"• 包名：{name}\n"
                     f"• 版本：{version}\n"
                     f"• 描述：{description}\n"
                     f"• 文件：{os.path.basename(file_path)}")
        return True
    
    def error_handler(error):
        print_error(f"发布失败：{error}。\n请检查包名和版本是否已存在。")
        return False
    
    return handle_response(response, success_handler, error_handler)

def publish(args):
    """发布包"""
    if not args.name or not args.version or not args.description or not args.file:
        return interactive_publish()
    
    headers = get_auth_headers()
    
    # 检查文件是否存在
    if not check_file_exists(args.file, f"文件 {args.file} 不存在。\n请检查文件路径是否正确。"):
        return False
    
    # 准备表单数据
    files = {
        'file': (os.path.basename(args.file), open(args.file, 'rb'), 'application/octet-stream')
    }
    data = {
        'packageName': args.name,
        'version': args.version,
        'description': args.description
    }
    
    response = api_request(
        'put',
        'packages/publish',
        headers=headers,
        data=data,
        files=files,
        status_message=f"[bold green]正在发布 {args.name}@{args.version}，请稍候...[/bold green]"
    )
    
    def success_handler(resp):
        # 清除缓存
        cache_file = CACHE_DIR / f"{args.name}.json"
        if os.path.exists(cache_file):
            os.remove(cache_file)
            
        print_success(f"包 {args.name}@{args.version} 发布成功！\n\n"
                     f"• 包名：{args.name}\n"
                     f"• 版本：{args.version}\n"
                     f"• 描述：{args.description}")
        return True
    
    def error_handler(error):
        print_error(f"发布失败：{error}。\n请检查包名和版本是否符合规范。")
        return False
    
    return handle_response(response, success_handler, error_handler)

def download(args):
    """下载包"""
    pkg_spec = args.package
    
    # 解析包规格
    # 格式: 包名[@版本][:输出文件名]
    output_file = None
    version = 'latest'
    
    # 首先检查是否包含输出文件名
    if ":" in pkg_spec:
        pkg_part, output_file = pkg_spec.split(":", 1)
    else:
        pkg_part = pkg_spec
    
    # 然后检查是否包含版本号
    if "@" in pkg_part:
        package_name, version = pkg_part.split("@", 1)
    else:
        package_name = pkg_part
    
    # 如果版本未指定，获取最新版本
    if version.lower() == 'latest':
        success, version_info = get_package_latest_version(package_name)
        if success and 'version' in version_info:
            version = version_info['version']
            console.print(f"[blue]获取到 {package_name} 的最新版本: {version}[/blue]")
        else:
            error_msg = version_info if not success else "未找到版本信息"
            print_error(f"获取最新版本失败: {error_msg}")
            return False
    
    with Progress() as progress:
        task = progress.add_task(f"[green]下载 {package_name}@{version}...", total=100)
        
        def update_progress(downloaded, total):
            if total > 0:
                progress.update(task, completed=int(downloaded * 100 / total))
        
        success, result = download_file(
            f"packages/{package_name}/download/{version}",
            output_file,
            headers=get_auth_headers(),
            progress_callback=update_progress
        )
        
        if success:
            file_size_kb = os.path.getsize(result) / 1024
            print_success(f"包 {package_name}@{version} 下载成功！\n\n"
                         f"• 包名：{package_name}\n"
                         f"• 版本：{version}\n"
                         f"• 保存位置：{result}\n"
                         f"• 文件大小：{file_size_kb:.2f} KB")
            return True
        else:
            print_error(f"下载失败：{result}")
            return False

def search(args):
    """搜索包"""
    response = api_request(
        'get',
        f"packages/search?query={args.query}",
        status_message=f"[bold green]正在搜索\"{args.query}\"相关的包，请稍候...[/bold green]"
    )
    
    def success_handler(resp):
        packages = resp.json()
        
        if not packages:
            print_info(f"很抱歉，未找到与\"{args.query}\"相关的包。\n请尝试使用其他关键词搜索。", title="搜索结果")
            return True
        
        # 使用 tabulate 格式化表格
        headers = ["包名", "描述", "更新时间"]
        table_data = []
        for pkg in packages:
            table_data.append([
                pkg.get('name', 'N/A'),
                pkg.get('description', 'N/A'),
                format_date(pkg.get('updatedAt', 'N/A'))
            ])
        
        table = tabulate(
            table_data,
            headers=headers,
            tablefmt="fancy_grid",
            numalign="right"
        )
        
        print_info(f"找到 {len(packages)} 个与\"{args.query}\"相关的包：\n\n{table}", title="搜索结果")
        return True
    
    def error_handler(error):
        print_error(f"搜索失败：{error}。\n请稍后再试。")
        return False
    
    return handle_response(response, success_handler, error_handler)

def get_package_latest_version(package_name, use_cache=True):
    """
    获取包的最新版本信息
    
    参数:
        package_name: 包名
        use_cache: 是否使用缓存
    
    返回:
        (bool, dict|str): (是否成功, 版本信息或错误消息)
    """
    # 检查缓存
    if use_cache:
        cached_info = get_cached_package_info(package_name)
        if cached_info and 'latest_version' in cached_info:
            return True, cached_info['latest_version']
    
    # 从服务器获取
    response = api_request(
        'get',
        f"packages/{package_name}/latestVersion",
        status_message=f"[bold green]正在获取 {package_name} 的最新版本信息...[/bold green]"
    )
    
    if response.status_code == 200:
        version_info = response.json()
        
        # 更新缓存
        if use_cache:
            cached_info = get_cached_package_info(package_name) or {}
            cached_info['latest_version'] = version_info
            cache_package_info(package_name, cached_info)
        
        return True, version_info
    else:
        try:
            error = response.json().get('error', '未知错误')
        except:
            error = f"状态码: {response.status_code}"
        return False, error

def get_package_versions(package_name, use_cache=True):
    """
    获取包的所有版本信息
    
    参数:
        package_name: 包名
        use_cache: 是否使用缓存
    
    返回:
        (bool, list|str): (是否成功, 版本列表或错误消息)
    """
    # 检查缓存
    if use_cache:
        cached_info = get_cached_package_info(package_name)
        if cached_info and 'versions' in cached_info:
            return True, cached_info['versions']
    
    # 从服务器获取
    response = api_request(
        'get',
        f"packages/{package_name}/versions",
        status_message=f"[bold green]正在获取 {package_name} 的版本列表，请稍候...[/bold green]"
    )
    
    if response.status_code == 200:
        versions = response.json()
        
        # 更新缓存
        if use_cache:
            cached_info = get_cached_package_info(package_name) or {}
            cached_info['versions'] = versions
            cache_package_info(package_name, cached_info)
        
        return True, versions
    else:
        try:
            error = response.json().get('error', '未知错误')
        except:
            error = f"状态码: {response.status_code}"
        return False, error

def batch_download(args):
    """批量下载包"""
    if not args.packages:
        print_error("请指定要下载的包列表。")
        return False
    
    packages = []
    for pkg_spec in args.packages:
        # 检查是否包含输出文件名规范
        if ":" in pkg_spec:
            pkg_part, output_file = pkg_spec.split(":", 1)
        else:
            pkg_part, output_file = pkg_spec, None
        
        # 解析包名和版本
        parts = pkg_part.split('@')
        if len(parts) == 2:
            packages.append({'name': parts[0], 'version': parts[1], 'output': output_file})
        else:
            # 如果没有指定版本，获取最新版本
            success, version_info = get_package_latest_version(parts[0])
            
            if success:
                if 'version' in version_info:
                    packages.append({'name': parts[0], 'version': version_info['version'], 'output': output_file})
                else:
                    print_error(f"包 {parts[0]} 暂无版本，跳过下载。")
            else:
                print_error(f"获取包 {parts[0]} 的版本信息失败: {version_info}，跳过下载。")
    
    if not packages:
        print_error("没有有效的包可下载。")
        return False
    
    print_info(f"准备下载 {len(packages)} 个包...", title="批量下载")
    
    def download_single(pkg):
        pkg_name = pkg['name']
        pkg_version = pkg['version']
        
        # 确定输出文件名
        filename = pkg['output']  # 可能为None，由download_file处理
        
        # 设置进度条
        with Progress() as progress:
            task = progress.add_task(f"[green]下载 {pkg_name}@{pkg_version}...", total=100)
            
            def update_progress(downloaded, total):
                if total > 0:
                    progress.update(task, completed=int(downloaded * 100 / total))
            
            url = f"packages/{pkg_name}/download/{pkg_version}"
            success, result = download_file(
                url, 
                filename, 
                progress_callback=update_progress
            )
        
        if success:
            file_size_kb = os.path.getsize(result) / 1024
            print_success(f"包 {pkg_name}@{pkg_version} 下载成功！\n\n"
                         f"• 包名：{pkg_name}\n"
                         f"• 版本：{pkg_version}\n"
                         f"• 保存位置：{result}\n"
                         f"• 文件大小：{file_size_kb:.2f} KB")
            return True
        else:
            print_error(f"下载失败：{result}。\n请检查包名和版本是否正确或网络连接。")
            return False
    
    results = batch_operation(packages, download_single, parallel=args.parallel, max_workers=args.workers)
    
    success_count = sum(1 for r in results if r)
    print_info(f"批量下载完成: {success_count}/{len(packages)} 个包下载成功。", title="下载结果")
    return success_count == len(packages)

def delete_package(args):
    """删除包"""
    headers = get_auth_headers()
    
    # 确认删除
    if not args.force and not confirm_action(f"警告：您即将删除包 {args.name}，此操作不可逆！"):
        print_info("已取消删除操作。", title="操作取消")
        return
    
    response = api_request(
        'delete',
        f"packages/{args.name}",
        headers=headers,
        status_message=f"[bold green]正在删除包 {args.name}，请稍候...[/bold green]"
    )
    
    def success_handler(resp):
        print_success(f"包 {args.name} 已成功删除。\n该包的所有版本和相关文件已被永久移除。")
        return True
    
    def error_handler(error):
        print_error(f"删除失败：{error}。\n请检查包名是否正确或确认您有权限删除此包。")
        return False
    
    return handle_response(response, success_handler, error_handler)

def batch_delete_packages(args):
    """批量删除包"""
    headers = get_auth_headers()
    
    if not args.packages:
        print_error("请指定要删除的包列表。")
        return False
    
    # 确认删除
    if not args.force:
        package_list = ", ".join(args.packages)
        if not confirm_action(f"警告：您即将删除以下包：{package_list}，此操作不可逆！"):
            print_info("已取消删除操作。", title="操作取消")
            return False
    
    print_info(f"准备删除 {len(args.packages)} 个包...", title="批量删除")
    
    def delete_single(pkg_name):
        console.print(f"[bold green]正在删除包 {pkg_name}...[/bold green]")
        
        response = api_request(
            'delete',
            f"packages/{pkg_name}",
            headers=headers
        )
        
        def success_handler(resp):
            console.print(f"[green]✓ {pkg_name} 删除成功[/green]")
            return True
        
        def error_handler(error):
            try:
                error = response.json().get('error', '未知错误')
            except:
                error = f"状态码: {response.status_code}"
            console.print(f"[red]✗ {pkg_name} 删除失败: {error}[/red]")
            return False
        
        return handle_response(response, success_handler, error_handler)

    results = batch_operation(args.packages, delete_single, parallel=args.parallel, max_workers=args.workers)
    
    success_count = sum(1 for r in results if r)
    print_info(f"批量删除完成: {success_count}/{len(args.packages)} 个包删除成功。", title="删除结果")
    return success_count == len(args.packages)

def config_cmd(args):
    """配置管理"""
    config = load_config()
    if not args.show and not args.get and not args.set and not args.delete:
        print_error("请指定要执行的操作。")
        return False
    
    if args.show:
        table = Table(title="当前配置", box=ROUNDED)
        table.add_column("配置项", style="cyan")
        table.add_column("值", style="green")
        
        for section in config.sections():
            for key, value in config[section].items():
                if key == 'api_key':
                    value = '******'
                table.add_row(f"{section}.{key}", value)
        
        console.print(table)
        return True
    
    elif args.get:
        section, key = args.get.split('.', 1) if '.' in args.get else ('settings', args.get)
        if section in config and key in config[section]:
            value = config[section][key]
            print_info(f"配置项 {section}.{key} 的值为：{value}")
        else:
            print_error(f"配置项 {args.get} 不存在")
        return True
    
    elif args.set:
        key, value = args.set.split('=', 1)
        section, key = key.split('.', 1) if '.' in key else ('settings', key)
        
        if section not in config:
            config[section] = {}
        
        config[section][key] = value
        save_config(config)
        print_success(f"配置项 {section}.{key} 已更新为：{value}")
        return True
    
    elif args.delete:
        section, key = args.delete.split('.', 1) if '.' in args.delete else ('settings', args.delete)
        if section in config and key in config[section]:
            del config[section][key]
            save_config(config)
            print_success(f"配置项 {section}.{key} 已删除")
        else:
            print_error(f"配置项 {args.delete} 不存在")
        return True

def clear_cache(args):
    """清除缓存"""
    if os.path.exists(CACHE_DIR):
        cache_files = list(CACHE_DIR.glob('*.json'))
        if not cache_files:
            print_info("缓存目录为空，无需清理。")
            return True
            
        if not args.force and not confirm_action(f"确定要清除 {len(cache_files)} 个缓存文件吗？"):
            print_info("已取消清除缓存操作。", title="操作取消")
            return True
            
        for f in cache_files:
            os.remove(f)
        print_success(f"已清除 {len(cache_files)} 个缓存文件。")
    else:
        print_info("缓存目录不存在，无需清理。")
    return True

def delete_account(args):
    """删除用户账户"""
    headers = get_auth_headers()
    config = load_config()
    username = config['user_info'].get('username', '用户')
    
    # 创建布局
    layout = Layout()
    layout.split_column(
        Layout(name="warning"),
        Layout(name="info")
    )
    
    # 添加警告内容
    layout["warning"].update(Panel(
        Text("您即将删除您的账户，此操作不可逆！\n所有您发布的包将无法再被管理。", style="bold red"),
        title="⚠️ 警告",
        border_style="red"
    ))
    
    # 添加账户信息
    layout["info"].update(Panel(
        Group(
            Text(f"用户名: {username}", style="blue"),
            Text(f"用户ID: {config['auth'].get('user_id', 'N/A')}", style="blue")
        ),
        title="账户信息",
        border_style="blue"
    ))
    
    # 显示布局
    if not args.force:
        console.print(layout)
        confirm = Prompt.ask("请输入您的用户名以确认删除账户")
        
        if confirm != username:
            print_info("用户名不匹配，已取消删除操作。", title="操作取消")
            return
    
    response = api_request(
        'delete',
        'auth/',
        headers=headers,
        status_message="[bold green]正在删除您的账户，请稍候...[/bold green]"
    )
    
    def success_handler(resp):
        # 清除本地配置
        clear_auth_info()
        print_success(f"尊敬的 {username}，您的账户已成功删除。\n感谢您曾经使用我们的服务。")
        return True
    
    def error_handler(error):
        print_error(f"删除账户失败：{error}。\n请稍后再试或联系管理员获取帮助。")
        return False
    
    return handle_response(response, success_handler, error_handler)

def get_latest_version(args):
    """获取包的最新版本"""
    success, result = get_package_latest_version(args.name)
    
    if success:
        if not result:
            print_info(f"包 {args.name} 暂无版本记录。", title="版本信息")
            return True
        
        version = result.get('version', 'N/A')
        description = result.get('description', 'N/A')
        file_size = result.get('fileSize', 0) / 1024
        published_at = format_date(result.get('publishedAt', 'N/A'))
        downloads = result.get('downloads', 0)
        
        print_info(f"包 {args.name} 的最新版本信息：\n\n"
                  f"• 版本：{version}\n"
                  f"• 描述：{description}\n"
                  f"• 文件大小：{file_size:.2f} KB\n"
                  f"• 发布时间：{published_at}\n"
                  f"• 下载量：{downloads}", title="版本信息")
        return True
    else:
        print_error(f"获取失败：{result}。\n请检查包名是否正确。")
        return False

def list_versions(args):
    """列出包的所有版本"""
    success, versions = get_package_versions(args.name)
    
    if success:
        if not versions:
            print_info(f"包 {args.name} 暂无版本记录。", title="版本列表")
            return True
        
        # 使用 tabulate 格式化表格
        headers = ["版本", "描述", "文件大小", "发布时间", "下载量"]
        table_data = []
        
        for ver in versions:
            table_data.append([
                ver.get('version', 'N/A'),
                ver.get('description', 'N/A'),
                f"{ver.get('fileSize', 0) / 1024:.2f} KB",
                format_date(ver.get('publishedAt', 'N/A')),
                ver.get('downloads', 0)
            ])
        
        table = tabulate(
            table_data,
            headers=headers,
            tablefmt="fancy_grid",
            numalign="right"
        )
        
        print_info(f"包 {args.name} 共有 {len(versions)} 个版本：\n\n{table}", title="版本列表")
        return True
    else:
        print_error(f"获取失败：{versions}。\n请检查包名是否正确。")
        return False

def ask_continue(message="是否继续？", default=True):
    """
    询问用户是否继续
    
    参数:
        message: 提示消息
        default: 默认选择，True 表示默认继续，False 表示默认取消
    
    返回:
        bool: 用户是否选择继续
    """
    # 尝试使用交互式版本
    try:
        return ask_continue_interactive(message, default)
    except Exception:
        # 如果交互式版本失败，回退到简单版本
        default_str = "Y/n" if default else "y/N"
        
        console.print(f"[yellow]{message} [{default_str}][/yellow]")
        
        try:
            response = input().strip().lower()
            if not response:
                return default
            return response in ['y', 'yes', '是', '确定', '继续']
        except KeyboardInterrupt:
            console.print("\n[bold yellow]操作已取消。[/bold yellow]")
            return False

def ask_continue_interactive(message="是否继续？", default=True):
    """
    交互式询问用户是否继续，支持键盘左右键选择
    
    参数:
        message: 提示消息
        default: 默认选择，True 表示默认继续，False 表示默认取消
    
    返回:
        bool: 用户是否选择继续
    """
    try:
        import readchar
    except ImportError:
        # 如果没有安装 readchar，回退到简单版本
        return ask_continue(message, default)
    
    options = ["是", "否"]
    selected = 0 if default else 1
    
    # ANSI 转义序列
    CLEAR_LINE = '\r\033[K'         # 清除当前行
    BOLD = '\033[1m'                # 加粗
    GREEN = '\033[32m'              # 绿色
    YELLOW = '\033[33m'             # 黄色
    DIM = '\033[2m'                 # 暗淡
    RESET = '\033[0m'               # 重置所有属性
    
    def render_options():
        option_text = ""
        for i, option in enumerate(options):
            if i == selected:
                option_text += f"{BOLD}{GREEN}[{option}]{RESET}"
            else:
                option_text += f"{DIM}[{option}]{RESET}"
            if i < len(options) - 1:
                option_text += " / "
        return option_text
    
    # 首次打印提示
    print(f"{YELLOW}{message}{RESET} {render_options()}", end="", flush=True)
    
    while True:
        # 获取按键
        key = readchar.readkey()
        
        # 处理按键
        if key == readchar.key.LEFT and selected > 0:
            selected -= 1
            # 清除当前行并重新打印
            print(f"{CLEAR_LINE}{YELLOW}{message}{RESET} {render_options()}", end="", flush=True)
        elif key == readchar.key.RIGHT and selected < len(options) - 1:
            selected += 1
            # 清除当前行并重新打印
            print(f"{CLEAR_LINE}{YELLOW}{message}{RESET} {render_options()}", end="", flush=True)
        elif key == readchar.key.ENTER:
            print()  # 换行
            return selected == 0
        elif key == "\x03":  # Ctrl+C
            print(f"\n{YELLOW}操作已取消。{RESET}")
            return False

def delete_version(args):
    """删除包的特定版本"""
    headers = get_auth_headers()
    
    # 确认删除
    if not args.force and not confirm_action(f"警告：您即将删除包 {args.name} 的版本 {args.version}，此操作不可逆！"):
        print_info("已取消删除操作。", title="操作取消")
        return False
    
    response = api_request(
        'delete',
        f"packages/{args.name}/versions/{args.version}",
        headers=headers,
        status_message=f"[bold green]正在删除包 {args.name} 的版本 {args.version}，请稍候...[/bold green]"
    )
    
    def success_handler(resp):
        print_success(f"包 {args.name} 的版本 {args.version} 已成功删除。")
        return True
    
    def error_handler(error):
        print_error(f"删除失败：{error}。\n请检查包名和版本是否正确或确认您有权限删除此版本。")
        return False
    
    return handle_response(response, success_handler, error_handler)

def main():
    parser = argparse.ArgumentParser(description=f"{APP_NAME} 命令行工具 v{APP_VERSION}")
    subparsers = parser.add_subparsers(dest="command", help="子命令")
    
    # 注册命令
    register_parser = subparsers.add_parser("register", help="注册新用户")
    register_parser.add_argument("-u", "--username", help="用户名")
    register_parser.add_argument("-p", "--password", help="密码")
    register_parser.set_defaults(func=register)
    
    # 登录命令
    login_parser = subparsers.add_parser("login", help="用户登录")
    login_parser.add_argument("-u", "--username", help="用户名")
    login_parser.add_argument("-p", "--password", help="密码")
    login_parser.set_defaults(func=login)
    
    # 退出登录命令
    logout_parser = subparsers.add_parser("logout", help="退出登录")
    logout_parser.set_defaults(func=logout)
    
    # 发布包命令
    publish_parser = subparsers.add_parser("publish", help="发布包")
    publish_parser.add_argument("-n", "--name", help="包名")
    publish_parser.add_argument("-v", "--version", help="版本号")
    publish_parser.add_argument("-d", "--description", help="包描述")
    publish_parser.add_argument("-f", "--file", help="包文件路径")
    publish_parser.set_defaults(func=publish)
    
    # 下载包命令
    download_parser = subparsers.add_parser("download", help="下载包")
    download_parser.add_argument("package", help="包规格，格式: 包名[@版本][:输出文件名]")
    download_parser.set_defaults(func=download)
    
    # 批量下载命令
    batch_download_parser = subparsers.add_parser("batch-download", help="批量下载包")
    batch_download_parser.add_argument("packages", nargs="+", help="包规格列表，格式: 包名[@版本][:输出文件名]")
    batch_download_parser.add_argument("-p", "--parallel", action="store_true", help="并行下载")
    batch_download_parser.add_argument("-w", "--workers", type=int, default=4, help="并行下载的工作线程数")
    batch_download_parser.set_defaults(func=batch_download)
    
    # 搜索包命令
    search_parser = subparsers.add_parser("search", help="搜索包")
    search_parser.add_argument("query", help="搜索关键词")
    search_parser.set_defaults(func=search)
    
    # 获取最新版本命令
    version_parser = subparsers.add_parser("version", help="获取包的最新版本")
    version_parser.add_argument("name", help="包名")
    version_parser.set_defaults(func=get_latest_version)
    
    # 列出所有版本命令
    list_parser = subparsers.add_parser("list", help="列出包的所有版本")
    list_parser.add_argument("name", help="包名")
    list_parser.set_defaults(func=list_versions)
    
    # 删除包命令
    delete_parser = subparsers.add_parser("delete", help="删除包")
    delete_parser.add_argument("name", help="包名")
    delete_parser.add_argument("-f", "--force", action="store_true", help="强制删除，不提示确认")
    delete_parser.set_defaults(func=delete_package)

    # 批量删除包命令
    batch_delete_parser = subparsers.add_parser("batch-delete", help="批量删除包")
    batch_delete_parser.add_argument("packages", nargs="+", help="包规格列表，格式: 包名")
    batch_delete_parser.add_argument("-p", "--parallel", action="store_true", help="并行删除")
    batch_delete_parser.add_argument("-w", "--workers", type=int, default=4, help="并行删除的工作线程数")
    batch_delete_parser.set_defaults(func=batch_delete_packages)
    
    # 配置命令
    config_parser = subparsers.add_parser("config", help="配置管理")
    config_parser.add_argument("--show", action="store_true", help="显示所有配置")
    config_parser.add_argument("--get", help="获取配置项值，格式: [section.]key")
    config_parser.add_argument("--set", help="设置配置项值，格式: [section.]key=value")
    config_parser.add_argument("--delete", help="删除配置项，格式: [section.]key")
    config_parser.set_defaults(func=config_cmd)
    
    # 清除缓存命令
    clear_cache_parser = subparsers.add_parser("clear-cache", help="清除缓存")
    clear_cache_parser.add_argument("-f", "--force", action="store_true", help="强制清除，不提示确认")
    clear_cache_parser.set_defaults(func=clear_cache)
    
    # 删除账户命令
    delete_account_parser = subparsers.add_parser("delete-account", help="删除用户账户")
    delete_account_parser.add_argument("-f", "--force", action="store_true", help="强制删除，不提示确认")
    delete_account_parser.set_defaults(func=delete_account)
    
    # 删除版本命令
    delete_version_parser = subparsers.add_parser("delete-version", help="删除包的特定版本")
    delete_version_parser.add_argument("name", help="包名")
    delete_version_parser.add_argument("version", help="版本号")
    delete_version_parser.add_argument("-f", "--force", action="store_true", help="强制删除，不提示确认")
    delete_version_parser.set_defaults(func=delete_version)
    
    args = parser.parse_args()
    
    if not args.command:
        # 如果没有指定命令，显示帮助信息
        print_welcome()
        parser.print_help()
        return
    
    args.func(args)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold yellow]操作已取消。[/bold yellow]")
        sys.exit(0)

