# Don't Remove Credit Tg - @VJ_Bots
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

import os
import asyncio 
import pyrogram
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated, UserAlreadyParticipant, InviteHashExpired, UsernameNotOccupied
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message 
from config import API_ID, API_HASH, ERROR_MESSAGE, LOGIN_SYSTEM, STRING_SESSION, CHANNEL_ID, WAITING_TIME
from database.db import db
from TechVJ.strings import HELP_TXT
from bot import TechVJUser

class batch_temp(object):
    IS_BATCH = {}
    STATE = {}
    DATA = {}

async def downstatus(client, statusfile, message, chat):
    while True:
        if os.path.exists(statusfile):
            break

        await asyncio.sleep(3)
      
    while os.path.exists(statusfile):
        with open(statusfile, "r") as downread:
            txt = downread.read()
        try:
            await client.edit_message_text(
    chat,
    message.id,
    f"📥 Downloading...\n\n<pre>{txt}</pre>",
    parse_mode=enums.ParseMode.HTML
			)
            await asyncio.sleep(10)
        except:
            await asyncio.sleep(5)


# upload status
async def upstatus(client, statusfile, message, chat):
    while True:
        if os.path.exists(statusfile):
            break

        await asyncio.sleep(3)      
    while os.path.exists(statusfile):
        with open(statusfile, "r") as upread:
            txt = upread.read()
        try:
            await client.edit_message_text(
    chat,
    message.id,
    f"📤 Uploading...\n\n<pre>{txt}</pre>",
    parse_mode=enums.ParseMode.HTML
			)
            await asyncio.sleep(10)
        except:
            await asyncio.sleep(5)


# progress writer
import time

# ultra premium progress bar
def progress(current, total, message, type):

    percentage = current * 100 / total

    speed = current / (time.time() - getattr(message, "_start_time", time.time()) + 1)

    speed_mb = speed / 1024 / 1024


    remaining = (total - current) / speed if speed > 0 else 0

    mins, secs = divmod(int(remaining), 60)

    current_size = current / 1024 / 1024
    total_size = total / 1024 / 1024

    completed = int(percentage / 10)
    remaining_bar = 10 - completed

    progress_bar = (
        "🟩" * completed +
        "⬜" * remaining_bar
    )

    status = f"""
╭━━━〔 ⚡ ULTRA PREMIUM ⚡ 〕━━━╮

📦 Size : {current_size:.2f} / {total_size:.2f} MB
🚀 Speed : {speed_mb:.2f} MB/s
⏳ ETA : {mins:02d}:{secs:02d}

┣━━━━━━━━━━━━━━━━━━━━━━━┫
┃ {progress_bar} {percentage:.1f}% ┃
┣━━━━━━━━━━━━━━━━━━━━━━━┫

🔥 Status : {"Downloading" if type == "down" else "Uploading"}

╰━━━━━━━━━━━━━━━━━━━━━━━╯
"""

    with open(f"{message.id}{type}status.txt", "w", encoding="utf-8") as f:
        f.write(status)


