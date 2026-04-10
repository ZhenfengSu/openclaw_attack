# OpenClaw 本地接入分析

## 结论

如果后续攻击实验要尽量接近真实使用场景，最适合的主入口是 `openclaw agent`。

如果后续需要更强的自动化和更细的事件级采集，那么第二阶段应该切到 `openclaw gateway call`。

`openclaw capability` 只适合做模型层基线，不适合作为主实验入口。

`openclaw health` 只适合做实验前体检。

## 为什么 `openclaw agent` 最适合

### 1. 它走的是完整 agent 栈

攻击研究真正关心的不只是模型会不会被一句话影响，而是：

- 会不会改写目标
- 会不会改写 planning
- 会不会错误选工具
- 会不会污染 memory
- 会不会在多步轨迹中放大攻击

这些都属于 agent runtime 行为，而不是单纯模型补全行为。

### 2. 它天然复用 OpenClaw 的模型配置

的本地配置文件 `~/.openclaw/openclaw.json` 已经表明：

- 默认 agent 模型是 `moonshot/kimi-k2.5`
- provider 是 `moonshot`
- base URL 是 `https://api.moonshot.cn/v1`

所以从 `openclaw_attack` 的角度，不应该重复实现 Kimi client。
只要通过 OpenClaw 调 agent，实际就会走已经配置好的 Kimi 模型层。

### 3. 它更贴近真实攻击面

对攻击实验来说，最重要的是保留真实执行路径：

- session context
- tools
- skills
- model routing
- memory
- channel or workspace semantics

`openclaw agent` 比 `capability` 更能覆盖这些面。

## 为什么 `openclaw gateway` 很重要但不该作为第一入口

Gateway 是底层控制面，优势在于：

- 有统一 WebSocket RPC
- 可以做自动化调用
- 可以走 `gateway call <method>`
- 支持 `--expect-final`
- 更适合后续订阅事件、等待 run 结束、读取更细粒度状态

但如果一开始就直接走 Gateway RPC，会更复杂：

- 要处理认证 token
- 要自己拼 RPC method 和参数
- 要处理更底层的状态机

所以更合理的路线是：

### Phase 1

先用 `openclaw agent` 跑通攻击 case。

### Phase 2

再为 richer trace 和批量自动化补 `gateway call` 版本。

## 为什么 `openclaw capability` 不是主入口

`capability` 或 `infer` 更像 provider-backed inference。

适合：

- 比较不同模型的纯推理脆弱性
- 做不带完整 runtime 的 baseline

不适合：

- 测 agent 的 planning hijack
- 测 tool-choice hijack
- 测 memory persistence
- 测真实 session/runtime 下的攻击链

所以它应该是“基线实验接口”，不是“主实验接口”。

## 为什么 `openclaw health` 只能做预检查

`health` 的职责只是：

- 看 gateway 通不通
- 看 channel 是否正常
- 看 session store 是否健康

它不能执行攻击 case。

但它应该被放进实验脚本最前面，当作 preflight：

- `openclaw health --json`
- 或 `openclaw gateway status --require-rpc --json`

## 结合当前本地环境的观察

从本机当前信息看：

- OpenClaw CLI 已安装
- 配置文件存在于 `~/.openclaw/openclaw.json`
- 默认 agent 模型已经是 `moonshot/kimi-k2.5`
- gateway 目标地址是 `ws://127.0.0.1:18789`

同时也看到了一个现象：

- `gateway status --json` 能读到配置
- 但 `health --json` 当前返回了 gateway 连接异常

这说明当前真正需要优先解决的是：

1. 确认 18789 上实际运行的是哪一个 gateway 进程
2. 确认 token / RPC 是否可正常连通
3. 确认 `openclaw agent` 能否成功跑单轮请求

## 对 `openclaw_attack` 的直接影响

新仓库应该做如下收口：

- 不再新增 Kimi API 直连客户端
- 默认假设模型层由本地 OpenClaw 托管
- 把本地 OpenClaw runner 作为唯一主执行后端

建议的执行分层：

- `health`: 预检查
- `agent`: 主实验入口
- `gateway`: 高级自动化与 trace 增强
- `capability`: 仅用于模型层对照实验
