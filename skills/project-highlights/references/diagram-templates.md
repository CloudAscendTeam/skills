# 架构图和流程图模板

本文档提供各类Mermaid图表模板，用于生成项目架构图和流程图。

## Mermaid 语法速查

### 基本语法
```
graph TB    # 从上到下
graph LR    # 从左到右
graph BT    # 从下到上
graph RL    # 从右到左
```

### 节点形状
```
A[矩形]
B(圆角矩形)
C((圆形))
D{菱形}
E[(数据库)]
F[[子程序]]
```

### 连接线
```
A --> B     # 实线箭头
A --- B     # 实线无箭头
A -.-> B    # 虚线箭头
A ==> B     # 粗线箭头
A --文字--> B  # 带文字的连接
```

---

## 一、系统架构图模板

### 1.1 分层架构图

```mermaid
graph TB
    subgraph 表现层 [Presentation Layer]
        Web[Web前端]
        App[移动端]
        API[开放API]
    end

    subgraph 网关层 [Gateway Layer]
        Nginx[Nginx负载均衡]
        Gateway[API网关]
    end

    subgraph 业务层 [Business Layer]
        BizService1[业务服务A]
        BizService2[业务服务B]
        BizService3[业务服务C]
    end

    subgraph 服务层 [Service Layer]
        BaseService1[基础服务1]
        BaseService2[基础服务2]
    end

    subgraph 数据层 [Data Layer]
        MySQL[(MySQL)]
        Redis[(Redis)]
        ES[(Elasticsearch)]
        MQ[消息队列]
    end

    Web --> Nginx
    App --> Nginx
    API --> Nginx
    Nginx --> Gateway
    Gateway --> BizService1
    Gateway --> BizService2
    Gateway --> BizService3
    BizService1 --> BaseService1
    BizService2 --> BaseService2
    BaseService1 --> MySQL
    BaseService1 --> Redis
    BaseService2 --> ES
    BizService3 --> MQ
```

### 1.2 微服务架构图

```mermaid
graph TB
    subgraph 客户端 [Clients]
        WebApp[Web应用]
        MobileApp[移动应用]
        ThirdParty[第三方系统]
    end

    subgraph 网关 [API Gateway]
        GW[Spring Cloud Gateway]
    end

    subgraph 微服务 [Microservices]
        UserService[用户服务]
        OrderService[订单服务]
        ProductService[商品服务]
        PayService[支付服务]
        NotifyService[通知服务]
    end

    subgraph 服务治理 [Service Governance]
        Nacos[Nacos注册中心]
        Config[配置中心]
        Sentinel[Sentinel限流]
    end

    subgraph 基础设施 [Infrastructure]
        Redis[(Redis Cluster)]
        MySQL[(MySQL主从)]
        Kafka[Kafka]
        ES[(Elasticsearch)]
    end

    subgraph 监控 [Monitoring]
        Prometheus[Prometheus]
        Grafana[Grafana]
        SkyWalking[SkyWalking]
    end

    WebApp --> GW
    MobileApp --> GW
    ThirdParty --> GW

    GW --> UserService
    GW --> OrderService
    GW --> ProductService
    GW --> PayService

    UserService -.-> Nacos
    OrderService -.-> Nacos
    ProductService -.-> Nacos
    PayService -.-> Nacos
    NotifyService -.-> Nacos

    OrderService --> Kafka
    Kafka --> NotifyService

    UserService --> Redis
    OrderService --> MySQL
    ProductService --> ES
    PayService --> MySQL

    UserService -.-> Prometheus
    OrderService -.-> Prometheus
```

### 1.3 DDD架构图

```mermaid
graph TB
    subgraph 用户接口层 [User Interface]
        Controller[Controller]
        DTO[DTO]
    end

    subgraph 应用层 [Application Layer]
        AppService[ApplicationService]
        Assembler[Assembler]
        Command[Command/Query]
    end

    subgraph 领域层 [Domain Layer]
        Entity[Entity]
        ValueObject[ValueObject]
        DomainService[DomainService]
        Repository[Repository接口]
        DomainEvent[DomainEvent]
    end

    subgraph 基础设施层 [Infrastructure]
        RepositoryImpl[Repository实现]
        Gateway[外部网关]
        MQ[消息队列]
        Persistence[持久化]
    end

    Controller --> AppService
    AppService --> DomainService
    AppService --> Repository
    DomainService --> Entity
    Entity --> ValueObject
    Repository --> RepositoryImpl
    RepositoryImpl --> Persistence
    DomainService --> DomainEvent
    DomainEvent --> MQ
```

### 1.4 事件驱动架构图

