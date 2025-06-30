import discord
from discord.ext import commands
import asyncio
import random
import os
from keep_alive import keep_alive
keep_alive()
# إعداد الصلاحيات
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.members = True

# إنشاء البوت
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")


# تحويل الوقت من صيغة مثل "10s" إلى ثواني
def convert_time(time_str):
    units = {"s": 1, "m": 60, "h": 3600, "d": 86400}
    try:
        return int(time_str[:-1]) * units[time_str[-1]]
    except:
        return -1


# أمر الجيف أواي
@bot.command(name="سحب")
async def giveaway(ctx, *, args):
    try:
        if "على" in args and "خلال" in args:
            parts = args.split("خلال")
            prize = parts[0].replace("على", "").strip()
            time = parts[1].strip()
        else:
            await ctx.send(
                "❌ الصيغة غير صحيحة. استخدم: `!سحب على (الجائزة) خلال (الوقت)`"
            )
            return
    except:
        await ctx.send("❌ حدث خطأ في قراءة الأمر.")
        return
    duration = convert_time(time)
    if duration == -1:
        await ctx.send(
            "❌ صيغة الوقت غير صحيحة. استخدم مثل: `10s`, `2m`, `1h`, `1d`")
        return

    # إرسال رسالة Embed للجيف أواي
    embed = discord.Embed(
        title="سحب مميز 🎊",
        description=(f"⚫ **الجائزة:** {prize}\n"
                     f"⚫ **المدة:** {time}\n"
                     f"⚫ للمشاركة: اضغط على 🎉 أسفل هذه الرسالة\n"
                     f"⚫ سيتم اختيار فائز تلقائيًا عند انتهاء الوقت"),
        color=0xE74C3C)

    msg = await ctx.send(embed=embed)
    await msg.add_reaction("🎉")

    # انتظار انتهاء الوقت
    await asyncio.sleep(duration)

    # إعادة تحميل الرسالة بعد الانتظار
    msg = await ctx.channel.fetch_message(msg.id)

    # جمع المستخدمين الذين تفاعلوا
    users = []
    async for user in msg.reactions[0].users():
        if not user.bot:
            users.append(user)

    if len(users) == 0:
        await ctx.send("❌ لم يشارك أحد.")
    else:
        winner = random.choice(users)
        await ctx.send(
            f"🎉 تهانينا {winner.mention}!\n"
            f"لقد ربحت الجائزة الرائعة: **{prize}** 🎁\n"
            f"استمتع بالجائزة ونتمنى لك حظًا أوفر للجميع في المرات القادمة! 🍀")


# تشغيل البوت باستخدام التوكن من Secrets
bot.run(os.environ['TOKEN'])
