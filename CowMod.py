__version__ = (2, 3, 1)
# meta developer: Аноним?
from .. import loader, utils
from hikkatl.tl.types import Message
import asyncio, re, telethon, string

class CowMod(loader.Module):
    """Коров`яча доверка
🏷 Использование: Ник (аргумент)\n
📋 Аргументы:
  🐄 Для управления коровкой — мук, мулс, муд, муа, мув, муз, мукр, мун, муф, муг, муко, муку, мул, мус, муб, муби, пок
  🐂 Для управления телям — бб, ббт, ббз, ббц, ббу, ббп, ббд, ббя, ббч, ббс, ббм, бби, ббр
  🎒 Для управления рюкзаком — лог[ика], пам[ять], чте[ние], физ[уха], фан[тазия], кре[ативность] (цифра)
  🧤 Для управления крафтами — крафт (1-50) 
  🐥 Для управления цыпами — цыпа (1-10)
  👀 Для управления мз — мз (предмет), (предмет)...
  👀 Для управления рес — рес (предмет), (предмет)...
  🌿 Для управления кинуть — кинуть (предмет),  [т|тал(исман), пикси]
  🕹 Для управления инлайн кнопками — (-∞; +∞)
  ✨ Для управления доп. командами — муу, адд, скрафтить, х|хер[омант]"""
    strings = {"name": "CowMod"}

    async def client_ready(self, client, db):
        self.db = db
        self.client = client #IDS
        if not self.db.get("CowMod", "dovs_ids", False):
            self.db.set("CowMod", "dovs_ids", [])
        if not self.db.get("CowMod", "prefix", False):
            self.db.set("CowMod", "prefix", "Г")
        self.cow_actions = {"мук": "Мук", "мулс": "Мулс", "муф": "Муф", "муа": "Муа", "мус": "Мус", "мув": "Мув", "муз": "Муз", "муд": "Муд", "муко": "Муко", "муку": "Муку", "мул": "Мул", "муг": "Муг", "муби": "Муби", "муб": "Муб", "мукр": "Мукр", "муу": "Муу", "мун": "Мун", "пок": "Пок"}
        self.bull_actions = {"бб": "Бб", "ббт": "Ббт", "ббз": "Ббз", "ббц": "Ббц", "ббу": "Ббу", "ббп": "Ббп", "ббд": "Ббд", "ббя": "Ббя", "ббч": "Ббч", "ббс": "Ббс", "ббм": "Ббм", "бби": "Бби", "ббр": "Ббр"}
        self.bp_actions = [("лог[ика]{,3}\s\d+$", "Логика"), ("пам[ять]{,3}\s\d+$", "Память"), ("чте[ние]{,3}\s\d+$", "Чтение"), ("физ[уха]{,3}\s\d+$", "Физуха"), ("фан[тазия]{,5}\s\d+$", "Фантазия"), ("кре[ативность]{,9}\s\d+$", "Креативность")]
        self.dovs_ids = self.db.get("CowMod", "dovs_ids")
        self.prefix = self.db.get("CowMod", "prefix")
        
    async def watcher(self, message):
        if not isinstance(message, telethon.tl.types.Message): return
        reply = await message.get_reply_message()
        author, content = await message.get_sender(), message.message
        args = utils.get_args_raw(message)

# Действия с коровкой
        if author.id in self.dovs_ids:
            for action, response in self.cow_actions.items():
                pattern = self.prefix + r'\s+' + action + "$"
                if re.match(pattern, content, re.IGNORECASE):
                    await message.respond(response)

# Действия с телями
        if author.id in self.dovs_ids:
            for action, response in self.bull_actions.items():
                pattern = self.prefix + r'\s+' + action + "$"
                if re.match(pattern, content, re.IGNORECASE):
                    await message.respond(response)
# Действия с рюкзаком   
        if author.id in self.dovs_ids:
            for action, response in self.bp_actions:
                if re.match(r := self.prefix + r'\s+' + action + "( \d+|)$", content, re.IGNORECASE):
                    await reply.reply(args)

# Действия с крафтом
        if author.id in self.dovs_ids and (r := re.match(self.prefix + r' крафт( \d+|)$', content, re.IGNORECASE)):
            if r.group(1):
                craft_value = int(r.group(1))
                if 1 <= craft_value <= 50:
                    await reply.reply(str(craft_value))

