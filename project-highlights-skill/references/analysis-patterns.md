# 项目分析模式参考

本文档提供大型项目分析的策略、检查清单和评估标准。

## 一、项目类型识别

### 1.1 通过配置文件识别

| 配置文件 | 项目类型 | 技术栈 |
|---------|---------|-------|
| `pom.xml` | Java Maven | Spring Boot, MyBatis |
| `build.gradle` | Java Gradle | Spring Boot, Kotlin |
| `package.json` | Node.js/前端 | React, Vue, Express |
| `requirements.txt` / `pyproject.toml` | Python | Django, Flask, FastAPI |
| `go.mod` | Go | Gin, Echo |
| `Cargo.toml` | Rust | Actix, Tokio |
| `composer.json` | PHP | Laravel, Symfony |
| `Gemfile` | Ruby | Rails |
| `*.csproj` | .NET | ASP.NET Core |

### 1.2 通过目录结构识别

```bash
# Maven标准结构
src/main/java/           # Java源码
src/main/resources/      # 配置文件
src/test/java/           # 测试代码

# Spring Boot分层结构
controller/              # 控制器层
service/                 # 业务层
repository/ / dao/       # 数据层
entity/ / model/         # 实体类

# DDD结构
domain/                  # 领域层
application/             # 应用层
infrastructure/          # 基础设施层
interfaces/              # 接口层

# 微服务结构
xxx-api/                 # API网关
xxx-service/             # 业务服务
xxx-common/              # 公共模块
xxx-gateway/             # 网关服务
```

---

## 二、大型项目分析策略

### 2.1 分层分析法

```
┌─────────────────────────────────────────────────┐
│                   1. 接入层分析                   │
│  - 入口点识别 (Controller, Handler)              │
│  - API设计风格 (RESTful, GraphQL, gRPC)         │
│  - 认证授权机制                                   │
└─────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────┐
│                   2. 业务层分析                   │
│  - 核心业务逻辑                                   │
│  - 设计模式使用                                   │
│  - 服务间调用方式                                 │
└─────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────┐
│                   3. 数据层分析                   │
│  - 数据库选型                                     │
│  - ORM框架使用                                    │
│  - 缓存策略                                       │
└─────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────┐
│                   4. 基础设施分析                 │
│  - 中间件使用                                     │
│  - 部署架构                                       │
│  - 监控告警                                       │
└─────────────────────────────────────────────────┘
```

### 2.2 模块分析法（适用于微服务/多模块项目）

```bash
# 步骤1: 识别所有模块
find . -name "pom.xml" -o -name "build.gradle" -o -name "package.json" | head -20

# 步骤2: 分析模块依赖关系
# Maven: mvn dependency:tree
# Gradle: gradle dependencies
# npm: npm ls

# 步骤3: 识别核心模块
# 被依赖最多的模块通常是核心模块

# 步骤4: 逐模块分析
for module in $(find . -maxdepth 2 -name "pom.xml" -exec dirname {} \;); do
    echo "=== Analyzing $module ==="
    # 分析每个模块
done
```

### 2.3 入口追踪法

从入口点开始，沿着调用链追踪核心业务逻辑：

```
Controller → Service → Repository → Database
     ↓          ↓           ↓
  DTO/VO    业务逻辑      数据访问
     ↓          ↓           ↓
  参数校验   事务管理     SQL优化
```

---

## 三、项目复杂度评估矩阵

### 3.1 代码规模评估

| 等级 | 代码行数 | 文件数 | 模块数 | 典型项目 |
|------|---------|--------|--------|---------|
| 小型 | < 1万 | < 50 | 1-2 | 工具类项目 |
| 中型 | 1-10万 | 50-200 | 3-5 | 业务系统 |
| 大型 | 10-50万 | 200-1000 | 5-20 | 平台系统 |
| 超大型 | > 50万 | > 1000 | > 20 | 电商/金融核心 |

### 3.2 技术复杂度评估