```mermaid
graph LR
    subgraph 生产者 [Producers]
        P1[订单服务]
        P2[支付服务]
        P3[用户服务]
    end

    subgraph 消息中间件 [Message Broker]
        Kafka[Kafka Cluster]
    end

    subgraph 消费者 [Consumers]
        C1[库存服务]
        C2[通知服务]
        C3[积分服务]
        C4[数据分析]
    end

    P1 -->|OrderCreated| Kafka
    P1 -->|OrderPaid| Kafka
    P2 -->|PaymentSuccess| Kafka
    P3 -->|UserRegistered| Kafka

    Kafka -->|OrderCreated| C1
    Kafka -->|OrderPaid| C2
    Kafka -->|PaymentSuccess| C3
    Kafka -->|All Events| C4
```

---

## 二、部署架构图模板

### 2.1 Kubernetes部署架构

```mermaid
graph TB
    subgraph Internet
        User[用户]
    end

    subgraph K8s Cluster
        subgraph Ingress
            Nginx[Nginx Ingress]
        end

        subgraph Namespace: Production
            subgraph Deployment: API
                Pod1[Pod-API-1]
                Pod2[Pod-API-2]
                Pod3[Pod-API-3]
            end

            subgraph Deployment: Worker
                WPod1[Pod-Worker-1]
                WPod2[Pod-Worker-2]
            end

            Service[Service]
        end

        subgraph StatefulSet
            Redis[(Redis)]
            MySQL[(MySQL)]
        end
    end

    User --> Nginx
    Nginx --> Service
    Service --> Pod1
    Service --> Pod2
    Service --> Pod3
    Pod1 --> Redis
    Pod1 --> MySQL
    WPod1 --> MySQL
```

### 2.2 多活部署架构

```mermaid
graph TB
    subgraph 北京机房 [Beijing DC]
        LB1[负载均衡]
        App1[应用集群]
        DB1[(MySQL主)]
        Cache1[(Redis主)]
    end

    subgraph 上海机房 [Shanghai DC]
        LB2[负载均衡]
        App2[应用集群]
        DB2[(MySQL从)]
        Cache2[(Redis从)]
    end

    DNS[智能DNS]

    DNS --> LB1
    DNS --> LB2
    LB1 --> App1
    LB2 --> App2
    App1 --> DB1
    App1 --> Cache1
    App2 --> DB2
    App2 --> Cache2
    DB1 -.->|主从同步| DB2
    Cache1 -.->|数据同步| Cache2
```

---

## 三、业务流程图模板

### 3.1 下单流程图

```mermaid
flowchart TD
    A[用户发起下单] --> B{库存检查}
    B -->|库存充足| C[锁定库存]
    B -->|库存不足| D[返回库存不足]

    C --> E[创建订单]
    E --> F{优惠券校验}
    F -->|有效| G[应用优惠]
    F -->|无效| H[原价结算]

    G --> I[计算金额]
    H --> I

    I --> J[生成支付单]
    J --> K[返回支付信息]

    K --> L{支付结果}
    L -->|支付成功| M[更新订单状态]
    L -->|支付超时| N[释放库存]
    L -->|支付失败| O[订单取消]

    M --> P[发送订单消息]
    P --> Q[扣减库存]
    P --> R[发送通知]
    P --> S[增加积分]
```

### 3.2 分布式事务流程图

```mermaid
flowchart TD
    A[TM: 开启全局事务] --> B[调用订单服务]
    B --> C[订单服务: 创建订单]
    C --> D{订单创建成功?}

    D -->|是| E[调用库存服务]
    D -->|否| F[TM: 回滚]

    E --> G[库存服务: 扣减库存]
    G --> H{库存扣减成功?}

    H -->|是| I[调用账户服务]
    H -->|否| J[TM: 回滚订单]

    I --> K[账户服务: 扣减余额]
    K --> L{余额扣减成功?}

    L -->|是| M[TM: 提交全局事务]
    L -->|否| N[TM: 回滚订单和库存]

    M --> O[事务完成]

    J --> P[订单服务: 删除订单]
    N --> Q[库存服务: 恢复库存]
    Q --> P
```

---

## 四、时序图模板

### 4.1 用户登录时序图

```mermaid
sequenceDiagram
    participant C as 客户端
    participant G as API网关
    participant U as 用户服务
    participant R as Redis
    participant D as 数据库

    C->>G: POST /login (username, password)
    G->>U: 转发请求

    U->>R: 查询登录失败次数
    R-->>U: 返回次数

    alt 失败次数超限
        U-->>G: 账号锁定
        G-->>C: 403 Forbidden
    else 可以登录
        U->>D: 查询用户信息
        D-->>U: 返回用户数据
        U->>U: 校验密码

        alt 密码正确
            U->>R: 清除失败次数
            U->>U: 生成JWT Token
            U->>R: 存储Token
            U-->>G: 登录成功 + Token
            G-->>C: 200 OK + Token
        else 密码错误
            U->>R: 增加失败次数
            U-->>G: 登录失败
            G-->>C: 401 Unauthorized
        end
    end
```

