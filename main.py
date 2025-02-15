import logging
from astrbot.api.star import Context, Star, register
from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.event.filter import event_message_type, EventMessageType
from astrbot.api.provider import ProviderRequest

# 获取当前模块 logger
logger = logging.getLogger(__name__)

@register("how_to_say", "olaqi", "一个怎么说插件", "1.1.3", "https://github.com/OLAQI/astrbot_plugin_how_to_say")
class CrazyThursdayPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    @event_message_type(EventMessageType.ALL)
    async def on_message(self, event: AstrMessageEvent) -> MessageEventResult:
        """
        当消息中包含“怎么说”时调用 LLM 大模型来回答。
        """
        msg_obj = event.message_obj

        text = msg_obj.message_str or ""

        logger.debug("=== Debug: AstrBotMessage ===")
        logger.debug("Bot ID: %s", msg_obj.self_id)
        logger.debug("Session ID: %s", msg_obj.session_id)
        logger.debug("Message ID: %s", msg_obj.message_id)
        logger.debug("Sender: %s", msg_obj.sender)
        logger.debug("Group ID: %s", msg_obj.group_id)
        logger.debug("Message Chain: %s", msg_obj.message)
        logger.debug("Raw Message: %s", msg_obj.raw_message)
        logger.debug("Timestamp: %s", msg_obj.timestamp)
        logger.debug("============================")

        if "怎么说" in text:
            # 获取 LLM 提供商
            provider = self.context.get_using_provider()
            if provider:
                try:
                    # 添加自定义的系统提示，使回复语气非常拽
                    custom_system_prompt = "你是一个非常拽的人，说话方式非常直接和强势。"
                    response = await provider.text_chat(text, session_id=event.session_id, system_prompt=custom_system_prompt)
                    result_text = response.completion_text
                except Exception as e:
                    result_text = f"获取信息失败: {e}"
            else:
                result_text = "LLM 未启用，请联系管理员。"

            yield event.plain_result(result_text)
