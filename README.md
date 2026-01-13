# CloudAscend Skills

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skills-blueviolet)](https://docs.anthropic.com/en/docs/claude-code)

Claude Code 技能插件集合。每个 skill 都是独立的功能模块，可以增强 Claude Code 的能力。

## 安装

```bash
# 克隆整个仓库到 Claude Code skills 目录
git clone https://github.com/CloudAscend/skills.git ~/.claude/skills/cloudascend-skills
```

## Skills 列表

| Skill | 描述 | 文档 |
|-------|------|------|
| [project-highlights](./skills/project-highlights/) | 深度分析项目代码库，识别技术亮点，生成架构图和简历项目描述 | [README](./skills/project-highlights/README.md) |

## Skills 简介

### Project Highlights

> 📍 [skills/project-highlights](./skills/project-highlights/)

一个能够深度分析项目代码库的技能插件，主要功能包括：

- **架构分析** - 识别架构模式，自动生成 Mermaid 系统架构图
- **技术亮点识别** - 覆盖高并发、高可用、分布式架构等 9 大技术领域
- **流程图生成** - 绘制核心业务流程图和时序图
- **简历输出** - 生成资深程序员级别的项目描述，包含量化成果

详细文档请查看 [Project Highlights README](./skills/project-highlights/README.md)

## 目录结构

```
.
├── README.md           # 本文件
├── LICENSE             # MIT 许可证
└── skills/
    └── project-highlights/    # 项目亮点分析技能
        ├── README.md
        ├── SKILL.md
        └── references/
```

## License

[MIT License](./LICENSE)
