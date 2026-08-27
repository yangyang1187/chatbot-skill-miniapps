# chatbot-skill-miniapps

> 给 AI Agent / 聊天机器人直接调用的小程序技能包：天气、塔罗牌、必应壁纸、猫猫图片等 12+ 个即用命令，配套加固版安全运行器，一条命令即可调用，输出结构化 JSON。

## 🚀 一句话安装（把下面这句发给你的 AI Agent）

> 帮我安装小程序技能：`bash <(curl -fsSL https://raw.githubusercontent.com/yangyang1187/chatbot-skill-miniapps/main/install.sh)`，装完按它提示的方式用。

装好后直接说「北京天气」「抽个塔罗牌」「今天吃什么」即可。

### 手动安装（不用 Agent 也行）

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/yangyang1187/chatbot-skill-miniapps/main/install.sh)
# 或
git clone https://github.com/yangyang1187/chatbot-skill-miniapps.git && cd chatbot-skill-miniapps && bash install.sh
```

## 这是什么

每个小程序是 `data/` 目录下一个独立的 Python 脚本，由 `tools/run_miniapp.py` 安全运行：

```bash
python3 tools/run_miniapp.py . 天气 北京
# {"ok": true, "command": "天气", "text": "北京: 多云 +26°C ...", "images": []}
```

Agent 拿到 JSON 后把 `text` 发给用户、把 `images` 里的 URL 作为图片发送即可。

## 命令列表（已实测）

| 命令 | 说明 | 数据源 |
|---|---|---|
| `天气 <城市>` | 查询城市天气（默认北京） | wttr.in / alapi |
| `塔罗牌` | 随机抽取塔罗牌（文+图） | oiapi |
| `BA <文字>` | 生成自定义 BA logo 图片 | oiapi |
| `kfc` | 疯狂星期四文案（一次两条） | ahfi |
| `今天吃什么` | 随机推荐今天吃什么 | aa1 |
| `励志英语` | 每日励志英文名言 | zenquotes |
| `舔狗日记` | 随机一条日记 | 60s API |
| `骚话` | 随机一句话 | hitokoto |
| `弱智吧问答` | 随机一条弱智吧经典问答 | 内置语料 |
| `藏头诗 <文字>` | 生成藏头诗（最多4字） | 内置语料 |
| `运气 [星座]` | 抽今日运势签 | 内置语料 |
| `摸头 <QQ号>` | 生成 rua 头像 GIF | q.qlogo.cn + 本地合成 |
| `二次元图片` | 随机高清二次元图片 | dmoe.cc |
| `随机头像` | 随机动漫头像 | QQ 头像 |
| `猫猫图片` | 随机一张猫猫图片 | thecatapi |
| `必应壁纸 [偏移]` | 必应每日壁纸 | Bing 官方 |

画图类（`画图DALL·E-3` / `画图OpenAI`）需自备 API key。

## 给 Agent 接入

### 方式一：命令行调用（任何 Agent）

```bash
python3 tools/run_miniapp.py <仓库路径> <命令名> [参数]
```

输出 JSON：`{"ok": bool, "command": str, "text": str, "images": [url], "error": str}`

### 方式二：Hermes Agent 技能

配套技能 `xiaocx-miniapp-runner` 已封装调用流程，Agent 收到「抽个塔罗牌」「北京天气」类请求时自动触发。

## 安全特性

- ✅ 命令名白名单校验（拒绝路径分隔符、注入字符）
- ✅ 路径穿越双重防护（realpath 校验必须落在 `data/` 内）
- ✅ 参数以 argv 传递，不走 shell，无注入面
- ✅ 60 秒超时、结构化错误输出
- ✅ `sys.executable` 自适应解释器

⚠️ 仍请注意：`data/` 目录下的脚本会以当前用户权限执行，请勿放入来源不明的脚本。

## 目录结构

```
├── tools/run_miniapp.py   # 加固版运行器（核心入口）
├── data/                  # 小程序脚本（命令名=文件名）
├── legacy/qchatgpt-plugin/# 旧版 QChatGPT 插件适配层（可选）
└── requirements.txt
```

## 开发新小程序

1. 在 `data/` 新建 `<命令名>.py`
2. 文本输出直接 `print()`；图片输出 Markdown 格式 `![描述](https://...)`
3. 文本类参考 `天气.py`，图片类参考 `猫猫图片.py`
4. 无需注册，放进去就能用

## 上游与致谢

小程序创意与部分代码来自 [sanxianxiaohuntun/XiaocxPlugin](https://github.com/sanxianxiaohuntun/XiaocxPlugin)（v0.2）。本仓库完成了安全加固、失效 API 修复，并重构为 Agent 技能工具。
