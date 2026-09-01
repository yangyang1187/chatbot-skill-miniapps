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
| `轮盘赌 [继续]` | 左轮轮盘赌（6 弹仓 1 子弹，可继续扣扳机） | 内置逻辑 |
| `明日方舟十连 [次数]` | 明日方舟寻访模拟（1-60 连，标准池概率） | 内置语料 |
| `搜图 <图片URL>` | 以图搜图，返回番剧标题/集数/相似度与命中画面 | trace.moe / saucenao |
| `pixiv图 <ID或URL> [页码]` | 查询 Pixiv 插画（标题/作者/标签/原图，多页可翻页） | pixiv ajax + i.pixiv.re 反代 |
| `B站直播 <房间号>` | 查询 B 站直播间状态/分区/人气（直播中附画面截图） | bilibili API |

> 💡 聊天里用搜图：qqBot 式「回复图片+输入搜图」的等价做法是——Agent 看到对话中被回复/附带的图片后，
> 把图片 URL 作为参数传给 `搜图 <图片URL>` 即可，效果相同。

画图类需自备 API key（未配置时会提示缺什么）：
- `画图DALL·E-3` → 环境变量 `DALLE_API_KEY` + `DALLE_API_URL`
- `画图OpenAI` → 环境变量 `OPENAI_API_HOST` + `OPENAI_API_KEY`
- `画图ideogram版` → 环境变量 `IDEOGRAM_API_URL` + `IDEOGRAM_API_KEY`
- `搜图` 的 saucenao 备选源 → 环境变量 `SAUCENAO_API_KEY`（不配置也能用免 key 的 trace.moe）
- `pixiv图` → 环境变量 `PIXIV_PHPSESSID`（可选，看 R-18 作品时需要；公开作品不用配）

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

## 多源容灾（自动 fallback）

每个命令配置 2-3 个数据源，按顺序自动切换，主源挂了用户无感知：

| 命令 | 源 1 | 源 2 | 源 3 |
|---|---|---|---|
| 天气 | alapi(需token) | wttr.in | open-meteo |
| 猫猫图片 | thecatapi | cataas | - |
| 二次元图片 | dmoe | jitsu | - |
| 随机头像 | q.qlogo | jitsu | - |
| 必应壁纸 | Bing 官方 | biturl 镜像 | - |
| 励志英语 | zenquotes | qqsuu | - |
| 舔狗日记 | 60s API | qqsuu | - |
| 骚话 | hitokoto | 60s 一言 | - |
| 今天吃什么 | aa1 | - | 本地菜库 |
| kfc | ahfi | qqsuu | 本地语料 |
| 塔罗牌 | oiapi | - | 本地22张大阿卡纳 |
| 色图(搜图) | safebooru | jitsu | dmoe |
| 搜图(以图搜图) | trace.moe | saucenao(需key) | - |
| B站直播 | Room/get_info | Room/room_playing | - |
| pixiv图 | pixiv ajax(公开作品免登录) | i.pixiv.re 反代 | i.pixiv.cat 反代 |

文本类命令（弱智吧问答/藏头诗/运气/摸头/轮盘赌/明日方舟十连）为纯本地实现，天然永不失效。
公共库：`data/_multisource.py`，新增数据源只需加一个函数进 `try_sources` 列表。

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
