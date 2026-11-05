# Don't Remove Credit Tg - @VJ_Bots
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01

import os
import re
import sys
import json
import time
import asyncio
import requests
import subprocess

import core as helper
from utils import progress_bar
from vars import API_ID, API_HASH, BOT_TOKEN
from aiohttp import ClientSession
from pyromod import listen
from subprocess import getstatusoutput

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from pyrogram.errors.exceptions.bad_request_400 import MessageNotModified
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

bot = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@bot.on_message(filters.command(["start"]))
async def start(bot: Client, m: Message):
    await m.reply_text(f"<b>Hello {m.from_user.first_name}!</b>\n\nI am TXT File Video Downloader Bot.")

@bot.on_message(filters.command("stop"))
async def restart_handler(_, m):
    await m.reply_text("**Stopped** 🛑")
    os.execl(sys.executable, sys.executable, *sys.argv)

@bot.on_message(filters.command(["upload"]))
async def upload(bot: Client, m: Message):
    editable = await m.reply_text('**Send Your TXT File**')
    input: Message = await bot.listen(m.chat.id)
    if not input.document:
        await m.reply_text("**Kripya .txt file attach (📎) karke bhejein.**")
        return
    x = await input.download()
    await input.delete(True)

    path = f"./downloads/{m.chat.id}"

    try:
        with open(x, "r") as f:
            content = f.read()
        content = content.split("\n")
        links = []
        for line in content:
            line = line.strip()
            if not line:
                continue
            # Regex se link aur title alag karein (chahe beech me kitne bhi colons hon)
            match = re.search(r"^(.*?)(https?://.*)$", line)
            if match:
                raw_name = match.group(1).rstrip(":").strip()
                link_url = match.group(2).strip()
                links.append([raw_name, link_url])
            elif ":" in line:
                parts = line.rsplit(":", 1)
                links.append([parts[0].strip(), parts[1].strip()])
        os.remove(x)
    except Exception:
        await m.reply_text("**Invalid File Format**")
        if os.path.exists(x):
            os.remove(x)
        return

    await editable.edit(f"**TOTAL LINKS FOUND:** {len(links)}\n\nSend from where you want to download (e.g. 1)")
    input0: Message = await bot.listen(m.chat.id)
    raw_text = input0.text
    await input0.delete(True)

    await editable.edit("**Now Please Enter Batch Name / Caption Header**")
    input1: Message = await bot.listen(m.chat.id)
    raw_text0 = input1.text
    await input1.delete(True)

    await editable.edit("**ENTER RESOLUTION (144, 240, 360, 480, 720, 1080)**")
    input2: Message = await bot.listen(m.chat.id)
    raw_text2 = input2.text
    await input2.delete(True)
    try:
        if raw_text2 == "144":
            res = "256x144"
        elif raw_text2 == "240":
            res = "426x240"
        elif raw_text2 == "360":
            res = "640x360"
        elif raw_text2 == "480":
            res = "854x480"
        elif raw_text2 == "720":
            res = "1280x720"
        elif raw_text2 == "1080":
            res = "1920x1080"
        else:
            res = "UN"
    except Exception:
        res = "UN"

    await editable.edit("**Now Enter Author / Credit Name**")
    input3: Message = await bot.listen(m.chat.id)
    raw_text3 = input3.text
    await input3.delete(True)
    highlighter = f" "
    if raw_text3 == 'Robin':
        MR = highlighter
    else:
        MR = raw_text3

    await editable.edit("**Now send the Thumbnail URL or type 'no'**")
    input6 = await bot.listen(m.chat.id)
    raw_text6 = input6.text
    await input6.delete(True)
    await editable.delete()

    thumb = raw_text6.strip()
    if thumb.startswith("http://") or thumb.startswith("https://"):
        getstatusoutput(f"wget '{thumb}' -O 'thumb.jpg'")
        thumb = "thumb.jpg"
    else:
        thumb = "no"

    if len(links) == 1:
        count = 1
    else:
        count = int(raw_text)

    try:
        for i in range(count - 1, len(links)):
            url = links[i][1].strip()

            if "visionias" in url:
                async with ClientSession() as session:
                    async with session.get(url, headers={'User-Agent': 'Mozilla/5.0'}) as resp:
                        text = await resp.text()
                        url = re.search(r"(https://.*?playlist.m3u8.*?)\"", text).group(1)

            elif 'videos.classplusapp' in url:
                url = requests.get(f'https://api.classplusapp.com/cams/uploader/video/jw-signed-url?url={url}').json()['url']

            elif '/master.mpd' in url:
                id = url.split("/")[-2]
                url = f"https://d26g5bnklkwsh4.cloudfront.net/{id}/master.m3u8"

            name1 = links[i][0].replace("\t", "").replace(":", " - ").replace("/", "").replace("+", "").strip()
            clean_title = re.sub(r'[\\/*?:"<>|()]', "", name1).strip()
            if not clean_title:
                clean_title = f"File_{count}"
            name = f"{str(count).zfill(3)} - {clean_title}"

            headers_arg = '--user-agent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" --referer "https://web.classplusapp.com/"'

            if "youtu" in url:
                ytf = f"b[height<={raw_text2}][ext=mp4]/bv[height<={raw_text2}][ext=mp4]+ba[ext=m4a]/b[ext=mp4]"
                cmd = f'yt-dlp {headers_arg} --no-check-certificates -f "{ytf}" "{url}" -o "{name}.mp4"'
            elif "cloudfront.net" in url or ".m3u8" in url:
                cmd = f'yt-dlp {headers_arg} --no-check-certificates -f "bestvideo[height<={raw_text2}]+bestaudio/best[height<={raw_text2}]/best" "{url}" -o "{name}.mp4"'
            elif "jw-prod" in url:
                cmd = f'yt-dlp {headers_arg} --no-check-certificates -o "{name}.mp4" "{url}"'
            else:
                ytf = f"b[height<={raw_text2}]/bv[height<={raw_text2}]+ba/b/bv+ba"
                cmd = f'yt-dlp {headers_arg} --no-check-certificates -f "{ytf}" "{url}" -o "{name}.mp4"'

            try:
                cc = f'**[{str(count).zfill(3)}]** {clean_title}\n\n**Batch »** {raw_text0}\n**Uploaded By »** {MR}'
                cc1 = f'**[{str(count).zfill(3)}]** {clean_title}\n\n**Batch »** {raw_text0}\n**Uploaded By »** {MR}'

                if "drive" in url:
                    try:
                        ka = await helper.download(url, name)
                        copy = await bot.send_document(chat_id=m.chat.id, document=ka, caption=cc1)
                        count += 1
                        os.remove(ka)
                        time.sleep(1)
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue

                elif ".pdf" in url or "static.pw.live" in url:
                    try:
                        # Direct clean download for static PDFs
                        pdf_name = f"{name}.pdf"
                        r = requests.get(url, allow_redirects=True, timeout=60)
                        with open(pdf_name, "wb") as f_pdf:
                            f_pdf.write(r.content)

                        await bot.send_document(chat_id=m.chat.id, document=pdf_name, caption=cc1)
                        count += 1
                        if os.path.exists(pdf_name):
                            os.remove(pdf_name)
                        time.sleep(1)
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue
                    except Exception as err:
                        await m.reply_text(f"**PDF Download Error:** {str(err)}\n**Name:** {name}\n**Link:** `{url}`")
                        continue

                else:
                    Show = f"**⬇️ DOWNLOADING... »**\n\n**Name »** {name}\n**Quality »** {raw_text2}\n\n**URL »** {url}"
                    prog = await m.reply_text(Show)
                    res_file = await helper.download_video(url, cmd, name)
                    filename = str(res_file) if res_file else f"{name}.mp4"
                    if not os.path.exists(filename) and os.path.exists(f"{name}.mp4"):
                        filename = f"{name}.mp4"
                    await prog.delete(True)
                    await helper.send_vid(bot, m, cc, filename, thumb, name, prog)
                    count += 1
                    time.sleep(1)

            except Exception as e:
                await m.reply_text(
                    f"**downloading Interrupted**\n{str(e)}\n**Name »** {name}\n**Link »** `{url}`"
                )
                continue

    except Exception as e:
        await m.reply_text(str(e))

    await m.reply_text("**DONE Boss😎**")

bot.run()