### 4.2 订单支付时序图

```mermaid
sequenceDiagram
    participant C as 客户端
    participant O as 订单服务
    participant P as 支付服务
    participant T as 第三方支付
    participant N as 通知服务
    participant MQ as 消息队列

    C->>O: 发起支付
    O->>O: 校验订单状态
    O->>P: 创建支付单

    P->>T: 调用支付接口
    T-->>P: 返回支付二维码

    P-->>O: 支付单信息
    O-->>C: 返回支付页面

    Note over C,T: 用户扫码支付

    T->>P: 支付回调
    P->>P: 验证签名
    P->>O: 更新订单状态

    O->>MQ: 发送支付成功事件
    MQ->>N: 消费事件
    N->>C: 推送支付成功通知

    O-->>T: 回调确认
```

### 4.3 分布式锁时序图

```mermaid
sequenceDiagram
    participant S1 as 服务实例1
    participant S2 as 服务实例2
    participant R as Redis

    S1->>R: SETNX lock_key value EX 30
    R-->>S1: OK (获取锁成功)

    S2->>R: SETNX lock_key value EX 30
    R-->>S2: FAIL (锁已存在)

    S2->>S2: 等待重试

    S1->>S1: 执行业务逻辑

    S1->>R: Lua脚本: 验证value并删除
    R-->>S1: 释放锁成功

    S2->>R: SETNX lock_key value EX 30
    R-->>S2: OK (获取锁成功)
```

---

## 五、数据流图模板

### 5.1 数据同步流图

```mermaid
flowchart LR
    subgraph 源数据 [Source]
        MySQL[(业务MySQL)]
    end

    subgraph 数据采集 [Collection]
        Canal[Canal]
    end

    subgraph 消息队列 [MQ]
        Kafka[Kafka]
    end

    subgraph 数据处理 [Processing]
        Flink[Flink]
    end

    subgraph 目标存储 [Target]
        ES[(Elasticsearch)]
        ClickHouse[(ClickHouse)]
        Redis[(Redis)]
    end

    MySQL -->|binlog| Canal
    Canal -->|JSON| Kafka
    Kafka --> Flink
    Flink -->|实时| ES
    Flink -->|实时| Redis
    Flink -->|批量| ClickHouse
```

### 5.2 缓存数据流图

```mermaid
flowchart TD
    A[请求到达] --> B{本地缓存}
    B -->|命中| C[返回数据]
    B -->|未命中| D{Redis缓存}

    D -->|命中| E[写入本地缓存]
    E --> C

    D -->|未命中| F{获取分布式锁}
    F -->|成功| G[查询数据库]
    F -->|失败| H[等待重试]

    G --> I[写入Redis]
    I --> E

    H --> D
```

---

## 六、状态图模板

### 6.1 订单状态机

```mermaid
stateDiagram-v2
    [*] --> 待支付: 创建订单

    待支付 --> 已支付: 支付成功
    待支付 --> 已取消: 超时/用户取消

    已支付 --> 待发货: 商家确认
    已支付 --> 退款中: 申请退款

    待发货 --> 已发货: 发货
    待发货 --> 退款中: 申请退款

    已发货 --> 已签收: 确认收货
    已发货 --> 退货中: 申请退货

    已签收 --> 已完成: 系统自动
    已签收 --> 售后中: 申请售后

    退款中 --> 已退款: 退款成功
    退货中 --> 已退货: 退货成功

    已取消 --> [*]
    已完成 --> [*]
    已退款 --> [*]
    已退货 --> [*]
```

---

## 使用指南

### 根据项目类型选择模板

| 项目类型 | 推荐架构图 | 推荐流程图 |
|---------|-----------|-----------|
| 单体应用 | 分层架构图 | 业务流程图 |
| 微服务 | 微服务架构图 | 时序图 |
| DDD项目 | DDD架构图 | 领域事件流 |
| 大数据 | 数据流图 | 数据管道图 |
| 电商系统 | 微服务+状态机 | 订单流程+支付时序 |

### 图表生成步骤

1. **识别核心组件**: 列出系统的主要服务、数据存储、中间件
2. **确定组件关系**: 标注组件间的调用、依赖、数据流向
3. **分组分层**: 按功能或层次对组件进行分组
4. **选择模板**: 根据项目类型选择合适的模板
5. **定制修改**: 替换模板中的组件名称和关系
