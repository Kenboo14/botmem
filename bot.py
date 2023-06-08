from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
import logging

# Set level log
logging.basicConfig(level=logging.INFO)

# Gunakan logging.info() untuk menulis log
logging.info("Pesan log info")
logging.warning("Pesan log warning")
logging.error("Pesan log error")


# Inisialisasi bot Telegram
api_id = 24977504
api_hash = '431a1ec75b188d6d3d46dabe99126c6e'
bot_token = '6091391494:AAHOIxGlD6tNFB3TGgKGGUlVDkjvuPNuuOo'

# Inisialisasi klien Pyrogram
bot = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token, plugins=dict(root="bot"))
text = "🧸 BenUserbot Premium\n\n↪️ Kebijakan Pengembalian\nSetelah melakukan pembayaran, jika Anda belum memperoleh/menerima manfaat  dari pembelian, Anda dapat menggunakan hak penggantian dalam waktu 2 hari setelah pembelian. Namun, jika Anda telah menggunakan/menerima salah satu manfaat dari pembelian, termasuk akses ke fitur pembuatan userbot, maka Anda tidak lagi berhak atas pengembalian dana.\n\n🆘 Dukungan\nUntuk mendapatkan dukungan, Anda dapat:\n• Menghubungi @eldipion di Telegram\n• Menghubungi @Drexc0de di Telegra>\n\n👉🏻 Tekan tombol Lanjutkan untuk menyatakan bahwa Anda telah membaca dan menerima ketentuan ini dan melanjutkan pembelian. Jika tidak, tekan tombol Batalkan."
tuxt = "👋🏻 Halo Tongmet Lovers, selamat datang di Bot!Dengan @v1BNubot, Anda dapat membuat userbot Telegram dengan mudah dan cepat."
members = {
    "🌟premium": {"price": 15000},
    "💎ultrapremium": {"price": 20000}
}


# Fungsi untuk menampilkan tombol membership
def show_membership_buttons():
    keyboard = []
    for membership, data in members.items():
        price = data["price"]
        button_text = f"{membership.capitalize()} - Rp.{price}"
        callback_data = f"membership_{membership}"
        button = InlineKeyboardButton(button_text, callback_data=callback_data)
        keyboard.append([button])
        
    keyboard.append([InlineKeyboardButton("🚪 Kembali", callback_data="subtombol1")])

    return InlineKeyboardMarkup(keyboard)

# Fungsi untuk menampilkan detail membership dan tombol checkout
def show_membership_detail(membership):
    data = members[membership]
    price = data["price"]
    text = f"Kamu memilih\n{membership.capitalize()} dengan harga Rp.{price}\n\n"
    text += "Jika benar, silahkan klik tombol Next. Untuk melanjutkan Pembayaran"
    buttdet_memship = [
            [
                InlineKeyboardButton("🔙 Back", callback_data="tombol1"),
                InlineKeyboardButton("🔜 Next", callback_data="checkout")
            ],
        ]
    return text, InlineKeyboardMarkup(buttdet_memship)
    


# Fungsi untuk menampilkan detail checkout dan tombol konfirmasi pembayaran
def show_checkout_detail(membership):
    data = members[membership]
    price = data["price"]
    text = f"🛒Keranjang\n\nDengan ini Anda memilih:\n{membership.capitalize()} - Rp.{price}\n\n"
    text += "Selesaikan dengan mengirim payment sesuai yang sudah di sediakan:\n\n"
    text += "BCA : 0882410445\n"
    text += "DANA : 081394369076\n"
    text += "Atas Nama: Much*** Ag** A*\n\n"
    text += "Wajib Menyertakan Bukti Screenshot Pembayaran"
    keyboard = [
        [
            InlineKeyboardButton("✅ Bayar", callback_data="confirm")
        ],
        [
            InlineKeyboardButton("❌ Batalkan", callback_data="tombol1")
        ]
    ]
    return text, InlineKeyboardMarkup(keyboard)


# Fungsi untuk menangani callback query dari tombol membership
@bot.on_callback_query(filters.regex("^membership_"))
async def handle_membership_callback(client: Client, callback_query: CallbackQuery):
    membership = callback_query.data.split("_")[1]
    text, reply_markup = show_membership_detail(membership)
    await callback_query.edit_message_text(text, reply_markup=reply_markup)


# Fungsi untuk menangani callback query dari tombol checkout
@bot.on_callback_query(filters.regex("^checkout$"))
async def handle_checkout_callback(client: Client, callback_query: CallbackQuery):
    membership = callback_query.message.text.split()[2].lower()
    text, reply_markup = show_checkout_detail(membership)
    await callback_query.edit_message_text(text, reply_markup=reply_markup)

# Fungsi untuk menangani callback query dari tombol confirm
@bot.on_callback_query(filters.regex("^confirm$"))
async def handle_confirm_callback(client: Client, callback_query: CallbackQuery):
    await callback_query.edit_message_text("⚠️ Silahkan upload bukti pembayaran")
owner_admin = [1935806583, 1971524208]
# Fungsi untuk memfilter pesan yang berisi gambar/foto
@bot.on_message(filters.photo & filters.private)
def handle_image_message(client, message):
    # Mendapatkan informasi pengguna pengirim
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    username = message.from_user.username

    # Mengirimkan pesan ke owner bot
    owner_chat_ids = [1935806583, 6036774020] # Daftar ID obrolan admin yang diperbolehkan
    owner_message = f"Pesan gambar dari pengguna:\n\nID: {user_id}\nNama: {first_name} {last_name}\nUsername: @{username}"
    for owner_chat_id in owner_chat_ids:
        client.send_message(owner_chat_id, owner_message)

    # Mengirim ulang gambar/foto ke owner bot
    image_file_id = message.photo.file_id
    for owner_chat_id in owner_chat_ids:
        client.send_photo(owner_chat_id, image_file_id)
        
    message.reply_text(text="✅ Terimakasi Pembayaran anda akan segera diproses oleh admin, mohon tunggu....")
    
