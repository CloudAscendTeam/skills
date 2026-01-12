# 高频技术亮点识别指南

本文档提供9大高频技术领域的详细识别指南，帮助快速定位项目中的技术亮点和难点。

## 1. 高并发 (High Concurrency)

### 识别特征

#### 代码级特征
```java
// 线程池配置
ThreadPoolExecutor executor = new ThreadPoolExecutor(
    corePoolSize, maxPoolSize, keepAliveTime, TimeUnit.SECONDS, workQueue);

// 异步处理
@Async
public CompletableFuture<Result> asyncProcess() { }

// 并行流
list.parallelStream().forEach(item -> process(item));
```

#### 配置级特征
```yaml
# 线程池配置
thread:
  pool:
    core-size: 10
    max-size: 50
    queue-capacity: 1000

# Tomcat配置
server:
  tomcat:
    max-threads: 200
    accept-count: 100
```

#### 中间件特征
- Kafka/RabbitMQ/RocketMQ 消息队列
- Redis 缓存和分布式锁
- Nginx 负载均衡配置

### 关键词搜索
```bash
# 搜索线程池相关
grep -rn "ThreadPoolExecutor\|ExecutorService\|@Async" --include="*.java"

# 搜索消息队列
grep -rn "KafkaTemplate\|RabbitTemplate\|@RabbitListener\|@KafkaListener" --include="*.java"

# 搜索限流组件
grep -rn "RateLimiter\|Sentinel\|@SentinelResource" --include="*.java"
```

### 简历表达模板
```
- 设计并实现xxx高并发方案，采用[线程池+消息队列+缓存]架构，支持[X] QPS并发处理
- 通过[异步化+批量处理+限流降级]优化，系统吞吐量提升[X]%
- 基于[Kafka/RocketMQ]实现异步解耦，峰值处理能力达到[X]万/秒
```

### 面试话术
```
Q: 你们的高并发方案是怎么设计的？
A: 我们采用了三层策略：
   1. 接入层：Nginx负载均衡 + 请求限流
   2. 应用层：线程池隔离 + 异步消息队列
   3. 数据层：Redis缓存 + 读写分离
   通过这套方案，系统从原来的xxx QPS提升到xxx QPS。
```

---

## 2. 高可用 (High Availability)

### 识别特征

#### 代码级特征
```java
// 熔断降级
@CircuitBreaker(name = "backendService", fallbackMethod = "fallback")
public String callService() { }

// 重试机制
@Retry(name = "backendService", maxAttempts = 3)
public String retryCall() { }

// 健康检查
@Component
public class CustomHealthIndicator implements HealthIndicator {
    @Override
    public Health health() { }
}
```

#### 配置级特征
```yaml
# Resilience4j配置
resilience4j:
  circuitbreaker:
    instances:
      backendService:
        failure-rate-threshold: 50
        wait-duration-in-open-state: 5000

# Hystrix配置
hystrix:
  command:
    default:
      circuitBreaker:
        requestVolumeThreshold: 20
        errorThresholdPercentage: 50
```

#### 架构级特征
- 多节点部署配置
- 主从/主备切换逻辑
- 故障转移机制

### 关键词搜索
```bash
# 搜索熔断降级
grep -rn "CircuitBreaker\|@HystrixCommand\|Fallback" --include="*.java"

# 搜索重试机制
grep -rn "@Retry\|@Retryable\|RetryTemplate" --include="*.java"

# 搜索健康检查
grep -rn "HealthIndicator\|@Health\|actuator" --include="*.java" --include="*.yaml"
```

### 简历表达模板
```
- 设计并实现服务高可用架构，系统可用性从[X]%提升至[99.9X]%
- 实现服务熔断降级机制，故障隔离时间从[X]分钟缩短至[X]秒
- 设计异地多活方案，支持[X]地[X]中心容灾部署
```

### 面试话术
```
Q: 你们的高可用是怎么保证的？
A: 我们从多个层面保证：
   1. 服务层：Resilience4j熔断器，50%失败率自动熔断
   2. 部署层：K8s多副本部署，自动探活和重启
   3. 数据层：MySQL主从 + Redis Cluster
   线上实际可用性达到99.95%。
```

