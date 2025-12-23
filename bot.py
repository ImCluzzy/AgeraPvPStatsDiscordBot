import discord
from discord import app_commands
from discord.ext import commands
import os
import asyncio
import logging
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

from core.api_client import AgeraPvPAPI
from generators import (
    StatsImageGenerator,
    ProfileImageGenerator,
    PunishmentsImageGenerator
)

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
API_KEY = os.getenv('API_KEY')

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден в переменных окружения! Создайте файл .env с токеном.")

if not API_KEY:
    raise ValueError("API_KEY не найден в переменных окружения! Создайте файл .env с API ключом.")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

api_client = AgeraPvPAPI(api_key=API_KEY)
stats_formatter = StatsImageGenerator()
profile_generator = ProfileImageGenerator()
punishments_generator = PunishmentsImageGenerator()


@bot.event
async def on_ready():
    print(f'Бот {bot.user} подключен к Discord!')
    
    try:
        synced = await bot.tree.sync()
        print(f'Синхронизировано {len(synced)} команд')
    except Exception as e:
        print(f'Ошибка при синхронизации команд: {e}')
    
    logger = logging.getLogger('bot')
    if api_client.test_connection():
        logger.info('Соединение с API установлено')
    else:
        logger.warning('Не удалось подключиться к API. Проверьте логи выше для деталей.')


@bot.tree.command(name="stats", description="Получить статистику игрока")
@app_commands.describe(
    nickname="Никнейм игрока",
    mode="Режим игры (BW для BedWars или Duels)"
)
async def stats_command(interaction: discord.Interaction, nickname: str, mode: str):
    try:
        await interaction.response.defer()
    except (discord.errors.NotFound, discord.errors.InteractionResponded) as e:
        print(f"Ошибка при defer в команде stats: {e}")
        return
    
    try:
        loop = asyncio.get_event_loop()
        stats_data = await loop.run_in_executor(None, api_client.get_player_stats, nickname, mode)
        
        if stats_data is None:
            await interaction.followup.send(
                f"❌ Не удалось получить статистику для игрока **{nickname}** в режиме **{mode.upper()}**.\n"
                "Проверьте правильность ника и режима."
            )
            return
        
        if isinstance(stats_data, dict):
            if not stats_data.get('success', True):
                error_msg = stats_data.get('message', 'Неизвестная ошибка')
                await interaction.followup.send(
                    f"❌ Ошибка: {error_msg}"
                )
                return
        
        rank = None
        profile_data = await loop.run_in_executor(None, api_client.get_player_profile, nickname)
        if profile_data and isinstance(profile_data, dict):
            ranks = profile_data.get('ranks', [])
            if ranks and isinstance(ranks, list) and len(ranks) > 0:
                first_rank = ranks[0]
                if isinstance(first_rank, dict):
                    rank = first_rank.get('name') or first_rank.get('displayName')
                elif isinstance(first_rank, str):
                    rank = first_rank
                
                if rank:
                    import re
                    rank = re.sub(r'§[0-9a-fA-Fk-oK-OrR]', '', rank)
        
        image_bytes = await loop.run_in_executor(
            None, 
            stats_formatter.generate, 
            nickname, 
            mode, 
            stats_data, 
            rank
        )
        
        if image_bytes is None:
            await interaction.followup.send(
                f"❌ Не удалось сгенерировать изображение со статистикой."
            )
            return
        
        file = discord.File(image_bytes, filename=f"stats_{nickname}_{mode}.png")
        await interaction.followup.send(
            f"📊 Статистика игрока **{nickname}** в режиме **{mode.upper()}**",
            file=file
        )
        
    except Exception as e:
        print(f"Ошибка в команде stats: {e}")
        await interaction.followup.send(
            f"❌ Произошла ошибка при обработке запроса: {str(e)}"
        )


@bot.tree.command(name="profile", description="Получить профиль игрока")
@app_commands.describe(
    nickname="Никнейм игрока"
)
async def profile_command(interaction: discord.Interaction, nickname: str):
    await interaction.response.defer()
    
    try:
        profile_data = api_client.get_player_profile(nickname)
        
        if profile_data is None:
            await interaction.followup.send(
                f"❌ Не удалось получить профиль для игрока **{nickname}**.\n"
                "Проверьте правильность ника."
            )
            return
        
        if isinstance(profile_data, dict):
            if not profile_data.get('success', True):
                error_msg = profile_data.get('message', 'Неизвестная ошибка')
                await interaction.followup.send(
                    f"❌ Ошибка: {error_msg}"
                )
                return
        
        image_bytes = profile_generator.generate(nickname, profile_data)
        
        if image_bytes is None:
            await interaction.followup.send(
                f"❌ Не удалось сгенерировать изображение профиля."
            )
            return
        
        file = discord.File(image_bytes, filename=f"profile_{nickname}.png")
        await interaction.followup.send(
            f"👤 Профиль игрока **{nickname}**",
            file=file
        )
        
    except Exception as e:
        print(f"Ошибка в команде profile: {e}")
        await interaction.followup.send(
            f"❌ Произошла ошибка при обработке запроса: {str(e)}"
        )


