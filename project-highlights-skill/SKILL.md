---
name: project-highlights
description: |
  分析项目代码库，识别技术亮点和项目经验，生成架构图、流程图和资深程序员级别的简历内容。
  触发场景：
  (1) 用户要求分析项目亮点或技术特点
  (2) 用户需要总结项目经验或准备技术面试
  (3) 用户想要生成简历项目描述
  (4) 用户需要画架构图或流程图
  (5) 用户询问项目有哪些高并发、高可用等技术方案
---

# 项目亮点识别技能

本技能用于深度分析项目代码库，识别技术亮点和难点，生成可视化架构图，并输出资深程序员级别的简历项目描述。

## 重要：输出要求

**必须在分析完成后，将完整的分析报告保存到被分析项目的根目录下，文件名为 `project-highlights.md`。**

使用 Write 工具将报告内容写入该文件，确保用户可以直接查看和使用分析结果。

## 工作流程

请按照以下5个阶段完成项目分析：

### 阶段1: 初始扫描

**目标**: 快速了解项目全貌

1. **识别项目类型和技术栈**
   - 检测配置文件: `package.json`, `pom.xml`, `build.gradle`, `requirements.txt`, `go.mod`, `Cargo.toml` 等
   - 识别主要编程语言和框架
   - 分析依赖列表，识别关键中间件

2. **分析目录结构**
   - 识别模块划分方式（按功能/按层次/按领域）
   - 定位核心业务代码目录
   - 识别配置、测试、文档等辅助目录

3. **运行分析脚本**（可选）
   ```bash
   python scripts/analyze_project.py --path <项目路径>
   ```

**输出**: 项目概览报告，包含技术栈列表和目录结构说明

### 阶段2: 架构分析

**目标**: 理解系统架构并生成可视化图表

1. **识别架构模式**
   - 分层架构: Controller-Service-Repository
   - 微服务架构: 多个独立服务模块
   - DDD架构: Domain, Application, Infrastructure层
   - 事件驱动架构: 消息队列、事件总线

2. **生成系统架构图**（Mermaid格式）

   参考 `references/diagram-templates.md` 中的模板，根据识别的组件生成架构图：

   ```mermaid
   graph TB
       subgraph 接入层
           Gateway[API网关]
       end

       subgraph 服务层
           ServiceA[服务A]
           ServiceB[服务B]
       end

       subgraph 数据层
           DB[(数据库)]
           Cache[(缓存)]
       end

       Gateway --> ServiceA
       Gateway --> ServiceB
       ServiceA --> DB
       ServiceB --> Cache
   ```

3. **识别核心组件交互**
   - 服务间调用关系
   - 数据流转路径
   - 第三方集成点

**输出**: Mermaid格式的系统架构图

### 阶段3: 高频技术亮点识别

**目标**: 深度分析9大高频技术领域的亮点

参考 `references/tech-highlights.md` 进行详细分析：

#### 3.1 高并发方案
- [ ] 线程池配置: `ThreadPoolExecutor`, `@Async`
- [ ] 异步处理: `CompletableFuture`, 响应式编程
- [ ] 消息队列: `Kafka`, `RabbitMQ`, `RocketMQ`
- [ ] 限流降级: `Sentinel`, `Hystrix`, `RateLimiter`

#### 3.2 高可用设计
- [ ] 负载均衡: `Nginx`, `LoadBalancer`
- [ ] 熔断降级: `CircuitBreaker`, `Fallback`
- [ ] 健康检查: `Actuator`, `HealthCheck`
- [ ] 集群部署: 主从、多副本配置

#### 3.3 可扩展架构
- [ ] 插件机制: `SPI`, `Plugin`
- [ ] 策略模式: `Strategy`, 多实现类
- [ ] 模块化: Maven多模块、Gradle子项目

#### 3.4 分布式架构
- [ ] 分布式锁: `Redisson`, `Zookeeper`
- [ ] 分布式事务: `Seata`, `TCC`, `Saga`
- [ ] 服务发现: `Nacos`, `Eureka`, `Consul`
- [ ] 配置中心: `Apollo`, `Nacos Config`

#### 3.5 微服务治理
- [ ] 服务拆分: 独立部署单元
- [ ] API网关: `Spring Cloud Gateway`, `Kong`
- [ ] 链路追踪: `Sleuth`, `Zipkin`, `SkyWalking`
- [ ] 服务网格: `Istio`, `Envoy`