---

## 3. 可扩展 (Scalability)

### 识别特征

#### 代码级特征
```java
// SPI机制
ServiceLoader<Plugin> loader = ServiceLoader.load(Plugin.class);

// 策略模式
@Component("strategyA")
public class StrategyA implements PaymentStrategy { }

// 模板方法
public abstract class AbstractProcessor {
    protected abstract void doProcess();
}
```

#### 配置级特征
```yaml
# 策略配置
strategies:
  payment:
    - type: alipay
      class: com.xxx.AlipayStrategy
    - type: wechat
      class: com.xxx.WechatStrategy
```

#### 架构级特征
- Maven/Gradle 多模块结构
- 插件化目录结构
- 扩展点接口定义

### 关键词搜索
```bash
# 搜索SPI和插件
grep -rn "ServiceLoader\|@SPI\|Plugin" --include="*.java"

# 搜索策略模式
grep -rn "Strategy\|@Component.*strategy" --include="*.java"

# 搜索扩展点
grep -rn "ExtensionPoint\|@Extension" --include="*.java"
```

### 简历表达模板
```
- 设计可扩展的[xxx]架构，采用[SPI/策略模式/插件化]机制
- 支持[X]种支付方式/渠道的灵活扩展，新增渠道仅需[X]行配置
- 实现[水平扩展/垂直扩展]能力，单服务可扩展至[X]节点
```

---

## 4. 分布式架构 (Distributed Architecture)

### 识别特征

#### 代码级特征
```java
// 分布式锁
RLock lock = redissonClient.getLock("lockKey");
lock.lock(10, TimeUnit.SECONDS);

// 分布式事务
@GlobalTransactional
public void distributedTx() { }

// 服务发现
@EnableDiscoveryClient
public class Application { }
```

#### 配置级特征
```yaml
# Nacos配置
spring:
  cloud:
    nacos:
      discovery:
        server-addr: 127.0.0.1:8848
      config:
        server-addr: 127.0.0.1:8848

# Seata配置
seata:
  tx-service-group: my_tx_group
  service:
    vgroup-mapping:
      my_tx_group: default
```

### 关键词搜索
```bash
# 搜索分布式锁
grep -rn "Redisson\|@DistributedLock\|ZooKeeper.*lock" --include="*.java"

# 搜索分布式事务
grep -rn "@GlobalTransactional\|Seata\|TCC\|Saga" --include="*.java"

# 搜索服务发现
grep -rn "DiscoveryClient\|@EnableDiscoveryClient\|Nacos\|Eureka" --include="*.java"
```

### 简历表达模板
```
- 设计分布式架构，采用[Nacos/Eureka]实现服务注册发现，管理[X]个微服务
- 实现分布式锁方案，解决[库存超卖/重复下单/并发竞争]问题
- 基于[Seata AT/TCC/Saga]实现分布式事务，保证跨服务数据一致性
```

### 面试话术
```
Q: 你们的分布式事务是怎么处理的？
A: 根据业务场景选择不同方案：
   1. 强一致性场景（如支付）：采用Seata AT模式
   2. 最终一致性场景（如订单状态同步）：消息队列+本地消息表
   3. 幂等性保障：全局唯一ID+状态机
```

---

## 5. 微服务治理 (Microservice Governance)

### 识别特征

#### 代码级特征
```java
// API网关
@EnableGateway
public class GatewayApplication { }

// 链路追踪
@Autowired
private Tracer tracer;

// Feign调用
@FeignClient(name = "user-service")
public interface UserClient { }
```

#### 配置级特征
```yaml
# 网关路由
spring:
  cloud:
    gateway:
      routes:
        - id: user-service
          uri: lb://user-service
          predicates:
            - Path=/api/user/**

# 链路追踪
spring:
  sleuth:
    sampler:
      probability: 1.0
  zipkin:
    base-url: http://localhost:9411
```

