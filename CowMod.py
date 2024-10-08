__version__ = (2, 9, 5)

# meta developer: Аноним?
from .. import loader, utils
from hikkatl.tl.types import Message
import asyncio, re, telethon, string
from telethon.tl.types import KeyboardButtonSwitchInline


class CowMod(loader.Module):
    """Коров`яча доверка
🏷 Использование: Ник (аргумент)\n
📋 Аргументы:
  🐄 Для управления коровкой — мук, мус, муп, муи, мулс, мув, муз, муд, муа, муш, муг, муко, муку, мул, мукр, мукри, мун, муф, муб, муби, таск
  🐂 Для управления телям — бб, ббт, ббз, ббц, ббу, ббп, ббд, ббя, ббч, ббс, ббм, бби, ббб, ббр, ббх, вб
  🎒 Для управления рюкзаком — лог[ика], пам[ять], чте[ние], физ[уха], фан[тазия], кре[ативность] (цифра)
  🔢 Для управления цифрами — ц|циф|цифра (-∞; +∞)
  🐥 Для управления цыпами — цыпа (1-10)
  👀 Для управления мз — мз (предмет), (предмет)...
  👀 Для управления рес — рес (предмет), (предмет)...
  🌿 Для управления кинуть — кинуть|доверить (предмет),  [т|тал(исман), пикси]
  🎏 Для управления базаром, рынком — [бз|базар] (предмет), рынок (предмет)
  🕹 Для управления инлайн кнопками — (-∞; +∞)
  🕹 Для управления #чеккоманд — чек
  ✨ Для управления доп. командами — муу, адд, скрафтить, гифт, пок, ач, рек, херомант, медаль, дд, ив, ивр, ивт, ивс, ивя, иви, ивм, ивз, гб, коров(ка)|ник|имя|к"""
    strings = {"name": "HikkaDov"}

    async def client_ready(self, client, db):
        self.db = db
        self.client = client
        if not self.db.get("CowMod", "dovs_ids", False):
            self.db.set("CowMod", "dovs_ids", [])
        if not self.db.get("CowMod", "prefix", False):
            self.db.set("CowMod", "prefix", "Г")
        self.cow_actions = {'мук': 'Мук', 'мулс': 'Мулс', 'муф': 'Муф', 'муи': 'Муи', 'муа': 'Муа', 'муп': 'Муп', 'муш': 'Муш', 'мус': 'Мус', 'мув': 'Мув', 'муз': 'Муз', 'муд': 'Муд', 'муко': 'Муко', 'муку': 'Муку', 'мул': 'Мул', 'муг': 'Муг', 'муби': 'Муби', 'муб': 'Муб', 'мукр': 'Мукр', 'муу': 'Муу', 'мун': 'Мун', 'мукри': 'Мукри', 'херомант': 'Херомант', 'дд': 'Дд', 'гб': 'Гб', 'гифт': 'Гифт', 'таск': 'Му таск', 'ив': 'Ив', 'ивс': 'Ивс', 'ивт': 'Ивт', 'ивя': 'Ивя', 'иви': 'Иви', 'ивм': 'Ивм', 'ивз': 'Ивз', 'ивр': 'Ивр', 'трс': 'Трс', 'сг': 'Сг', 'сгг': 'Сгг', 'сгл': 'Сгл', 'сги': 'Сги', 'сгс': 'Сгс', 'тк': 'Тк', 'ткб': 'Ткб', 'ткн': 'Ткн', 'ткс': 'Ткс'}
        self.bull_actions = {"бб": "Бб", "ббт": "Ббт", "ббб": "Ббб", "ббз": "Ббз", "ббц": "Ббц", "ббх": "Ббх", "ббу": "Ббу", "ббп": "Ббп", "ббд": "Ббд", "ббя": "Ббя", "ббч": "Ббч", "ббс": "Ббс", "ббм": "Ббм", "бби": "Бби", "ббр": "Ббр", "вб": "Вб"}
        self.bp_actions = [("лог[ика]{,3}\s\d+$", "Логика"), ("пам[ять]{,3}\s\d+$", "Память"), ("чте[ние]{,3}\s\d+$", "Чтение"), ("физ[уха]{,3}\s\d+$", "Физуха"), ("фан[тазия]{,5}\s\d+$", "Фантазия"), ("кре[ативность]{,9}\s\d+$", "Креативность")]
        self.dovs_ids = self.db.get("CowMod", "dovs_ids")
        self.prefix = self.db.get("CowMod", "prefix")

    async def watcher(self, message):
        if not isinstance(message, telethon.tl.types.Message): return
        reply = await message.get_reply_message()
        author, content = await message.get_sender(), message.message
        args = utils.get_args_raw(message)
        bruh = await self.client.get_me()
        cow_name = bruh.last_name

        if author is None:
            return

# Действия с коровкой
        if author is not None and author.id in self.dovs_ids:
            for action, response in self.cow_actions.items():
                pattern = self.prefix + r'\s+' + action + "$"
                if re.match(pattern, content, re.IGNORECASE):
                    await message.respond(response)

# Действия с телями
        if author is not None and author.id in self.dovs_ids:
            for action, response in self.bull_actions.items():
                pattern = self.prefix + r'\s+' + action + "$"
                if re.match(pattern, content, re.IGNORECASE):
                    await message.respond(response)
# Действия с рюкзаком
        if author.id in self.dovs_ids:
            for action, response in self.bp_actions:
                if re.match(r := self.prefix + r'\s+' + action + "( \d+|)$", content, re.IGNORECASE):
                    await reply.reply(args)

