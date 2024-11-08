from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import Activity
from aiohttp import web
import asyncio

class SimpleChatbot(ActivityHandler):
    def __init__(self):
        self.introduction = "Hello! I'm a simple chatbot. How can I assist you today?"

    async def on_message_activity(self, turn_context: TurnContext):
        user_input = turn_context.activity.text.strip().lower()

        if "capabilities" in user_input:
            await turn_context.send_activity("Here are my capabilities: I can answer questions about my capabilities, respond to greetings, and assist with common inquiries.")
        elif "hello" in user_input or "hi" in user_input:
            await turn_context.send_activity("Hi there! How can I help you?")
        elif "bye" in user_input:
            await turn_context.send_activity("Goodbye! Have a nice day!")
        else:
            await turn_context.send_activity("I'm sorry, I didn't understand that. Could you please rephrase?")

async def main():
    app = web.Application()
    bot = SimpleChatbot()

    async def handle_messages(req):
        body = await req.json()
        activity = Activity().deserialize(body)
        auth_header = req.headers.get("Authorization", "")
        await bot.on_turn(TurnContext(bot, activity), auth_header)
        return web.Response(status=201)

    app.router.add_post("/api/messages", handle_messages)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "localhost", 3978)
    await site.start()
    print("Bot is running on http://localhost:3978/api/messages")

if __name__ == "__main__":
    asyncio.run(main())