### 关键词搜索
```bash
# 搜索网关配置
grep -rn "Gateway\|@EnableGateway\|RouteLocator" --include="*.java" --include="*.yaml"

# 搜索链路追踪
grep -rn "Sleuth\|Zipkin\|Tracer\|SkyWalking" --include="*.java" --include="*.yaml"

# 搜索服务调用
grep -rn "@FeignClient\|@DubboReference\|RestTemplate" --include="*.java"
```

### 简历表达模板
```
- 主导[X]个微服务的架构设计与拆分，服务数量从[X]到[Y]
- 实现基于[Spring Cloud Gateway/Kong]的统一API网关
- 集成[Sleuth+Zipkin/SkyWalking]实现全链路追踪，问题定位效率提升[X]%
```

---

## 6. 性能调优 (Performance Tuning)

### 识别特征

#### 代码级特征
```java
// 多级缓存
@Cacheable(value = "users", key = "#id")
public User getUser(Long id) { }

// 批量处理
@Transactional
public void batchInsert(List<Entity> list) {
    for (int i = 0; i < list.size(); i += BATCH_SIZE) {
        mapper.batchInsert(list.subList(i, Math.min(i + BATCH_SIZE, list.size())));
    }
}

// 懒加载
@OneToMany(fetch = FetchType.LAZY)
private List<Order> orders;
```

#### 配置级特征
```yaml
# 缓存配置
spring:
  cache:
    type: redis
    redis:
      time-to-live: 3600000

# 连接池配置
spring:
  datasource:
    hikari:
      maximum-pool-size: 20
      minimum-idle: 5
```

### 关键词搜索
```bash
# 搜索缓存
grep -rn "@Cacheable\|@CacheEvict\|RedisTemplate" --include="*.java"

# 搜索批量处理
grep -rn "batchInsert\|batchUpdate\|BATCH_SIZE" --include="*.java"

# 搜索连接池
grep -rn "HikariConfig\|DruidDataSource\|poolSize" --include="*.java" --include="*.yaml"
```

### 简历表达模板
```
- 优化[xxx]核心接口性能，响应时间从[X]ms降至[Y]ms
- 设计[本地缓存+Redis+DB]三级缓存架构，缓存命中率达[X]%
- 优化批量数据处理，处理效率提升[X]倍
```

### 面试话术
```
Q: 你是怎么做性能优化的？
A: 我通常从以下几个方面入手：
   1. 缓存：热点数据Redis缓存，本地Caffeine二级缓存
   2. SQL优化：慢查询分析，索引优化，避免全表扫描
   3. 批量处理：减少数据库交互次数
   4. 异步化：非核心逻辑异步执行
   最终将P99响应时间从500ms降到50ms。
```

---

## 7. 数据库设计 (Database Design)

### 识别特征

#### 代码级特征
```java
// 分库分表
@ShardingDataSource
public interface OrderMapper { }

// 读写分离
@Master
public void insert() { }

@Slave
public List<Entity> query() { }
```

#### 配置级特征
```yaml
# ShardingSphere配置
spring:
  shardingsphere:
    datasource:
      names: ds0,ds1
    rules:
      sharding:
        tables:
          t_order:
            actual-data-nodes: ds$->{0..1}.t_order_$->{0..15}
            table-strategy:
              standard:
                sharding-column: order_id
                sharding-algorithm-name: order_inline
```

### 关键词搜索
```bash
# 搜索分库分表
grep -rn "ShardingSphere\|MyCat\|@ShardingDataSource" --include="*.java" --include="*.yaml"

# 搜索读写分离
grep -rn "@Master\|@Slave\|ReadWriteSeparation" --include="*.java"

# 搜索索引定义
grep -rn "CREATE INDEX\|@Index\|unique.*index" --include="*.sql" --include="*.java"
```

### 简历表达模板
```
- 设计[X]库[Y]表的分库分表方案，支撑[X]亿级数据存储
- 实现MySQL读写分离，读性能提升[X]倍
- 优化慢SQL[X]条，平均查询时间从[X]ms降至[Y]ms
```