# Действия с цифрами
        if author.id in self.dovs_ids and (r := re.match(self.prefix + r'\s+(?:ц|циф|цифра)\s+(-?\d+)$', content, re.IGNORECASE)):
            if r.group(1):
                num_value = int(r.group(1))
                await reply.reply(str(num_value))


# Действия с ником
        if author.id in self.dovs_ids and re.match(self.prefix + r'\s+(коров[ка]{,2}$|к$|имя$|ник$)', content, re.IGNORECASE):
            if "🐮" in cow_name:
                updated_name = cow_name.replace("🐮", "")
            else:
                updated_name = f"{cow_name} 🐮"
            await self.client(telethon.tl.functions.account.UpdateProfileRequest(last_name=updated_name))
            await message.respond(f"✅ Имя изменилось на: <b><i>{updated_name}</i></b>")

# Действия с разными предметами
        if author.id in self.dovs_ids and re.match(self.prefix + r'\s+т(?:ал(?:и(?:с(?:м(?:ан?)?)?)?)?)?$', content, re.IGNORECASE):
            await message.reply("Кинуть талисман")
        if author.id in self.dovs_ids and re.match(self.prefix + r'\s+пикси$', content, re.IGNORECASE):
            await message.reply("Кинуть пикси")
        if author.id in self.dovs_ids and re.match(self.prefix + r'\s+медаль$', content, re.IGNORECASE):
            await message.reply("Медаль")
        if author.id in self.dovs_ids and re.match(self.prefix + r'\s+адд$', content, re.IGNORECASE):
            await reply.reply("Адд")

# Действия с скрафтить
        if author.id in self.dovs_ids and (r := re.match(self.prefix + r' скрафтить\s\w+\s\d+$', content, re.IGNORECASE)):
            await message.reply(str(args))

# Действия с пок
        if author.id in self.dovs_ids and (r := re.match(self.prefix + r' пок(?:\s+\w+)?$', content, re.IGNORECASE)):
            await message.reply(str(args))

# Действия с кинуть
        if author.id in self.dovs_ids and (r := re.match(self.prefix + r' кинуть\s\w+', content, re.IGNORECASE)):
            await message.reply(str(args))

# Действия с доверить
        if author.id in self.dovs_ids and (r := re.match(self.prefix + r' доверить\s\w+', content, re.IGNORECASE)):
            await message.reply(str(args))

        # Действия с кинуть
        if author.id in self.dovs_ids and (r := re.match(self.prefix + r' подарить\s\w+', content, re.IGNORECASE)):
            await message.reply(str(args))

        # Действия с кинуть
        if author.id in self.dovs_ids and (r := re.match(self.prefix + r' отправить\s\w+', content, re.IGNORECASE)):
            await message.reply(str(args))

# Действия с рынком, базаром
        if author.id in self.dovs_ids and (r := re.match(self.prefix + r' (базар|бз)\s+\w+$', content, re.IGNORECASE)):
            await message.reply(str(args))
        if author.id in self.dovs_ids and (r := re.match(self.prefix + r' рынок(?:\s+\w+)?$', content, re.IGNORECASE)):
            await message.reply(str(args))

# Действия с мз
        if author.id in self.dovs_ids and (r := re.match(self.prefix + r' мз(?:\s+\w+)?', content, re.IGNORECASE)):
            await message.reply(str(args))

# Действия с рес
        if author.id in self.dovs_ids and (r := re.match(self.prefix + r' рес(?:\s+\w+)?', content, re.IGNORECASE)):
            await message.reply(str(args))

# Действия с рек, ач
        if author.id in self.dovs_ids and (r := re.match(self.prefix + r' рек(?:\s+\w+)?$', content, re.IGNORECASE)):
            await message.reply(str(args))
        if author.id in self.dovs_ids and (r := re.match(self.prefix + r' ач(?:\s+\w+)?$', content, re.IGNORECASE)):
            await message.reply(str(args))

# Действия с цыпами
        if author.id in self.dovs_ids and (r := re.match(self.prefix + r' цыпа( \d+|)$', content, re.IGNORECASE)):
            if r.group(1) and int(r.group(1)) > 10: return
            for _ in range(int((r.group(1) or f' {1}')[1:])):
                await message.reply("Кинуть цыпа")
                await asyncio.sleep(2)

# Действия с чек
        if author.id in self.dovs_ids and re.match(self.prefix + r'\s+чек$', content, re.IGNORECASE):
            reply = await self.client.get_messages(message.chat_id, ids=reply.id)
            markup = reply.reply_markup

            if markup and markup.rows:
                for row in markup.rows:
                    for button in row.buttons:
                        if isinstance(button, KeyboardButtonSwitchInline):
                            await self.client.send_message(message.chat_id, f"@{reply.sender.username}{button.query}")

# Действия с инлайнами
        try:
            n = int(args)-1
            if author.id in self.dovs_ids and re.match(self.prefix + r'\s+' + str(args), content, re.IGNORECASE):
                await reply.click(n)
        except ValueError: return

# Доверенность
    @loader.owner
    async def dovcmd(self, message):
        """(аргумент1) (аргумент 2)\n 📝 Введи команду для просмотра аргументов!"""
        args = utils.get_args(message)
        if len(args) < 1:
            dovs_ids_str = ', '.join(f'<code>@{id}</code>' for id in self.dovs_ids)
            await self.inline.form(f"🌘 <code>.dov сет</code>  <i>id/реплай</i> <b>— Добавить/удалить доверенность.</b>\n    🐮 <b>Доверенные пользователи:</b>\n{dovs_ids_str}\n\n🌘 <code>.dov ник</code> <i>ник</i> <b>— Установить ник.</b>\n    🐮 <b>Ваш ник:</b> <code>{utils.escape_html(self.prefix)}</code>", message, {'text': 'закрыть', 'action': 'close'})
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
