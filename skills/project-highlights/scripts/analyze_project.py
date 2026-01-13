#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目结构分析脚本

功能:
- 自动检测项目类型和技术栈
- 分析代码统计（行数、文件数）
- 识别依赖关系
- 输出JSON格式分析报告

用法:
    python analyze_project.py --path /path/to/project
    python analyze_project.py --path . --output report.json
"""

import os
import sys
import json
import argparse
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Any, Optional
import re

# 配置文件与项目类型的映射
PROJECT_TYPE_MARKERS = {
    'pom.xml': {'type': 'Java Maven', 'language': 'Java'},
    'build.gradle': {'type': 'Java Gradle', 'language': 'Java'},
    'build.gradle.kts': {'type': 'Kotlin Gradle', 'language': 'Kotlin'},
    'package.json': {'type': 'Node.js', 'language': 'JavaScript/TypeScript'},
    'requirements.txt': {'type': 'Python', 'language': 'Python'},
    'pyproject.toml': {'type': 'Python', 'language': 'Python'},
    'setup.py': {'type': 'Python', 'language': 'Python'},
    'go.mod': {'type': 'Go', 'language': 'Go'},
    'Cargo.toml': {'type': 'Rust', 'language': 'Rust'},
    'composer.json': {'type': 'PHP', 'language': 'PHP'},
    'Gemfile': {'type': 'Ruby', 'language': 'Ruby'},
    '*.csproj': {'type': '.NET', 'language': 'C#'},
    '*.sln': {'type': '.NET', 'language': 'C#'},
}

# 文件扩展名与语言的映射
EXTENSION_LANGUAGE_MAP = {
    '.java': 'Java',
    '.kt': 'Kotlin',
    '.scala': 'Scala',
    '.py': 'Python',
    '.js': 'JavaScript',
    '.ts': 'TypeScript',
    '.tsx': 'TypeScript',
    '.jsx': 'JavaScript',
    '.go': 'Go',
    '.rs': 'Rust',
    '.rb': 'Ruby',
    '.php': 'PHP',
    '.cs': 'C#',
    '.cpp': 'C++',
    '.c': 'C',
    '.swift': 'Swift',
    '.vue': 'Vue',
    '.sql': 'SQL',
    '.sh': 'Shell',
    '.yml': 'YAML',
    '.yaml': 'YAML',
    '.xml': 'XML',
    '.json': 'JSON',
    '.md': 'Markdown',
}

# 技术栈关键词识别
TECH_STACK_PATTERNS = {
    # 后端框架
    'Spring Boot': [r'spring-boot', r'@SpringBootApplication'],
    'Spring Cloud': [r'spring-cloud', r'@EnableDiscoveryClient', r'@FeignClient'],
    'Spring MVC': [r'@Controller', r'@RestController', r'@RequestMapping'],
    'MyBatis': [r'mybatis', r'@Mapper', r'<mapper namespace'],
    'MyBatis-Plus': [r'mybatis-plus', r'BaseMapper'],
    'Dubbo': [r'dubbo', r'@DubboService', r'@DubboReference'],
    'Django': [r'django', r'from django'],
    'Flask': [r'flask', r'from flask import'],
    'FastAPI': [r'fastapi', r'from fastapi'],
    'Express': [r'"express"', r'require\([\'"]express[\'"]\)'],
    'NestJS': [r'@nestjs', r'@Controller', r'@Injectable'],
    'Gin': [r'github.com/gin-gonic/gin'],
    'Echo': [r'github.com/labstack/echo'],

    # 数据库
    'MySQL': [r'mysql', r'jdbc:mysql'],
    'PostgreSQL': [r'postgresql', r'postgres'],
    'MongoDB': [r'mongodb', r'MongoClient'],
    'Redis': [r'redis', r'RedisTemplate', r'Jedis', r'Lettuce'],
    'Elasticsearch': [r'elasticsearch', r'ElasticsearchClient'],
    'Oracle': [r'oracle', r'jdbc:oracle'],

    # 消息队列
    'Kafka': [r'kafka', r'KafkaTemplate', r'@KafkaListener'],
    'RabbitMQ': [r'rabbitmq', r'RabbitTemplate', r'@RabbitListener'],
    'RocketMQ': [r'rocketmq', r'RocketMQTemplate'],

    # 微服务组件
    'Nacos': [r'nacos', r'com.alibaba.nacos'],
    'Eureka': [r'eureka', r'@EnableEurekaClient'],
    'Consul': [r'consul'],
    'Sentinel': [r'sentinel', r'@SentinelResource'],
    'Hystrix': [r'hystrix', r'@HystrixCommand'],
    'Gateway': [r'spring-cloud-gateway', r'@EnableGateway'],
    'Seata': [r'seata', r'@GlobalTransactional'],

    # 前端框架
    'React': [r'"react"', r'import React'],
    'Vue': [r'"vue"', r'import Vue', r'\.vue$'],
    'Angular': [r'"@angular', r'@Component'],
    'Next.js': [r'"next"'],
    'Nuxt.js': [r'"nuxt"'],

    # 部署/运维
    'Docker': [r'Dockerfile', r'docker-compose'],
    'Kubernetes': [r'kubernetes', r'\.yaml.*kind:\s*Deployment'],
    'Jenkins': [r'Jenkinsfile', r'jenkins'],
}

# 需要忽略的目录
IGNORE_DIRS = {
    'node_modules', '.git', '.svn', '.hg', '__pycache__', '.idea', '.vscode',
    'target', 'build', 'dist', 'out', '.gradle', 'vendor', 'venv', 'env',
    '.tox', '.eggs', '*.egg-info', '.mypy_cache', '.pytest_cache'
}

# 需要忽略的文件
IGNORE_FILES = {'.DS_Store', 'Thumbs.db', '.gitignore', '.gitattributes'}


class ProjectAnalyzer:
    """项目分析器"""

    def __init__(self, project_path: str):
        self.project_path = Path(project_path).resolve()
        self.report: Dict[str, Any] = {
            'project_name': self.project_path.name,
            'project_path': str(self.project_path),
            'project_type': [],
            'languages': {},
            'tech_stack': [],
            'file_statistics': {},
            'directory_structure': {},
            'modules': [],
            'config_files': [],
            'highlights_hints': [],
        }

    def analyze(self) -> Dict[str, Any]:
        """执行完整分析"""
        print(f"Analyzing project: {self.project_path}")

        self._detect_project_type()
        self._analyze_file_statistics()
        self._detect_tech_stack()
        self._analyze_directory_structure()
        self._detect_modules()
        self._identify_highlights_hints()

        return self.report

    def _should_ignore(self, path: Path) -> bool:
        """判断是否应该忽略该路径"""
        for ignore_dir in IGNORE_DIRS:
            if ignore_dir in path.parts:
                return True
        if path.name in IGNORE_FILES:
            return True
        return False

    def _detect_project_type(self):
        """检测项目类型"""
        for config_file, info in PROJECT_TYPE_MARKERS.items():
            if '*' in config_file:
                # 通配符匹配
                pattern = config_file.replace('*', '')
                matches = list(self.project_path.glob(f'**/*{pattern}'))
                if matches:
                    self.report['project_type'].append(info['type'])
                    self.report['config_files'].extend([str(m.relative_to(self.project_path)) for m in matches[:5]])
            else:
                # 精确匹配
                config_path = self.project_path / config_file
                if config_path.exists():
                    self.report['project_type'].append(info['type'])
                    self.report['config_files'].append(config_file)

        # 去重
        self.report['project_type'] = list(set(self.report['project_type']))

    def _analyze_file_statistics(self):
        """分析文件统计信息"""
        language_stats = defaultdict(lambda: {'files': 0, 'lines': 0})
        total_files = 0
        total_lines = 0

        for file_path in self.project_path.rglob('*'):
            if file_path.is_file() and not self._should_ignore(file_path):
                ext = file_path.suffix.lower()
                if ext in EXTENSION_LANGUAGE_MAP:
                    lang = EXTENSION_LANGUAGE_MAP[ext]
                    language_stats[lang]['files'] += 1
                    total_files += 1

                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            lines = len(f.readlines())
                            language_stats[lang]['lines'] += lines
                            total_lines += lines
                    except Exception:
                        pass

        self.report['languages'] = dict(language_stats)
        self.report['file_statistics'] = {
            'total_files': total_files,
            'total_lines': total_lines,
            'by_language': dict(language_stats),
        }

    def _detect_tech_stack(self):
        """检测技术栈"""
        detected_tech = set()

        # 扫描配置文件和代码文件
        scan_extensions = {'.java', '.kt', '.py', '.js', '.ts', '.go', '.rs', '.xml', '.yaml', '.yml', '.json', '.gradle'}

        for file_path in self.project_path.rglob('*'):
            if file_path.is_file() and not self._should_ignore(file_path):
                ext = file_path.suffix.lower()
                if ext in scan_extensions:
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()

                            for tech, patterns in TECH_STACK_PATTERNS.items():
                                if tech not in detected_tech:
                                    for pattern in patterns:
                                        if re.search(pattern, content, re.IGNORECASE):
                                            detected_tech.add(tech)
                                            break
                    except Exception:
                        pass

        self.report['tech_stack'] = sorted(list(detected_tech))

    def _analyze_directory_structure(self):
        """分析目录结构"""
        structure = {}
        depth_limit = 3

        for item in sorted(self.project_path.iterdir()):
            if item.name.startswith('.') or item.name in IGNORE_DIRS:
                continue

            if item.is_dir():
                structure[item.name] = self._get_dir_structure(item, depth=1, max_depth=depth_limit)
            else:
                structure[item.name] = 'file'

        self.report['directory_structure'] = structure

    def _get_dir_structure(self, path: Path, depth: int, max_depth: int) -> Any:
        """递归获取目录结构"""
        if depth >= max_depth:
            return '...'

        structure = {}
        try:
            for item in sorted(path.iterdir()):
                if item.name.startswith('.') or item.name in IGNORE_DIRS:
                    continue

                if item.is_dir():
                    structure[item.name] = self._get_dir_structure(item, depth + 1, max_depth)
                else:
                    structure[item.name] = 'file'
        except PermissionError:
            pass

        return structure if structure else '(empty)'

    def _detect_modules(self):
        """检测模块/子项目"""
        modules = []

        # Maven多模块
        for pom in self.project_path.rglob('pom.xml'):
            if pom.parent != self.project_path:
                modules.append({
                    'name': pom.parent.name,
                    'type': 'Maven module',
                    'path': str(pom.parent.relative_to(self.project_path)),
                })

        # Gradle多模块
        for build_file in self.project_path.rglob('build.gradle*'):
            if build_file.parent != self.project_path:
                modules.append({
                    'name': build_file.parent.name,
                    'type': 'Gradle module',
                    'path': str(build_file.parent.relative_to(self.project_path)),
                })

        # Node.js子包
        for pkg in self.project_path.rglob('package.json'):
            if pkg.parent != self.project_path and 'node_modules' not in str(pkg):
                modules.append({
                    'name': pkg.parent.name,
                    'type': 'Node.js package',
                    'path': str(pkg.parent.relative_to(self.project_path)),
                })

        self.report['modules'] = modules

    def _identify_highlights_hints(self):
        """识别技术亮点提示"""
        hints = []

        tech_stack = set(self.report['tech_stack'])

        # 高并发
        if tech_stack & {'Kafka', 'RabbitMQ', 'RocketMQ', 'Redis'}:
            hints.append({
                'category': '高并发',
                'hint': '检测到消息队列/缓存组件，可能存在高并发处理方案',
                'search_keywords': ['ThreadPoolExecutor', '@Async', 'CompletableFuture', 'RateLimiter'],
            })

        # 高可用
        if tech_stack & {'Sentinel', 'Hystrix', 'Gateway'}:
            hints.append({
                'category': '高可用',
                'hint': '检测到熔断/网关组件，可能存在高可用设计',
                'search_keywords': ['CircuitBreaker', '@Retry', 'Fallback', 'HealthIndicator'],
            })

        # 分布式
        if tech_stack & {'Nacos', 'Eureka', 'Consul', 'Seata'}:
            hints.append({
                'category': '分布式架构',
                'hint': '检测到注册中心/分布式事务组件',
                'search_keywords': ['@GlobalTransactional', 'DistributedLock', 'Redisson'],
            })

        # 微服务
        if tech_stack & {'Spring Cloud', 'Dubbo'}:
            hints.append({
                'category': '微服务',
                'hint': '检测到微服务框架',
                'search_keywords': ['@FeignClient', '@DubboReference', 'RestTemplate'],
            })

        # 数据库
        if tech_stack & {'MyBatis', 'MyBatis-Plus'}:
            hints.append({
                'category': '数据库',
                'hint': '检测到ORM框架，可查找分库分表/读写分离配置',
                'search_keywords': ['ShardingSphere', '@Master', '@Slave', 'FOR UPDATE'],
            })

        # 缓存
        if 'Redis' in tech_stack:
            hints.append({
                'category': '性能优化',
                'hint': '检测到Redis，可查找缓存策略',
                'search_keywords': ['@Cacheable', '@CacheEvict', 'RedisTemplate'],
            })

        self.report['highlights_hints'] = hints


def main():
    parser = argparse.ArgumentParser(description='项目结构分析工具')
    parser.add_argument('--path', '-p', type=str, default='.', help='项目路径')
    parser.add_argument('--output', '-o', type=str, help='输出文件路径 (JSON)')
    parser.add_argument('--pretty', action='store_true', help='美化JSON输出')

    args = parser.parse_args()

    analyzer = ProjectAnalyzer(args.path)
    report = analyzer.analyze()

    # 输出结果
    indent = 2 if args.pretty else None
    json_output = json.dumps(report, ensure_ascii=False, indent=indent)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(json_output)
        print(f"Report saved to: {args.output}")
    else:
        print(json_output)

    # 打印摘要
    print("\n" + "=" * 50)
    print("项目分析摘要")
    print("=" * 50)
    print(f"项目名称: {report['project_name']}")
    print(f"项目类型: {', '.join(report['project_type']) or '未识别'}")
    print(f"主要语言: {', '.join(report['languages'].keys())}")
    print(f"技术栈: {', '.join(report['tech_stack'][:10])}")
    print(f"总文件数: {report['file_statistics']['total_files']}")
    print(f"总代码行: {report['file_statistics']['total_lines']}")
    print(f"模块数量: {len(report['modules'])}")
    print("=" * 50)

    if report['highlights_hints']:
        print("\n技术亮点提示:")
        for hint in report['highlights_hints']:
            print(f"  [{hint['category']}] {hint['hint']}")


if __name__ == '__main__':
    main()