---

## 8. 锁机制 (Locking Mechanism)

### 识别特征

#### 代码级特征
```java
// 乐观锁
@Version
private Integer version;

// 悲观锁
@Select("SELECT * FROM table WHERE id = #{id} FOR UPDATE")
Entity selectForUpdate(Long id);

// 分布式锁
@DistributedLock(key = "'order:' + #orderId")
public void processOrder(String orderId) { }
```

### 关键词搜索
```bash
# 搜索乐观锁
grep -rn "@Version\|version.*=.*version.*\+.*1" --include="*.java"

# 搜索悲观锁
grep -rn "FOR UPDATE\|LOCK IN SHARE MODE" --include="*.java" --include="*.xml"

# 搜索分布式锁
grep -rn "@DistributedLock\|Redisson.*getLock\|tryLock" --include="*.java"
```

### 简历表达模板
```
- 设计[乐观锁/悲观锁/分布式锁]方案，解决[库存超卖/重复下单/并发更新]问题
- 基于[Redisson/ZooKeeper]实现分布式锁，锁竞争成功率达[X]%
- 优化锁粒度，系统吞吐量提升[X]%
```

---

## 9. 事务管理 (Transaction Management)

### 识别特征

#### 代码级特征
```java
// 本地事务
@Transactional(rollbackFor = Exception.class)
public void localTx() { }

// 分布式事务
@GlobalTransactional(timeoutMills = 60000)
public void globalTx() { }

// 事务传播
@Transactional(propagation = Propagation.REQUIRES_NEW)
public void nestedTx() { }
```

### 关键词搜索
```bash
# 搜索事务注解
grep -rn "@Transactional\|@GlobalTransactional" --include="*.java"

# 搜索事务传播
grep -rn "Propagation\.\|propagation.*=" --include="*.java"

# 搜索手动事务
grep -rn "TransactionTemplate\|PlatformTransactionManager" --include="*.java"
```

### 简历表达模板
```
- 设计[TCC/Saga/AT]分布式事务方案，保证跨服务数据一致性
- 实现[幂等性/补偿机制/重试策略]，事务成功率达[X]%
- 优化事务边界，数据库连接占用时间减少[X]%
```

---

## 快速检查清单

在分析项目时，可以使用以下命令快速扫描：

```bash
#!/bin/bash
echo "=== 高并发 ==="
grep -rn "ThreadPool\|@Async\|Kafka\|RabbitMQ" --include="*.java" | head -5

echo "=== 高可用 ==="
grep -rn "CircuitBreaker\|@Retry\|Fallback" --include="*.java" | head -5

echo "=== 分布式 ==="
grep -rn "Redisson\|@GlobalTransactional\|Nacos\|Eureka" --include="*.java" | head -5

echo "=== 微服务 ==="
grep -rn "@FeignClient\|Gateway\|Sleuth" --include="*.java" | head -5

echo "=== 缓存 ==="
grep -rn "@Cacheable\|RedisTemplate" --include="*.java" | head -5

echo "=== 数据库 ==="
grep -rn "ShardingSphere\|@Master\|@Slave" --include="*.java" | head -5

echo "=== 锁 ==="
grep -rn "@Version\|FOR UPDATE\|getLock" --include="*.java" | head -5

echo "=== 事务 ==="
grep -rn "@Transactional\|@GlobalTransactional" --include="*.java" | head -5
```

## 亮点评分标准

| 等级 | 标准 | 示例 |
|------|------|------|
| ⭐⭐⭐⭐⭐ | 自主设计核心架构方案 | 从0设计分布式事务框架 |
| ⭐⭐⭐⭐ | 主导复杂技术方案落地 | 主导微服务拆分重构 |
| ⭐⭐⭐ | 深度参与核心模块开发 | 实现分布式锁组件 |
| ⭐⭐ | 使用框架解决业务问题 | 使用Seata解决事务问题 |
| ⭐ | 了解并配置使用 | 配置Sentinel限流规则 |
