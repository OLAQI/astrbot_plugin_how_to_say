from astrbot.api.event import AstrMessageEvent, filter, EventMessageType
from astrbot.api.star import Context, Star, register
from astrbot.types import MessageEventResult

# 1. 插件注册信息 (遵循命名规范)
@register("astrbot_plugin_how_to_say", "Your Name", "检测消息中的'怎么说'并调用 LLM 回复", "1.0.0")
class HowToSayPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    # 2. 使用事件监听器 (更通用，可以处理任何消息，不仅仅是指令)
    @filter.event_message_type(EventMessageType.ALL)
    async def on_message(self, event: AstrMessageEvent) -> MessageEventResult:
        """
        监听所有消息事件，如果消息中包含 "怎么说"，则调用 LLM。
        """
        message_str = event.message_str  # 获取消息纯文本

        if "怎么说" in message_str:
            # 3. 调用 LLM (确保已在 AstrBot 中启用并配置了 LLM)
            provider = self.context.get_using_provider()
            if provider:
                prompt = message_str.replace("怎么说", "").strip()  # 提取 "怎么说" 后面的内容作为 prompt
                if not prompt:
                    yield event.plain_result("请在'怎么说'后面加上你想表达的内容！")
                    return
                
                # 调用大语言模型
                response = await provider.text_chat(prompt, session_id=event.session_id)

                # 4. 处理 LLM 响应 (根据返回类型进行处理)
                if response.finish_reason == "FINISHED":  # 假设 LLM 正常返回
                    yield event.plain_result(response.completion_text)
                else:
                    yield event.plain_result("抱歉，LLM 没有给出合适的回答。")
            else:
                yield event.plain_result("请先启用并配置大语言模型！")
