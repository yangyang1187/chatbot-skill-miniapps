from pkg.plugin.context import register, handler, BasePlugin, APIHost, EventContext
from pkg.plugin.events import PersonNormalMessageReceived, GroupNormalMessageReceived
import subprocess
import os
import re
import sys
import asyncio
from mirai import Image, Plain

# 命令名只允许：字母/数字/下划线/中文/中点/连字符，禁止路径分隔符，防止目录穿越
SAFE_COMMAND_NAME = re.compile(r'^[\w·][\w·\-.]*$', re.UNICODE)


@register(name="小程序运行插件", description="一个小插件运行插件不必开关程序直接运行程序简单（可以用gpt直接写功能添加）", version="0.3", author="小馄饨")
class CommandExecutorPlugin(BasePlugin):
    lock = asyncio.Lock()  # 创建一个锁以确保串行执行
    command_queue = asyncio.Queue()  # 创建一个队列以存储待处理的命令
    TIMEOUT_SECONDS = 60  # 单个小程序的最长运行时间
    DATA_DIR = os.path.realpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data'))

    @handler(PersonNormalMessageReceived)
    async def person_normal_message_received(self, ctx: EventContext):
        await self.command_queue.put(ctx)  # 将命令上下文放入队列
        await self.process_commands()  # 处理命令

    @handler(GroupNormalMessageReceived)
    async def group_normal_message_received(self, ctx: EventContext):
        await self.command_queue.put(ctx)  # 将命令上下文放入队列
        await self.process_commands()  # 处理命令

    async def process_commands(self):
        # 只由持锁的一方消费队列，避免多个协程重复抢占同一条消息
        if self.lock.locked():
            return
        while not self.command_queue.empty():  # 当队列不为空时
            async with self.lock:  # 使用锁确保串行执行
                if self.command_queue.empty():
                    break
                ctx = await self.command_queue.get()  # 从队列中获取命令上下文
            await self.execute_command(ctx)  # 执行命令
            await asyncio.sleep(2)  # 等待 2 秒再处理下一条命令

    async def execute_command(self, ctx: EventContext):
        receive_text = ctx.event.text_message
        cleaned_text = re.sub(r'@\S+\s*', '', receive_text).strip()  # 清理文本

        if not cleaned_text.startswith('/'):  # 检查是否为命令
            return
        parts = cleaned_text[1:].split(' ', 1)  # 分割命令和参数
        command = parts[0]
        args = parts[1] if len(parts) > 1 else ''

        # 命令名白名单校验：拒绝空命令、路径分隔符、目录穿越字符
        if not command or not SAFE_COMMAND_NAME.match(command):
            ctx.add_return("reply", [f"非法命令名: {command}"])
            ctx.prevent_default()
            return

        script_path = os.path.realpath(os.path.join(self.DATA_DIR, f"{command}.py"))

        # 双重保险：解析后的真实路径必须仍在 data 目录内
        if not script_path.startswith(self.DATA_DIR + os.sep):
            ctx.add_return("reply", ["非法命令路径"])
            ctx.prevent_default()
            return

        if os.path.isfile(script_path):  # 检查脚本是否存在
            try:
                # 用当前解释器执行，避免硬编码的 'python' 在部分环境不存在
                result = subprocess.run(
                    [sys.executable, script_path, args],
                    capture_output=True,
                    text=True,
                    encoding='utf-8',
                    errors='replace',
                    timeout=self.TIMEOUT_SECONDS,
                )
                if result.returncode == 0:
                    messages = self.convert_message(result.stdout)  # 转换输出消息格式
                else:
                    messages = [f"执行失败: {result.stderr.strip() or result.stdout.strip()}"]
                ctx.add_return("reply", messages)  # 返回处理后的消息
            except subprocess.TimeoutExpired:
                ctx.add_return("reply", [f"执行超时（超过 {self.TIMEOUT_SECONDS} 秒）"])
            except Exception as e:
                ctx.add_return("reply", [f"发生错误: {str(e)}"])  # 返回通用错误消息
            ctx.prevent_default()  # 防止后续处理

    def convert_message(self, message):
        message = message.strip()
        if not message:
            return [Plain("（小程序没有输出任何内容）")]
        parts = []
        last_end = 0
        image_pattern = re.compile(r'!\[.*?\]\((https?://\S+)\)')  # 定义图像链接的正则表达式

        for match in image_pattern.finditer(message):  # 查找所有匹配的图像链接
            start, end = match.span()  # 获取匹配的起止位置
            if start > last_end:  # 如果有文本在图像之前
                parts.append(Plain(message[last_end:start]))  # 添加纯文本部分
            image_url = match.group(1)  # 提取图像 URL
            parts.append(Image(url=image_url))  # 添加图像消息
            last_end = end  # 更新最后位置
        if last_end < len(message):  # 如果还有剩余文本
            parts.append(Plain(message[last_end:]))  # 添加剩余的纯文本
        return parts if parts else [Plain(message)]  # 返回构建好的消息列表，如果没有部分则返回纯文本消息
