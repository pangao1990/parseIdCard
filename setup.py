#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
FilePath: /Python/parseIdCard/setup.py
Author: 潘高
LastEditors: 潘高
Date: 2021-08-18 15:32:37
LastEditTime: 2021-08-19 23:55:10
Description: 解析身份证
usage: 运行前，请确保本机已经搭建Python3开发环境，且已经安装 setuptools 模块。详细教程请移步至 https://blog.pangao.vip/Python环境搭建及模块安装/
        Example:
            https://pypi.python.org/simple/    # 查询项目是否重名
            python3 setup.py check    # 校验
            python3 -m build    # 在dist/下构建一个.tar.gz的源文件和一个.whl的二进制发行版
            python3 -m twine upload --repository testpypi dist/*    # 构建源码包发布到测试平台
            python3 -m twine upload --repository pypi dist/*    # 构建源码包发布到正式平台
'''

from setuptools import setup, find_packages

VERSION = '1.0.0.0'

with open('README.md', 'r', encoding='utf-8') as fp:
    long_description = fp.read()

setup(
    name = 'parseIdCard',     # 包名字
    version = VERSION,     # 包版本
    author = '潘高',     # 作者
    author_email = 'pangao1990@qq.com',     # 作者邮箱
    url = 'https://github.com',     # 包的主页
    project_urls = {"Blog": "https://blog.pangao.vip/%E5%8F%AF%E8%83%BD%E6%98%AFPython%E4%B8%AD%E6%9C%80%E5%A5%BD%E7%94%A8%E7%9A%84%E8%BA%AB%E4%BB%BD%E8%AF%81%E8%A7%A3%E6%9E%90%E5%B7%A5%E5%85%B7%E2%80%94parseIdCard/",},    # 额外链接
    description = '一款解析身份证的工具',     # 简单描述
    long_description = long_description,    # 详细描述
    long_description_content_type = "text/markdown",    # 详细描述的格式
    keywords='idard parse',    # 关键词
    include_package_data = True,    # 是否包含数据
    package_dir = {"": "src"},    # 根包
    packages = find_packages(where="src"),    # 包
    python_requires = '>=3',    # python最低版本要求
    classifiers = [
        "Programming Language :: Python :: 3",    # 该软件包仅与Python3兼容
        'Operating System :: OS Independent',    # 与操作系统无关
        'License :: OSI Approved :: MIT License'    # 根据MIT许可证开源
    ]
)
