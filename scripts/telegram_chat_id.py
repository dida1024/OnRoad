import asyncio
import telegram
from telegram import Update

TOKEN = "8006898048:AAEHziOLj6IsuCp01ft_ysigLP-j_WemK-s"

async def print_latest_update():
    bot = telegram.Bot(TOKEN)
    async with bot:
        try:
            print("向群组里发条消息")
            updates = await bot.get_updates()
            if not updates:
                print("目前没有新的更新")
                return
            latest_update: Update = updates[-1]  # 获取最新的一条更新
            chat = latest_update.effective_chat
            message = latest_update.message
            print(f"最新消息来自 chat_id={chat.id}，chat_type={chat.type}")
            if message:
                print(f"消息内容：{message.text}")
            else:
                print("该更新没有消息内容")
        except Exception as e:
            print(f"获取更新时出错: {e}")

if __name__ == "__main__":
    asyncio.run(print_latest_update())