| 维度 | 低复杂度 | 中复杂度 | 高复杂度 |
|------|---------|---------|---------|
| 架构 | 单体MVC | 分层架构 | 微服务/DDD |
| 数据 | 单库单表 | 主从/读写分离 | 分库分表 |
| 缓存 | 无/简单缓存 | Redis单机 | 多级缓存/集群 |
| 消息 | 无 | 单一MQ | 多MQ混合 |
| 事务 | 本地事务 | 可靠消息 | 分布式事务 |
| 部署 | 单机 | 集群 | K8s/多活 |

### 3.3 综合评分表

```
项目复杂度得分 =
    代码规模(20%) +
    技术复杂度(30%) +
    业务复杂度(30%) +
    团队规模(10%) +
    项目周期(10%)

得分区间:
- 0-40:  初级项目
- 40-60: 中级项目
- 60-80: 高级项目
- 80-100: 专家级项目
```

---

## 四、亮点发掘检查清单

### 4.1 架构设计亮点

- [ ] **架构模式**: 是否采用了清晰的架构模式（分层/DDD/六边形）？
- [ ] **模块划分**: 模块边界是否清晰？职责是否单一？
- [ ] **依赖管理**: 依赖方向是否合理？是否存在循环依赖？
- [ ] **扩展性设计**: 是否有插件化/策略模式等扩展机制？
- [ ] **解耦设计**: 核心业务与技术实现是否解耦？

### 4.2 性能优化亮点

- [ ] **缓存策略**: 是否有多级缓存？缓存更新策略是否合理？
- [ ] **异步处理**: 非核心逻辑是否异步化？
- [ ] **批量处理**: 是否优化了批量数据操作？
- [ ] **连接池**: 各种连接池配置是否合理？
- [ ] **SQL优化**: 是否有复杂SQL的优化？索引设计是否合理？

### 4.3 高可用亮点

- [ ] **容错机制**: 是否有熔断、降级、重试机制？
- [ ] **故障隔离**: 服务间是否有隔离措施？
- [ ] **数据冗余**: 数据是否有备份和冗余？
- [ ] **监控告警**: 是否有完善的监控和告警？
- [ ] **灰度发布**: 是否支持灰度发布/蓝绿部署？

### 4.4 安全设计亮点

- [ ] **认证授权**: 认证机制是否安全（JWT、OAuth2）？
- [ ] **数据加密**: 敏感数据是否加密存储和传输？
- [ ] **接口安全**: 是否有防重放、防篡改机制？
- [ ] **SQL注入**: 是否使用参数化查询？
- [ ] **XSS防护**: 是否有XSS过滤？

### 4.5 工程化亮点

- [ ] **代码规范**: 是否有统一的代码规范和检查？
- [ ] **单元测试**: 测试覆盖率如何？
- [ ] **CI/CD**: 是否有自动化构建和部署流水线？
- [ ] **文档**: 是否有API文档、架构文档？
- [ ] **日志**: 日志规范是否统一？是否便于排查问题？

---

## 五、代码模式识别

### 5.1 设计模式识别

```bash
# 单例模式
grep -rn "private static.*instance\|getInstance()" --include="*.java"

# 工厂模式
grep -rn "Factory\|create.*return new" --include="*.java"

# 策略模式
grep -rn "interface.*Strategy\|implements.*Strategy" --include="*.java"

# 观察者模式
grep -rn "Observer\|Listener\|@EventListener" --include="*.java"

# 模板方法
grep -rn "abstract.*Template\|extends.*Template" --include="*.java"

# 责任链
grep -rn "Chain\|Handler.*next\|setNext" --include="*.java"
```

### 5.2 技术栈特征识别

```bash
# Spring框架特征
grep -rn "@SpringBootApplication\|@RestController\|@Service" --include="*.java" | head -5

# MyBatis特征
grep -rn "@Mapper\|@Select\|<mapper namespace" --include="*.java" --include="*.xml" | head -5

# 微服务特征
grep -rn "@FeignClient\|@EnableDiscoveryClient\|spring.cloud" --include="*.java" --include="*.yaml" | head -5

# 消息队列特征
grep -rn "@KafkaListener\|@RabbitListener\|JmsTemplate" --include="*.java" | head -5
```

