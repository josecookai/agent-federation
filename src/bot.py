# Agent Federation Bot - P0 MVP

import os
import yaml
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from dotenv import load_dotenv

# 导入本地模块
from digest import DigestGenerator
from agent import AgentRegistry

load_dotenv()

# 配置
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GROUP_ID = os.getenv("TELEGRAM_GROUP_ID")
AGENT_ID = os.getenv("AGENT_ID", "eva@smrti-lab")
AGENT_NAME = os.getenv("AGENT_NAME", "Eva")
AGENT_COMPANY = os.getenv("AGENT_COMPANY", "Smrti Lab")

class FederationBot:
    def __init__(self):
        self.registry = AgentRegistry("agents/registry.yaml")
        self.digest_gen = DigestGenerator(AGENT_ID, AGENT_NAME, AGENT_COMPANY)
        
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """欢迎消息"""
        welcome = f"""
🤖 **Agent Federation Bot - P0**

我是 {AGENT_NAME} (@{AGENT_ID})
来自 {AGENT_COMPANY}

可用命令:
/digest - 发布今日日报
/agents - 列出联邦中的Agents
/hello - 打招呼
/help - 帮助

*Built with OpenClaw*
        """
        await update.message.reply_text(welcome, parse_mode="Markdown")
    
    async def post_digest(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """发布日报 - 从 memory 文件自动生成"""
        await update.message.reply_text("🔄 正在生成日报...")
        
        # 使用 DigestGenerator 从 memory 生成
        digest = self.digest_gen.generate_eva_daily_digest()
        
        # 格式化输出
        message = self._format_digest(digest.to_dict())
        await update.message.reply_text(message, parse_mode="Markdown")
        
    def _format_digest(self, digest: dict) -> str:
        """格式化日报为 Telegram 消息"""
        msg = f"""📊 **{digest['name']} 日报**
🏢 {digest['company']} | 🆔 {digest['agent_id']}
⏰ {digest['timestamp'][:10]}

📋 **摘要**: {digest['summary']}

✅ **完成任务**: {digest['tasks_completed']}
"""
        if digest['highlights']:
            msg += f"\n🔥 **亮点**:\n" + "\n".join(f"• {h}" for h in digest['highlights'])
        
        if digest['skills_showcase']:
            msg += f"\n\n🛠️ **技能展示**:\n" + "\n".join(f"• {s}" for s in digest['skills_showcase'])
            
        if digest['open_questions']:
            msg += f"\n\n❓ **开放问题**:\n" + "\n".join(f"• {q}" for q in digest['open_questions'])
            
        msg += "\n\n`#AgentFederation #DailyDigest`"
        return msg
    
    async def list_agents(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """列出联邦中的 Agents"""
        try:
            with open("agents/registry.yaml", 'r') as f:
                data = yaml.safe_load(f)
                agents = data.get('agents', [])
        except:
            agents = []
        
        msg = "🌐 **Agent Federation 成员**:\n\n"
        
        if not agents:
            msg += "暂无成员\n"
        else:
            for agent in agents:
                msg += f"🤖 **{agent['name']}** ({agent['company']})\n"
                msg += f"   🆔 `@{agent['id']}`\n"
                msg += f"   📍 {agent.get('location', 'Unknown')}\n"
                if agent.get('skills'):
                    skills = ', '.join(agent['skills'][:3])
                    msg += f"   🛠️ {skills}\n"
                msg += "\n"
        
        # 添加 pending
        try:
            with open("agents/registry.yaml", 'r') as f:
                data = yaml.safe_load(f)
                pending = data.get('pending', [])
                if pending:
                    msg += "⏳ **等待加入**:\n"
                    for p in pending:
                        msg += f"• {p['name']} ({p['company']})\n"
        except:
            pass
        
        await update.message.reply_text(msg, parse_mode="Markdown")
    
    async def hello(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """打招呼 - 展示个性"""
        greetings = [
            f"你好！我是 {AGENT_NAME}，来自 {AGENT_COMPANY}。",
            f"👋 {AGENT_NAME} 报道！今天有什么可以协作的吗？",
            f"嗨！{AGENT_COMPANY} 的 {AGENT_NAME} 在此。",
        ]
        import random
        await update.message.reply_text(random.choice(greetings))
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """帮助"""
        help_text = """
🤖 **Agent Federation Bot 命令**:

/digest - 发布今日日报
/agents - 查看联邦成员列表
/hello - 打招呼
/help - 显示帮助

💡 **提示**:
• 在群里 @我 可以提问
• 使用 /digest 分享你的工作
• 查看别人的日报了解协作机会
        """
        await update.message.reply_text(help_text, parse_mode="Markdown")
    
    async def handle_mention(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """处理被 @ 的情况"""
        if f"@{context.bot.username}" in update.message.text:
            await update.message.reply_text(
                f"👋 被提到了！我是 {AGENT_NAME}。\n"
                f"试试用 /help 查看我能做什么。"
            )

def main():
    bot = FederationBot()
    
    # 创建应用
    application = Application.builder().token(BOT_TOKEN).build()
    
    # 添加处理器
    application.add_handler(CommandHandler("start", bot.start))
    application.add_handler(CommandHandler("digest", bot.post_digest))
    application.add_handler(CommandHandler("agents", bot.list_agents))
    application.add_handler(CommandHandler("hello", bot.hello))
    application.add_handler(CommandHandler("help", bot.help_command))
    
    # 处理 @ 提及
    application.add_handler(MessageHandler(filters.TEXT & filters.Entity("mention"), bot.handle_mention))
    
    # 启动
    print(f"🤖 {AGENT_NAME} 启动中...")
    print(f"📡 监控群组: {GROUP_ID}")
    application.run_polling()

if __name__ == "__main__":
    main()