# Daftar ID pengguna admin atau owner bot
owner_ids = [1935806583, 6036774020]

# Fungsi untuk memfilter pesan yang dikirim oleh pengguna biasa ke bot
@bot.on_message(filters.photo & ~filters.private & ~filters.edited)
def handle_user_message(client, message):
    if message.from_user.id not in owner_ids:
        # Mengirim pesan ke owner bot
        owner_chat_ids = owner_ids
        for owner_chat_id in owner_chat_ids:
            client.forward_messages(owner_chat_id, message.chat.id, message.message_id)
            
        image_file_id = message.photo.file_id
        for owner_chat_id in owner_chat_ids:
              client.send_photo(owner_chat_id, image_file_id)
              
        message.reply_text(text="✅ Terimakasi Pembayaran anda akan segera diproses oleh admin, mohon tunggu....")
# Fungsi untuk memfilter pesan balasan dari owner bot kepada pengguna
@bot.on_message(filters.private & filters.reply & filters.user(owner_ids))
def handle_owner_reply(client, message):
    # Mendapatkan informasi pengguna pengirim balasan
    user_id = message.from_user.id

    # Mengirim pesan balasan ke pengguna asli
    original_message = client.get_messages(message.reply_to_message.forward_from_chat.id, message.reply_to_message.message_id)
    client.send_message(original_message.chat.id, message.text)
    
    
def show_menu_mem(callback_query: CallbackQuery, data: str):
    # Menampilkan tombol dengan teks/penjelasan dan tombol "Kembali"
    keyboard = [    
                    
                    [   
                        InlineKeyboardButton("🔙 Back", callback_data='tombol1')
                    ]
                ]
    reply_markup = InlineKeyboardMarkup(keyboard)
def show_main_menu(message: Message):
	keyboard = [
			[
				InlineKeyboardButton("🛒 Usbot", callback_data='subtombol1')
			]
		]
	reply_markup = InlineKeyboardMarkup(keyboard)
	message.reply_text(text=tuxt, reply_markup=reply_markup)
def show_sub_menu(message: Message):
	keyboard  = [
			[
				InlineKeyboardButton("Ubot", callback_data='tombol2')
			]
		]
	reply_markup = InlineKeyboardMarkup(keyboard)
	message.reply_text(text="Ubot nih", reply_markup=reply_markup)
# Fungsi untuk menangani pesan masuk
@bot.on_message(filters.command('start'))
def start_command_handler(client: Client, message: Message):
    show_main_menu(message)

# Fungsi untuk menangani penekanan tombol
@bot.on_callback_query()
def button_click_handler(client: Client, callback_query: CallbackQuery):
    # Mendapatkan data yang dikirim melalui tombol
    data = callback_query.data
        

      
    # Menampilkan pesan yang sesuai tergantung dari tombol yang ditekan
    if data == "tombol1":
        tuks = tuxt
        keyboard = [
            [
                InlineKeyboardButton("🛒 Usbot", callback_data="subtombol1")
            ]
        ]
        reply_markup=InlineKeyboardMarkup(keyboard)
        callback_query.edit_message_text(text=tuks, reply_markup=InlineKeyboardMarkup(keyboard))
    elif data == "tombol2":
        show_sub_menu(callback_query, "Tombol 2")
    elif data == "tombol3":
        show_sub_menu(callback_query, "Tombol 3")
    if data == "subtombol1":
        back_sub1 = [
            [
                InlineKeyboardButton("🔜 Next", callback_data="subtombol2")
            ],
            [
                InlineKeyboardButton("🔙 Back", callback_data="tombol1")
            ],
        ]
        reply_markup=InlineKeyboardMarkup(back_sub1)
        callback_query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(back_sub1))
    elif data == "subtombol2":
        teks = "🤖Ada perbedaan harga,jenis, dan fitur.\nHarga & Jenis yang tercantum dibwah sudah termasuk 1Bulan.\n\nJika anda menyetujui. Silahkan pilih tombol yang dibawah"
        keyboard = show_membership_buttons()
        callback_query.edit_message_text(text=teks, reply_markup=keyboard)
    if data == "noktel":
        tekk = "📞 Noktel (Nomor Kosong Telegram)\n\nIDC 1 = Rp. 35.000\nIDC 2 = Rp. 32.000\nIDC 5/6 = Rp. 3.000\n\n⚠️ Silahkan Upload Bukti pembayaran dengan caption detail Pemesanan anda"
        noktels = [
            [
                InlineKeyboardButton("🔙 Back", callback_data="tombol1")
            ],
        ]
        callback_query.edit_message_text(text=tekk,reply_markup=InlineKeyboardMarkup(noktels))
    if data == "kembali":
        keyboard = [
            [       
                InlineKeyboardButton("🛒 Merchandise", callback_data='tombol1')       
            ],
            [   
                InlineKeyboardButton("🆘 SOS", url="https://t.me/rexc0de"),
                InlineKeyboardButton("👤 My Account", callback_data='tombol3')
            ],
        ]
        reply_markup=InlineKeyboardMarkup(keyboard)
        callback_query.edit_message_text(f"Haloo Tongmet Lovers Welcome To Bot", reply_markup=InlineKeyboardMarkup(keyboard))


# Menjalankan bot
bot.run()