@bot.tree.command(name="punishments", description="Получить статистику наказаний")
async def punishments_command(interaction: discord.Interaction):
    await interaction.response.defer()
    
    try:
        stats_data = api_client.get_staff_stats()
        
        if stats_data is None:
            await interaction.followup.send(
                "❌ Не удалось получить статистику наказаний."
            )
            return
        
        if isinstance(stats_data, dict):
            if not stats_data.get('success', True):
                error_msg = stats_data.get('message', 'Неизвестная ошибка')
                await interaction.followup.send(
                    f"❌ Ошибка: {error_msg}"
                )
                return
        
        image_bytes = punishments_generator.generate(stats_data)
        
        if image_bytes is None:
            await interaction.followup.send(
                "❌ Не удалось сгенерировать изображение статистики наказаний."
            )
            return
        
        file = discord.File(image_bytes, filename="punishments.png")
        await interaction.followup.send(
            "📊 Статистика наказаний",
            file=file
        )
        
    except Exception as e:
        print(f"Ошибка в команде punishments: {e}")
        await interaction.followup.send(
            f"❌ Произошла ошибка при обработке запроса: {str(e)}"
        )


@bot.tree.command(name="staff", description="Получить список онлайн стаффа")
async def staff_command(interaction: discord.Interaction):
    try:
        await interaction.response.defer()
    except (discord.errors.NotFound, discord.errors.InteractionResponded) as e:
        print(f"Ошибка при defer в команде staff: {e}")
        return
    
    try:
        loop = asyncio.get_event_loop()
        staff_data = await loop.run_in_executor(None, api_client.get_staff_online)
        
        if staff_data is None:
            await interaction.followup.send(
                "❌ Не удалось получить список онлайн стаффа."
            )
            return
        
        if isinstance(staff_data, dict):
            if not staff_data.get('success', True):
                error_msg = staff_data.get('message', 'Неизвестная ошибка')
                await interaction.followup.send(
                    f"❌ Ошибка: {error_msg}"
                )
                return
        
        players = staff_data.get('players', [])
        
        if len(players) == 0:
            await interaction.followup.send(
                "👮 **Онлайн стафф**\n\nНет онлайн стаффа"
            )
            return
        
        import re
        lines = [f"👮 **Онлайн стафф ({len(players)})**", ""]
        
        for i, player in enumerate(players, 1):
            display_name = player.get('displayName', 'Неизвестно')
            user_id = player.get('userId', 'N/A')
            
            display_name = re.sub(r'§[0-9a-fA-Fk-oK-OrR]', '', display_name)
            
            lines.append(f"{i}. **{display_name}** (ID: {user_id})")
        
        message = "\n".join(lines)
        await interaction.followup.send(message)
        
    except Exception as e:
        print(f"Ошибка в команде staff: {e}")
        await interaction.followup.send(
            f"❌ Произошла ошибка при обработке запроса: {str(e)}"
        )


@bot.tree.command(name="online", description="Получить общее количество онлайн игроков")
async def online_command(interaction: discord.Interaction):
    try:
        await interaction.response.defer()
    except (discord.errors.NotFound, discord.errors.InteractionResponded) as e:
        print(f"Ошибка при defer в команде online: {e}")
        return
    
    try:
        loop = asyncio.get_event_loop()
        online_data = await loop.run_in_executor(None, api_client.get_total_online)
        
        if online_data is None:
            await interaction.followup.send(
                "❌ Не удалось получить количество онлайн игроков."
            )
            return
        
        if isinstance(online_data, dict):
            if not online_data.get('success', True):
                error_msg = online_data.get('message', 'Неизвестная ошибка')
                await interaction.followup.send(
                    f"❌ Ошибка: {error_msg}"
                )
                return
        
        online_count = 0
        if isinstance(online_data, dict):
            online_count = online_data.get('online') or online_data.get('count') or 0
        elif isinstance(online_data, (int, float)):
            online_count = online_data
        
        await interaction.followup.send(
            f"👥 Онлайн игроков: **{online_count}**"
        )
        
    except Exception as e:
        print(f"Ошибка в команде online: {e}")
        await interaction.followup.send(
            f"❌ Произошла ошибка при обработке запроса: {str(e)}"
        )


@bot.tree.command(name="test", description="Проверить соединение с API")
async def test_command(interaction: discord.Interaction):
    await interaction.response.defer()
    
    is_connected = api_client.test_connection()
    
    if is_connected:
        await interaction.followup.send("✅ Соединение с API установлено!")
    else:
        await interaction.followup.send("❌ Не удалось подключиться к API")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    print(f"Ошибка команды: {error}")


def main():
    if not BOT_TOKEN:
        print("Ошибка: BOT_TOKEN не установлен!")
        print("Создайте файл .env и добавьте туда: BOT_TOKEN=ваш_токен")
        return
    
    if not API_KEY:
        print("Ошибка: API_KEY не установлен!")
        print("Создайте файл .env и добавьте туда: API_KEY=ваш_api_ключ")
        return
    
    try:
        bot.run(BOT_TOKEN)
    except discord.LoginFailure:
        print("Ошибка: Неверный токен бота!")
    except Exception as e:
        print(f"Ошибка при запуске бота: {e}")


if __name__ == "__main__":
    main()