#### 3.6 性能调优
- [ ] 缓存策略: 多级缓存、缓存预热
- [ ] SQL优化: 索引优化、查询优化
- [ ] JVM调优: GC参数、内存配置
- [ ] 连接池: 数据库连接池、HTTP连接池

#### 3.7 数据库设计
- [ ] 分库分表: `ShardingSphere`, `MyCat`
- [ ] 读写分离: 主从复制
- [ ] 索引设计: 复合索引、覆盖索引
- [ ] 慢查询优化: `Explain`, 执行计划分析

#### 3.8 锁机制
- [ ] 乐观锁: `@Version`, CAS
- [ ] 悲观锁: `SELECT FOR UPDATE`
- [ ] 分布式锁: `Redis`, `Zookeeper`
- [ ] 死锁预防: 锁顺序、超时机制

#### 3.9 事务管理
- [ ] 本地事务: `@Transactional`
- [ ] 分布式事务: `XA`, `TCC`, `Saga`
- [ ] 补偿机制: 幂等设计、重试策略
- [ ] 最终一致性: 消息队列、事件驱动

**输出**: 技术亮点清单，标注发现的亮点和对应代码位置

### 阶段4: 流程图生成

**目标**: 绘制核心业务流程图

1. **识别核心业务流程**
   - 用户认证流程
   - 核心交易流程
   - 数据处理流程

2. **生成时序图**（关键交互）

   ```mermaid
   sequenceDiagram
       participant Client as 客户端
       participant Gateway as 网关
       participant Service as 服务
       participant DB as 数据库

       Client->>Gateway: 发起请求
       Gateway->>Service: 路由转发
       Service->>DB: 数据操作
       DB-->>Service: 返回结果
       Service-->>Gateway: 响应数据
       Gateway-->>Client: 返回响应
   ```

3. **生成流程图**（业务逻辑）

   ```mermaid
   flowchart TD
       A[开始] --> B{条件判断}
       B -->|是| C[执行操作A]
       B -->|否| D[执行操作B]
       C --> E[结束]
       D --> E
   ```

**输出**: Mermaid格式的业务流程图和时序图

### 阶段5: 价值评估与简历输出

**目标**: 生成资深程序员级别的简历项目描述，并保存到 `project-highlights.md`

参考 `references/resume-templates.md` 生成最终输出：

#### 5.1 项目概述
- 一句话描述项目定位和规模
- 突出业务价值和用户规模

#### 5.2 技术栈
按类别列出：
- 后端框架
- 数据库/缓存
- 中间件
- 部署/运维

#### 5.3 核心职责（3-5条）
使用动词开头，体现技术深度：
- "设计并实现..."
- "主导xxx重构..."
- "优化xxx性能..."

#### 5.4 技术亮点（2-3个）
使用【标签】格式突出高频技术点：
- 【高并发】xxx方案
- 【高可用】xxx设计
- 【分布式】xxx架构

#### 5.5 项目价值（量化数据）
- 性能提升百分比
- 可用性指标
- 业务指标改善

## 输出文件

完成所有分析后，**必须**使用 Write 工具将以下格式的报告保存到项目根目录下的 `project-highlights.md` 文件：

```markdown
# 项目亮点分析报告

> 生成时间: [当前日期时间]

## 1. 项目概览
[项目名称、类型、技术栈概述]

## 2. 系统架构图
[Mermaid架构图]

## 3. 技术亮点分析
[9大领域亮点识别结果]

## 4. 核心业务流程
[Mermaid流程图/时序图]

## 5. 简历项目描述
[格式化的简历内容]

## 6. 面试话术建议
[针对识别出的亮点的面试问答准备]
```

## 注意事项

1. **输出文件**: 分析完成后必须将报告保存到项目根目录的 `project-highlights.md` 文件
2. **大型项目处理**: 对于mono-repo或多模块项目，分模块进行分析
3. **隐私保护**: 不在输出中包含敏感配置信息
4. **客观评估**: 基于代码事实，不夸大项目亮点
5. **量化原则**: 尽量使用可量化的数据描述成果
6. **面试导向**: 输出内容要能经得起技术面试追问