### 5.3 复杂业务逻辑识别

```bash
# 复杂条件判断（可能的业务规则）
grep -rn "if.*&&.*&&\|switch.*case.*case.*case" --include="*.java" | head -10

# 状态机
grep -rn "State\|Status.*enum\|FSM\|StateMachine" --include="*.java" | head -5

# 工作流
grep -rn "Workflow\|Process\|Activity\|activiti" --include="*.java" | head -5

# 规则引擎
grep -rn "Drools\|@Rule\|RuleEngine" --include="*.java" | head -5
```

---

## 六、技术债务识别

### 6.1 代码异味检测

| 异味类型 | 识别特征 | 严重程度 |
|---------|---------|---------|
| 过长方法 | 方法超过100行 | 中 |
| 过大类 | 类超过1000行 | 高 |
| 重复代码 | 相似代码块超过3处 | 中 |
| 过深嵌套 | if/for嵌套超过4层 | 中 |
| 魔法数字 | 硬编码的数字/字符串 | 低 |
| 过长参数 | 方法参数超过5个 | 中 |

### 6.2 架构债务识别

| 债务类型 | 识别特征 | 影响 |
|---------|---------|------|
| 循环依赖 | A→B→C→A | 部署困难 |
| 上帝类 | 一个类做所有事 | 维护困难 |
| 贫血模型 | 实体类只有getter/setter | 业务散落 |
| 分层混乱 | Controller调用Repository | 边界模糊 |
| 硬编码配置 | 环境相关配置写死 | 部署困难 |

### 6.3 技术债务检查命令

```bash
# 检查过大文件
find . -name "*.java" -exec wc -l {} \; | sort -rn | head -10

# 检查TODO/FIXME
grep -rn "TODO\|FIXME\|HACK\|XXX" --include="*.java" | wc -l

# 检查废弃注解
grep -rn "@Deprecated" --include="*.java" | wc -l

# 检查注释代码
grep -rn "^[[:space:]]*//" --include="*.java" | wc -l
```

---

## 七、项目分析报告模板

```markdown
# 项目分析报告: [项目名称]

## 1. 项目概览

### 1.1 基本信息
- **项目名称**:
- **项目类型**: [Web应用/微服务/工具库/平台]
- **技术栈**:
- **代码规模**: [X万行代码, Y个文件, Z个模块]

### 1.2 技术栈清单

| 类别 | 技术 | 版本 |
|------|------|------|
| 语言 | | |
| 框架 | | |
| 数据库 | | |
| 缓存 | | |
| 消息队列 | | |
| 部署 | | |

## 2. 架构分析

### 2.1 架构模式
[描述采用的架构模式: 分层/微服务/DDD等]

### 2.2 架构图
[Mermaid架构图]

### 2.3 模块说明

| 模块 | 职责 | 依赖 |
|------|------|------|
| | | |

## 3. 技术亮点

### 3.1 高频技术亮点
[按9大领域列出识别到的亮点]

### 3.2 亮点详情
[每个亮点的具体实现和代码位置]

## 4. 复杂度评估

| 维度 | 评分 | 说明 |
|------|------|------|
| 代码规模 | /10 | |
| 技术复杂度 | /10 | |
| 业务复杂度 | /10 | |
| **综合评分** | /10 | |

## 5. 改进建议

### 5.1 技术债务
[识别到的技术债务]

### 5.2 优化建议
[针对性的改进建议]

## 6. 简历项目描述
[格式化的简历内容]
```

---

## 八、分析工具推荐

| 工具 | 用途 | 命令示例 |
|------|------|---------|
| `cloc` | 代码行数统计 | `cloc --by-file .` |
| `tokei` | 快速代码统计 | `tokei .` |
| `tree` | 目录结构 | `tree -L 3 -d` |
| `grep` | 关键词搜索 | `grep -rn "pattern"` |
| `find` | 文件查找 | `find . -name "*.java"` |
| `wc` | 文件统计 | `wc -l *.java` |