# Действия с разными предметами       
        if author.id in self.dovs_ids and re.search(self.prefix + r'\s+т(?:ал(?:и(?:с(?:м(?:ан?)?)?)?)?)?$', content, re.IGNORECASE):
            await message.reply("Кинуть талисман")
        if author.id in self.dovs_ids and re.match(self.prefix + r'\s+пикси$', content, re.IGNORECASE):
            await message.reply("Кинуть пикси")
        if author.id in self.dovs_ids and re.match(self.prefix + r'\s+х(?:ер(?:о(?:м(?:а(?:н(?:т?)?)?)?)?)?)?$', content, re.IGNORECASE):
            await message.reply("Херомант")
        if author.id in self.dovs_ids and re.match(self.prefix + r'\s+адд$', content, re.IGNORECASE):
            await reply.reply("Адд")

# Действия с скрафтить
        args = utils.get_args_raw(message)
        if author.id in self.dovs_ids and (r := re.match(self.prefix + r' скрафтить\s\w+\s\d+$', content, re.IGNORECASE)):
            await message.reply(str(args))

# Действия с кинуть
        if author.id in self.dovs_ids and (r := re.search(self.prefix + r' кинуть\s\w+', content, re.IGNORECASE)):
            await message.reply(str(args))

# Действия с мз
        args = utils.get_args_raw(message)
        if author.id in self.dovs_ids and (r := re.match(self.prefix + r' мз\s\w+', content, re.IGNORECASE)):
            await message.reply(str(args))

# Действия с рес
        args = utils.get_args_raw(message)
        if author.id in self.dovs_ids and (r := re.match(self.prefix + r' рес\s\w+', content, re.IGNORECASE)):
            await message.reply(str(args))

# Действия с цыпами
        if author.id in self.dovs_ids and (r := re.match(self.prefix + r' цыпа( \d+|)$', content, re.IGNORECASE)):
            if r.group(1) and int(r.group(1)) > 10: return
            for _ in range(int((r.group(1) or f' {1}')[1:])):
                await message.reply("Кинуть цыпа")
                await asyncio.sleep(2)

# Действия с инлайнами
        try:
            n = int(args)-1
            if author.id in self.dovs_ids and re.match(self.prefix + r'\s+' + str(args), content, re.IGNORECASE):
                await reply.click(n)
        except ValueError: return

    @loader.owner
    async def dovcmd(self, message):
        """(аргумент 1) (аргумент 2)
        Введи команду для просмотра аргументов!"""
        args = utils.get_args(message)
        if len(args) < 1:
            dovs_ids_str = ', '.join(f'<code>@{id}</code>' for id in self.dovs_ids)
            await self.inline.form(f"🌘 <code>.dov сет</code>  <i>id/реплай</i> <b>— Добавить/удалить доверенность.</b>\n    🐮 <b>Доверенные пользователи:</b>\n{dovs_ids_str}\n\n🌘 <code>.dov ник</code> <i>ник</i> <b>— Установить ник.</b>\n   🐮 <b>Ваш ник:</b> <code>{utils.escape_html(self.prefix)}</code>", message, {'text': 'закрыть', 'action': 'close'})
        return

        if args[0].lower() == "ник":
            new_prefix = args[1]
            self.prefix = new_prefix
            self.db.set("CowMod", "prefix", new_prefix)
            await message.respond(f"✅ <b>Ник изменен на:</b> {new_prefix}")
        elif args[0].lower() == "сет":
            if len(args) < 2 and not (message.is_reply and message.reply_to_msg_id):
                await message.respond("❌ <b>Не указан id/реплай.</b>")
                return

            if message.is_reply and message.reply_to_msg_id:
                reply_message = await message.get_reply_message()
                if reply_message.sender_id:
                    new_id = reply_message.sender_id
                    if new_id in self.dovs_ids:
                        self.dovs_ids.remove(new_id)
                        await message.respond(f"✅ <b>Доверенность удалена:</b> {new_id}")
                    else:
                        self.dovs_ids.append(new_id)
                        await message.respond(f"✅ <b>Доверенность добавлена:</b> {new_id}")
                else:
                    await message.respond("❌ <b>Невозможно получить id отправителя!</b>")
            else:
                new_id = args[1].lstrip("@")
                if new_id.isdigit():
                    new_id = int(new_id)
                    if new_id in self.dovs_ids:
                        self.dovs_ids.remove(new_id)
                        await message.respond(f"✅ <b>Доверенность удалена:</b> {new_id}")
                    else:
                        self.dovs_ids.append(new_id)
                        await message.respond(f"✅ <b>Доверенность добавлена:</b> {new_id}")
                else:
                    await message.respond("❌ <b>Это не id/реплай</b>")
        else:
            await message.respond("❌ <b>Неверные аргументы!</b>")