# start command
@Client.on_message(filters.command(["start"]))
async def send_start(client: Client, message: Message):
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id, message.from_user.first_name)
    buttons = [[
        InlineKeyboardButton("❣️ Developer", url = "https://t.me/vipinkk798")
    ],[
        InlineKeyboardButton('📌 sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ', url='https://t.me/+TZcsQ-tSOLZmZmI1'),
        InlineKeyboardButton('♦️ ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ', url='https://t.me/+HDMluvw5V6Y2ZWI1')
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    await client.send_message(
        chat_id=message.chat.id, 
        text=f"""<b>
✨ Welcome {message.from_user.mention} ✨

╭──────────────────╮
  🚀 Save Restricted Bot
╰──────────────────╯

🔓 Download Restricted Content
⚡ Fast & Secure Processing
📥 Supports Private Channels
🎬 Videos • Photos • Documents

━━━━━━━━━━━━━━━━━━

📌 How To Use:

1️⃣ Send Any Telegram Post Link
2️⃣ Login Using /login
3️⃣ Get File Instantly

🆘 Need Help? Use /help

━━━━━━━━━━━━━━━━━━
💎 Powered By @vipinkk798
</b>""",
        reply_markup=reply_markup, 
        reply_to_message_id=message.id
    )
    return


# help command
@Client.on_message(filters.command(["help"]))
async def send_help(client: Client, message: Message):
    await client.send_message(
        chat_id=message.chat.id, 
        text=f"{HELP_TXT}"
    )

@Client.on_message(filters.command("batch"))
async def batch_cmd(client: Client, message: Message):

    uid = message.from_user.id

    batch_temp.STATE[uid] = "WAIT_START_LINK"
    batch_temp.IS_BATCH[uid] = True

    await message.reply_text(
    "📌 Send START post link"
	)

# cancel command
@Client.on_message(filters.command(["cancel"]))
async def send_cancel(client: Client, message: Message):
    batch_temp.IS_BATCH[message.from_user.id] = True
    await client.send_message(
        chat_id=message.chat.id, 
        text="**Batch Successfully Cancelled.**"
    )

@Client.on_message(filters.text & filters.private)
async def save(client: Client, message: Message):

    uid = message.from_user.id
    state = batch_temp.STATE.get(uid)

    # STEP 1
    if state == "WAIT_START_LINK":

        batch_temp.DATA[uid] = {
            "start_link": message.text
        }

        batch_temp.STATE[uid] = "WAIT_COUNT"

        return await message.reply_text(
            "⏳ Send number of files"
        )

    # STEP 2
    if state == "WAIT_COUNT":

        try:
            count = int(message.text)

        except:
            return await message.reply_text(
                "❌ Invalid number"
            )

        start_link = batch_temp.DATA[uid]["start_link"]

        batch_temp.STATE[uid] = None

        datas = start_link.split("/")

        temp = datas[-1].replace("?single","").split("-")

        fromID = int(temp[0].strip())

        toID = fromID + count - 1

        message.text = start_link
    # Joining chat
    if ("https://t.me/+" in message.text or "https://t.me/joinchat/" in message.text) and LOGIN_SYSTEM == False:
        if TechVJUser is None:
            await client.send_message(message.chat.id, "String Session is not Set", reply_to_message_id=message.id)
            return
        try:
            try:
                await TechVJUser.join_chat(message.text)
            except Exception as e: 
                await client.send_message(message.chat.id, f"Error : {e}", reply_to_message_id=message.id)
                return
            await client.send_message(message.chat.id, "Chat Joined", reply_to_message_id=message.id)
        except UserAlreadyParticipant:
            await client.send_message(message.chat.id, "Chat already Joined", reply_to_message_id=message.id)
        except InviteHashExpired:
            await client.send_message(message.chat.id, "Invalid Link", reply_to_message_id=message.id)
        return
    
    if "https://t.me/" in message.text:

        if batch_temp.IS_BATCH.get(message.from_user.id, True) == False:
            return await message.reply_text(
                "**One Task Is Already Processing. Wait For Complete It. If You Want To Cancel This Task Then Use - /cancel**"
            )

        datas = message.text.split("/")
        temp = datas[-1].replace("?single","").split("-")

        fromID = int(temp[0].strip())

        if state != "WAIT_COUNT":
            count = 1

        if LOGIN_SYSTEM == True:

            user_data = await db.get_session(message.from_user.id)

            if user_data is None:
                await message.reply(
                    "**For Downloading Restricted Content You Have To /login First.**"
                )
                return

            api_id = int(await db.get_api_id(message.from_user.id))
            api_hash = await db.get_api_hash(message.from_user.id)

            try:
                acc = Client(
                    "saverestricted",
                    session_string=user_data,
                    api_hash=api_hash,
                    api_id=api_id
                )

                await acc.connect()

            except:
                return await message.reply(
                    "**Your Login Session Expired. So /logout First Then Login Again By - /login**"
                )

        else:

            if TechVJUser is None:
                await client.send_message(
                    message.chat.id,
                    "**String Session is not Set**",
                    reply_to_message_id=message.id
                )
                return

            acc = TechVJUser

        batch_temp.IS_BATCH[message.from_user.id] = False

remaining = count

        for msgid in range(fromID, fromID + count):

            if batch_temp.IS_BATCH.get(message.from_user.id):
                break

            # private
            if "https://t.me/c/" in message.text:

                chatid = int("-100" + datas[4])

                try:
                    await handle_private(
                        client,
                        acc,
                        message,
                        chatid,
                        msgid
                    )

                except Exception as e:

                    if ERROR_MESSAGE == True:
                        await client.send_message(
                            message.chat.id,
                            f"Error: {e}",
                            reply_to_message_id=message.id
                        )

            # bot
            elif "https://t.me/b/" in message.text:

                username = datas[4]

                try:
                    await handle_private(
    client,
    acc,
    message,
    chatid,
    msgid,
    remaining
)

remaining -= 1

                except Exception as e:

                    if ERROR_MESSAGE == True:
                        await client.send_message(
                            message.chat.id,
                            f"Error: {e}",
                            reply_to_message_id=message.id
                        )

            # public
            else:

                username = datas[3]

                try:
                    msg = await client.get_messages(username, msgid)

                except UsernameNotOccupied:

                    await client.send_message(
                        message.chat.id,
                        "The username is not occupied by anyone",
                        reply_to_message_id=message.id
                    )

                    return

                try:

                    await client.copy_message(
                        message.chat.id,
                        msg.chat.id,
                        msg.id,
                        reply_to_message_id=message.id
                    )

                except:

                    try:
                        await handle_private(
                            client,
                            acc,
                            message,
                            username,
                            msgid
                        )

                    except Exception as e:

                        if ERROR_MESSAGE == True:
                            await client.send_message(
                                message.chat.id,
                                f"Error: {e}",
                                reply_to_message_id=message.id
                            )

            await asyncio.sleep(WAITING_TIME)

        if LOGIN_SYSTEM == True:

            try:
                await acc.disconnect()

            except:
                pass

        batch_temp.IS_BATCH[message.from_user.id] = True

        await client.send_message(
            message.chat.id,
            "☑️ Batch Completed Successfully."
		)

# handle private
async def handle_private(client: Client, acc, message: Message, chatid: int, msgid: int, remaining):
    msg: Message = await acc.get_messages(chatid, msgid)
    if msg.empty: return 
    msg_type = get_message_type(msg)
    if not msg_type: return 
    if CHANNEL_ID:
        try:
            chat = int(CHANNEL_ID)
        except:
            chat = message.chat.id
    else:
        chat = message.chat.id
    if batch_temp.IS_BATCH.get(message.from_user.id): return 
    if "Text" == msg_type:
        try:
            await client.send_message(chat, msg.text, entities=msg.entities, reply_to_message_id=message.id, parse_mode=enums.ParseMode.HTML)
            return 
        except Exception as e:
            if ERROR_MESSAGE == True:
                await client.send_message(message.chat.id, f"Error: {e}", reply_to_message_id=message.id, parse_mode=enums.ParseMode.HTML)
            return 

    message._start_time = time.time()

    smsg = await client.send_message(
        message.chat.id,
        "⚡ Starting Process...",
        reply_to_message_id=message.id
    )

    asyncio.create_task(
        downstatus(
            client,
            f'{message.id}downstatus.txt',
            smsg,
            chat
        )
	)
    try:
        file = await acc.download_media(msg, progress=progress, progress_args=[message,"down"])
        os.remove(f'{message.id}downstatus.txt')
    except Exception as e:
        if ERROR_MESSAGE == True:
            await client.send_message(message.chat.id, f"Error: {e}", reply_to_message_id=message.id, parse_mode=enums.ParseMode.HTML) 
        return await smsg.delete()
    if batch_temp.IS_BATCH.get(message.from_user.id): return 
    asyncio.create_task(upstatus(client, f'{message.id}upstatus.txt', smsg, chat))

    if msg.caption:
        caption = msg.caption
    else:
        caption = None
    if batch_temp.IS_BATCH.get(message.from_user.id): return 
            
    if "Document" == msg_type:
        try:
            ph_path = await acc.download_media(msg.document.thumbs[0].file_id)
        except:
            ph_path = None
        
        try:
            await client.send_document(chat, file, thumb=ph_path, caption=caption, reply_to_message_id=message.id, parse_mode=enums.ParseMode.HTML, progress=progress, progress_args=[message,"up"])
        except Exception as e:
            if ERROR_MESSAGE == True:
                await client.send_message(message.chat.id, f"Error: {e}", reply_to_message_id=message.id, parse_mode=enums.ParseMode.HTML)
        if ph_path != None: os.remove(ph_path)
        

    elif "Video" == msg_type:
        try:
            ph_path = await acc.download_media(msg.video.thumbs[0].file_id)
        except:
            ph_path = None
        
        try:
            await client.send_video(chat, file, duration=msg.video.duration, width=msg.video.width, height=msg.video.height, thumb=ph_path, caption=caption, reply_to_message_id=message.id, parse_mode=enums.ParseMode.HTML, progress=progress, progress_args=[message,"up"])
        except Exception as e:
            if ERROR_MESSAGE == True:
                await client.send_message(message.chat.id, f"Error: {e}", reply_to_message_id=message.id, parse_mode=enums.ParseMode.HTML)
        if ph_path != None: os.remove(ph_path)

    elif "Animation" == msg_type:
        try:
            await client.send_animation(chat, file, reply_to_message_id=message.id, parse_mode=enums.ParseMode.HTML)
        except Exception as e:
            if ERROR_MESSAGE == True:
                await client.send_message(message.chat.id, f"Error: {e}", reply_to_message_id=message.id, parse_mode=enums.ParseMode.HTML)
        
    elif "Sticker" == msg_type:
        try:
            await client.send_sticker(chat, file, reply_to_message_id=message.id, parse_mode=enums.ParseMode.HTML)
        except Exception as e:
            if ERROR_MESSAGE == True:
                await client.send_message(message.chat.id, f"Error: {e}", reply_to_message_id=message.id, parse_mode=enums.ParseMode.HTML)     

    elif "Voice" == msg_type:
        try:
            await client.send_voice(chat, file, caption=caption, caption_entities=msg.caption_entities, reply_to_message_id=message.id, parse_mode=enums.ParseMode.HTML, progress=progress, progress_args=[message,"up"])
        except Exception as e:
            if ERROR_MESSAGE == True:
                await client.send_message(message.chat.id, f"Error: {e}", reply_to_message_id=message.id, parse_mode=enums.ParseMode.HTML)

    elif "Audio" == msg_type:
        try:
            ph_path = await acc.download_media(msg.audio.thumbs[0].file_id)
        except:
            ph_path = None

        try:
            await client.send_audio(chat, file, thumb=ph_path, caption=caption, reply_to_message_id=message.id, parse_mode=enums.ParseMode.HTML, progress=progress, progress_args=[message,"up"])   
        except Exception as e:
            if ERROR_MESSAGE == True:
                await client.send_message(message.chat.id, f"Error: {e}", reply_to_message_id=message.id, parse_mode=enums.ParseMode.HTML)
        
        if ph_path != None: os.remove(ph_path)

    elif "Photo" == msg_type:
        try:
            await client.send_photo(chat, file, caption=caption, reply_to_message_id=message.id, parse_mode=enums.ParseMode.HTML)
        except Exception as e:
            if ERROR_MESSAGE == True:
                await client.send_message(message.chat.id, f"Error: {e}", reply_to_message_id=message.id, parse_mode=enums.ParseMode.HTML)
    
    if os.path.exists(f'{message.id}upstatus.txt'): 
        os.remove(f'{message.id}upstatus.txt')
        os.remove(file)
    await client.delete_messages(message.chat.id,[smsg.id])


# get the type of message
def get_message_type(msg: pyrogram.types.messages_and_media.message.Message):
    try:
        msg.document.file_id
        return "Document"
    except:
        pass

    try:
        msg.video.file_id
        return "Video"
    except:
        pass

    try:
        msg.animation.file_id
        return "Animation"
    except:
        pass

    try:
        msg.sticker.file_id
        return "Sticker"
    except:
        pass

    try:
        msg.voice.file_id
        return "Voice"
    except:
        pass

    try:
        msg.audio.file_id
        return "Audio"
    except:
        pass

    try:
        msg.photo.file_id
        return "Photo"
    except:
        pass

    try:
        msg.text
        return "Text"
    except:
        pass
        

# Don't Remove Credit @VJ_Bots
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01
