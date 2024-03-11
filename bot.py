
import discord
from discord.ext import commands
import asyncio
from openai import OpenAI
import time


intents = discord.Intents.default() # Подключаем "Разрешения"
intents.message_content = True

# Задаём префикс и интенты
bot = commands.Bot(command_prefix='/', intents=intents) 

# С помощью декоратора создаём первую команду
@bot.command()
async def start(ctx):
    await ctx.send('Привет👋 Напиши: /prompt, а я дам ответ🦾')



@bot.command()
async def prompt(ctx):
    await ctx.send('Введите вопрос который хотите задать...')

    def check(message):
        return message.author == ctx.author

    try:
        response = await bot.wait_for('message', check=check, timeout=60)
        msg = await ctx.reply('Принято 🫡')

        client = OpenAI(api_key="token", base_url="https://api.deepseek.com/v1")

        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": response.content + "Напиши ответ  обязательно на русском и без сложных слов"},
                {"role": "user", "content":  response.content + "Напиши ответ  обязательно на русском и без сложных слов"},
            ]
        )

        responce = response.choices[0].message.content

        await msg.delete()
        await ctx.send(responce)
    except asyncio.TimeoutError:
        await ctx.send('Вы не ввели текст вовремя💥')


bot.run("token")
