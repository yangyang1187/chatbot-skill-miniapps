# XiaocxPlugin

> 一个用于 [QChatGPT](https://github.com/RockChinQ/QChatGPT) 的小程序加载器插件，往 `data/` 目录丢一个 `.py` 文件，群里发 `/文件名` 即可调用，无需重启。

## 更新日志

### 0.3（本 fork，2026-08）

**安全加固**
- 命令名白名单校验 + 路径穿越双重防护（原版存在 `/../` 任意脚本执行漏洞）
- `sys.executable` 替代硬编码 `python`（修复只有 `python3` 的环境）
- 超时处理、空输出提示、队列消费竞态修复

**修复失效 API**（原版依赖的第三方接口大面积失效）
- 天气 → 无 token 自动降级 [wttr.in](https://wttr.in)，支持 `ALAPI_TOKEN` 环境变量
- 二次元图片 → dmoe.cc｜随机头像 → QQ 头像服务｜励志英语 → zenquotes
- 骚话 → hitokoto｜舔狗日记 → 60s API｜必应壁纸 → Bing 官方接口（带重试）
- 补全 `requirements.txt`（原为空）

**移除无可用源的小程序**（移入 `data/deprecated/`）
- 藏头诗、运气（星座运势）、弱智吧问答、摸头 —— 上游 API 已停止服务

### 0.2（原版）
更新了文档对部分小插件的使用讲解和图片示例

## 安装

配置完成 [QChatGPT](https://github.com/RockChinQ/QChatGPT) 主程序后，使用管理员账号向机器人发送命令：

```
!plugin get https://github.com/yangyang1187/XiaocxPlugin.git
```

或查看详细的[插件安装说明](https://github.com/RockChinQ/QChatGPT/wiki/5-%E6%8F%92%E4%BB%B6%E4%BD%BF%E7%94%A8)

安装依赖：

```bash
pip install -r requirements.txt
```

## 命令列表

### 可用命令（已实测，2026-08）

| 命令 | 说明 | 数据源 |
|---|---|---|
| `/天气 北京` | 查询城市天气（默认北京） | wttr.in / alapi |
| `/塔罗牌` | 随机抽取塔罗牌 | oiapi |
| `/BA 你好` | 生成自定义 BA logo 图片 | oiapi |
| `/kfc` | 生成疯狂星期四文案（一次两条） | ahfi |
| `/今天吃什么` | 随机推荐今天吃什么 | aa1 |
| `/励志英语` | 每日励志英文名言 | zenquotes |
| `/舔狗日记` | 随机生成舔狗日记 | 60s API |
| `/骚话` | 随机一句话 | hitokoto |
| `/二次元图片` | 随机高清二次元图片 | dmoe.cc |
| `/随机头像` | 随机动漫头像 | QQ 头像 |
| `/猫猫图片` | 随机一张猫猫图片 | thecatapi |
| `/必应壁纸` | 必应每日壁纸（可加天数偏移） | Bing 官方 |

### AI 绘图（需自备 API key）

调用 DALL·E-3 绘图，需要自己配置 API key 和地址：

```
/画图DALL·E-3 一只可爱的猫娘
```

另有 `/画图OpenAI` 版本。觉得命令太长可修改 `main.py` 中的前缀。

### 已停用（`data/deprecated/`）

上游 API 已停止服务，暂不可用：藏头诗、运气（星座运势）、弱智吧问答、摸头

### R18 命令（谨慎使用）

`/色图` `/真色图` `/看妹妹` `/看腿` —— 真的会返回 R18 内容，请注意场合！仅用于代码学习展示。

## 使用与开发

这是一个小程序加载器插件，`data/` 目录内的每个 `.py` 文件就是一个小程序。

### 添加自己的小程序

1. 写一个 `.py` 文件（只支持文本和图片输出）
2. 放到 `QChatGPT/plugins/XiaocxPlugin/data/` 目录
3. 群里发 `/文件名` 即可使用（无需重启）

文本类参考 `天气.py`，图片类参考 `猫猫图片.py`。

### 输出协议

- 文本：直接 `print()` 即可
- 图片：输出 Markdown 图片格式 `![描述](https://...)` 会被自动转为图片消息

### 修改命令前缀

如果 `/` 与其他插件冲突，修改 `main.py` 中：

```python
if cleaned_text.startswith('/'):  # 改成你想要的前缀，如 'AAA'
```

## 安全说明

⚠️ 本插件会以机器人权限执行 `data/` 目录下的任意 Python 脚本。请勿放入来源不明的脚本。

本 fork 已加固：命令名白名单 + 路径穿越防护，但 `data/` 目录本身的写入权限仍需自行管控。

## 上游

- 原项目：[sanxianxiaohuntun/XiaocxPlugin](https://github.com/sanxianxiaohuntun/XiaocxPlugin)
- 本 fork：[yangyang1187/XiaocxPlugin](https://github.com/yangyang1187/XiaocxPlugin)
