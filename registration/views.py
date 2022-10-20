from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from telethon import TelegramClient, sync
from pyrogram import *
from telebot import *
import telebot
from .models import SimCardOption, Gift, Client, SimOrder
from django.core.files.base import ContentFile
import logging

logger = telebot.logger

bot = telebot.TeleBot("5696455466:AAH4ui4aHOInjRi20GcdGK4OTGcv12mAA88") # test token

# bot = telebot.TeleBot("5051960822:AAFyFKJFrybdVmRsrG3E1k3rCz3bVXFEYPo") # simdroid main token

@csrf_exempt
def index(request):
    if request.method == 'GET':
        return HttpResponse("Bot Url Page")
    elif request.method == 'POST':
        bot.process_new_updates([
            telebot.types.Update.de_json(
                request.body.decode("utf-8")
            )
        ])
        return HttpResponse(status=200)


@bot.message_handler(commands=['start'])
def greeting(message):  
    video = open('in.mp4', 'rb')
    bot.send_message(message.from_user.id, '*Botdan osonroq foydalnish uchun quyidagi videoni ko\'ring*', parse_mode="Markdown")
    bot.send_video(message.from_user.id, video)
    
    if len(Client.objects.filter(user_id=message.from_user.id)) == 0:
        bot.send_message(message.from_user.id, '*Botga Xush kelibsiz...*\n', parse_mode="Markdown")
        client = Client.objects.create(
            user_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            )
        client.save()
    language_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    uzbek = types.KeyboardButton("🇺🇿 O'zbek")
    english = types.KeyboardButton("🇬🇧 English")
    russian = types.KeyboardButton("🇷🇺 Russian")
    language_markup.add(uzbek, english, russian)
    bot.send_message(message.from_user.id,
                  '*Iltimos kerakli tilni tanlang 🇬🇧:*\n', reply_markup=language_markup, parse_mode="Markdown")
    


@bot.message_handler(commands=['info'])
def info(message):    
    bot.send_message(message.from_user.id,
                     '*Bot haqida ma\'lumot 📕*', parse_mode="Markdown")


@bot.message_handler(func=lambda message: True, content_types=['photo', 'text'] )
def register_view(message):
    client = Client.objects.get(user_id=message.from_user.id)

    main_markup_uzbek = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1_u = types.KeyboardButton('Simkarta buyurtma berish 📦')
    btn2_u = types.KeyboardButton('Mening buyurtmalarim 📄')
    btn3_u = types.KeyboardButton('Linephone 📱')
    btn4_u = types.KeyboardButton('Ma\'lumot olish📕')
    main_markup_uzbek.add(btn1_u, btn2_u, btn3_u, btn4_u)

    main_markup_english = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1_e = types.KeyboardButton('Order simcard 📦')
    btn2_e = types.KeyboardButton('My orders 📄')
    btn3_e = types.KeyboardButton('Linephone 📱')
    btn4_e = types.KeyboardButton('Info📕')
    main_markup_english.add(btn1_e, btn2_e, btn3_e, btn4_e)

    main_markup_russian = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1_r = types.KeyboardButton('Заказать симкарту 📦')
    btn2_r = types.KeyboardButton('Мои заказы 📄')
    btn3_r = types.KeyboardButton('Linephone 📱')
    btn4_r = types.KeyboardButton('Информация📕')
    main_markup_russian.add(btn1_r, btn2_r, btn3_r, btn4_r)
    lan = client.language
    user_commands = ['Tasdiqlash✅', 'Orqaga ↩️', '🇺🇿 O\'zbek', '🇬🇧 English', '🇷🇺 Russian', 'Mening buyurtmalarim', 'My orders', 'Orqaga', 'O\'chirish', 'Bekor qilish 🚫', 'Ma\'lumot olish📕', 'Simkarta buyurtma berish','Order simcard', 'Info📕', 'Cancel 🚫', 'Back ↩️', 'Confirm✅', 'Simkartani o\'chirish'] 
    if message.text == "🇺🇿 O'zbek":
        client.language = 'uz'
        client.save()
        bot.send_message(message.from_user.id, '*Menyu:*', reply_markup=main_markup_uzbek, parse_mode="Markdown")
    elif message.text == "🇬🇧 English":
        client.language = 'en'
        client.save()
        bot.send_message(message.from_user.id, '*Menu*', reply_markup=main_markup_english, parse_mode="Markdown")
    elif message.text == "🇷🇺 Russian":
        client.language = 'ru'
        client.save() 
        bot.send_message(message.from_user.id, '*Меню:*', reply_markup=main_markup_russian, parse_mode="Markdown")
    

    elif (message.text == 'Simkarta buyurtma berish 📦' or message.text == 'Заказать симкарту 📦'):  
        order = SimOrder.objects.create(
            owner=client,
            sim_type=SimCardOption.objects.first(),
            full_name=message.from_user.first_name,
            gift=Gift.objects.first(),
            address='unavailable',
            tel_number='9x xxx xx xx'
            )
        order.active_sim = True
        order.step = 1
        order.save()
        client.step = 1
        client.save()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        if lan == 'uz':
            bot.send_message(message.from_user.id, '*Iltimos, simkarta buyurtma berish uchun quyidagi ma\'lumotlarni kiriting:*', parse_mode="Markdown")   
            btn2 = types.KeyboardButton('Bekor qilish 🚫')
            markup.add(btn2)
            bot.send_message(
            message.from_user.id, 'Ismingiz va familiyangizni kiriting 👨‍💼:', reply_markup=markup)
        elif lan == 'en':
            bot.send_message(message.from_user.id, '*Please, enter your credentials to order a simcard:*', parse_mode="Markdown")
            btn2 = types.KeyboardButton('Cancel 🚫')
            markup.add(btn2)
            bot.send_message(
            message.from_user.id, 'Enter your last and first name 👨‍💼:', reply_markup=markup)
        elif lan == 'ru':
            bot.send_message(message.from_user.id, '*Пожалуйста, введите свои данные, чтобы заказать сим-карту:*', parse_mode="Markdown")
            btn2 = types.KeyboardButton('Отмена 🚫')
            markup.add(btn2)
            bot.send_message(
            message.from_user.id, 'Введите свою фамилию и имя 👨‍💼:', reply_markup=markup)

    elif message.text == 'Ma\'lumot olish📕':
        bot.send_message(message.from_user.id,
                         "Bot haqida ma\'lumot:")

    elif message.text == 'Info📕':
        bot.send_message(message.from_user.id,
                         "Some text")

    elif message.text == 'Информация📕':
        bot.send_message(message.from_user.id,
                         "Информация📕")
    
    elif message.text == 'Bekor qilish 🚫':
        order = SimOrder.objects.filter(owner=client, active_sim=True).last()
        print(order)
        order.delete()
        
        bot.send_message(message.from_user.id,
                         "*Bekor qilindi.*\n", reply_markup=main_markup_uzbek, parse_mode="Markdown")
    
    elif message.text == 'Cancel 🚫':
        order = SimOrder.objects.filter(owner=client, active_sim=True).last()
        order.delete()
        bot.send_message(message.from_user.id,
                         "*Cancelled.*\n", reply_markup=main_markup_english, parse_mode="Markdown")

    elif message.text == 'Отмена 🚫':
        order = SimOrder.objects.filter(owner=client, active_sim=True).last()
        order.delete()
        bot.send_message(message.from_user.id,
                         "*Отменено.*\n", reply_markup=main_markup_russian, parse_mode="Markdown")
    
    elif message.text in ['Orqaga ↩️', 'Back ↩️', 'Назад ↩️']:
        order = SimOrder.objects.filter(owner=client, active_sim=True).last()
        order.step -= 1
        order.save()
        cancel_func(message)
    
    elif message.text == 'Linephone 📱':
        bot.send_message(message.from_user.id,
                          "Linephone\n")

    elif message.text in ['Tasdiqlash✅', 'Confirm✅', 'Подтвердить✅']:
        order = SimOrder.objects.filter(owner=client, step=8).first()
        order.step = 9
        order.active_sim = False
        order.save()
        if lan == 'uz':
            bot.send_message(message.from_user.id,
                         "*Buyurtmangiz qabul qilindi!*", reply_markup=main_markup_uzbek, parse_mode="Markdown")
        elif lan == 'en':
            bot.send_message(message.from_user.id,
                         "*Your order has been accepted!*", reply_markup=main_markup_english, parse_mode="Markdown")
        elif lan == 'ru':
            bot.send_message(message.from_user.id,
                         "*Ваш заказ принят!*", reply_markup=main_markup_russian, parse_mode="Markdown")
    
    elif (message.text == 'Mening buyurtmalarim 📄' or message.text == 'My orders 📄' or message.text == 'Мои заказы 📄'): # use callback query use loops to retrieve objects from database
        if lan == 'uz':
                bot.send_message(message.from_user.id,
                              "Sizning buyurtmalaringiz:\n")
        elif lan == 'en':
            bot.send_message(message.from_user.id,
                          "Your orders:\n")
        elif lan == 'ru':
            bot.send_message(message.from_user.id,
                              "Ваши заказы:\n")    
        orders = SimOrder.objects.filter(owner=client, active_sim=False)
        if len(orders) != 0:
            for order in orders:
                markup = types.InlineKeyboardMarkup(row_width=2)
                markup.add( types.InlineKeyboardButton("O'chirish ❌", callback_data=f"{order.id}"))
                bot.send_message(message.from_user.id, f"Buyurtma raqami:{order.id}\nIsm Familiyasi: {order.full_name}\nSim karta turi: {order.sim_type}\nSovg'a: {order.gift.name}\nManzil: {order.address}", reply_markup=markup)
        else:
            if lan == 'uz':
                bot.send_message(message.from_user.id,
                              "*Sizda hozircha buyurtmalar mavjud emas.*\n", reply_markup=markup, parse_mode="Markdown")
            if lan == 'en':
                bot.send_message(message.from_user.id,
                              "*You do not have any orders*\n", reply_markup=markup, parse_mode="Markdown")
            if lan == 'ru':
                bot.send_message(message.from_user.id,
                              "*У вас еще нет заказов.*\n", reply_markup=markup, parse_mode="Markdown")
    else:
        order = SimOrder.objects.filter(owner=client, active_sim=True).first()
        
        secordary_markup_u = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1_u = types.KeyboardButton('Orqaga ↩️')
        btn2_u = types.KeyboardButton('Bekor qilish 🚫')
        secordary_markup_u.add(btn1_u, btn2_u)

        secordary_markup_e = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1_e = types.KeyboardButton('Back ↩️')
        btn2_e = types.KeyboardButton('Cancel 🚫')
        secordary_markup_e.add(btn1_e, btn2_e)

        secordary_markup_r = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1_r = types.KeyboardButton('Назад ↩️')
        btn2_r = types.KeyboardButton('Отмена 🚫')
        secordary_markup_r.add(btn1_r, btn2_r)
        
        if order.step == 1:
            order.full_name = message.text
            client.first_name = message.text
            order.step += 1
            order.save()
            client.save()
            if lan == 'uz':
                bot.send_message(
                    message.from_user.id, 'Telefon raqamingizni 9x xxx xx xx ko\'rinshda kiriting☎️:', reply_markup=secordary_markup_u)
            if lan == 'en':
                bot.send_message(
                    message.from_user.id, 'Enter your phone number as shown: 9x xxx xx xx☎️:', reply_markup=secordary_markup_e)
            if lan == 'ru':
                bot.send_message(
                    message.from_user.id, 'Введите свой номер телефона, как показано: 9x xxx xx xx☎️:', reply_markup=secordary_markup_r)

        elif order.step == 2:
            if str(message.text).isdigit():
                order.tel_number = message.text
                order.step += 1
                order.save()
                sim_options = SimCardOption.objects.all()
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
                for s in sim_options:
                    markup.add(types.KeyboardButton(s.sim_option))
                if lan == 'uz':
                    markup.add(btn1_u, btn2_u)
                    bot.send_message(message.from_user.id,
                                     'Sim karta turini tanlang 🗂:', reply_markup=markup)
                if lan == 'en':
                    markup.add(btn1_e, btn2_e)
                    bot.send_message(message.from_user.id,
                                     'Choose the simcard type 🗂:', reply_markup=markup)
                if lan == 'ru':
                    markup.add(btn1_r, btn2_r)
                    bot.send_message(message.from_user.id,
                                     'Выберите тип сим-карты 🗂', reply_markup=markup)
            else:
                if lan == 'uz':
                    bot.send_message(message.from_user.id,
                                     'Iltimos to\'g\'ri ma\'lumot kiriting🙅‍♂️')
                    bot.send_message(
                        message.from_user.id, 'Telefon raqamingizni 9x xxx xx xx ko\'rinshda kiriting☎️:', reply_markup=secordary_markup_u)
                if lan == 'en':
                    bot.send_message(message.from_user.id,
                                     'Please, enter correct information🙅‍♂️')
                    bot.send_message(
                        message.from_user.id, 'Enter your phone number as shown: 9x xxx xx xx☎️:', reply_markup=secordary_markup_e)
                if lan == 'ru':
                    bot.send_message(message.from_user.id,
                                     'Пожалуйста, введите правильную информацию🙅‍♂️')
                    bot.send_message(
                        message.from_user.id, 'Введите свой номер телефона, как показано: 9x xxx xx xx☎️:', reply_markup=secordary_markup_r)

        elif order.step == 3: 
            obj = SimCardOption.objects.filter(sim_option=message.text).first()
            order.sim_option = obj
            order.step += 1
            order.save()
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
            gifts = Gift.objects.all()
            for g in gifts:
                markup.add(types.KeyboardButton(g.name))
            if lan == 'uz':
                markup.add(btn1_u, btn2_u)
                bot.send_message(
                    message.from_user.id, "Sim kartaga bonus sifatida sovg'aga ham ega bo'lasiz.\nSovga turini tanlang 🎁:", reply_markup=markup)
            if lan == 'en':
                markup.add(btn1_e, btn2_e)
                bot.send_message(
                    message.from_user.id, 'You can get a present as a bonus to a simcard.\nWhat do you want to get as a gift?\nChoose below 🎁:', reply_markup=markup)
            if lan == 'ru':
                markup.add(btn1_u, btn2_u)
                bot.send_message(
                    message.from_user.id, 'Вы можете получить подарок в качестве бонуса к симкарте.\nЧто вы хотите получить в подарок?\nВыберите ниже 🎁:', reply_markup=markup)
    
        elif order.step == 4: 
            obj = Gift.objects.filter(name=message.text).first()
            order.user_gift = obj
            order.step += 1
            order.save()
            if lan == 'uz':
                bot.send_message(message.from_user.id, "Passportingiz yoki ID kartangizning oldi qism rasmini jo'nating 🖼:", reply_markup=secordary_markup_u)
            if lan == 'en':
                bot.send_message(message.from_user.id, "Send the frontside picture of your ID or passport 🖼:", reply_markup=secordary_markup_e)
            if lan == 'ru':
                bot.send_message(message.from_user.id, "Отправьте фотографию своего удостоверения личности или паспорта на лицевой стороне 🖼:", reply_markup=secordary_markup_r)
       
        elif order.step == 5:
            raw = message.photo[1].file_id
            path = raw + ".jpg"
            file_info = bot.get_file(raw)
            downloaded_file = bot.download_file(file_info.file_path)
            content = ContentFile(downloaded_file)
            order.id_picture.save(path, content, save=True)
            order.step += 1
            order.save()
            if lan == 'uz':
                bot.send_message(message.from_user.id, "Passportingiz yoki ID kartangizning orqa qism rasmini jo'nating 🖼:", reply_markup=secordary_markup_u)
            if lan == 'en':
                bot.send_message(message.from_user.id, "Send the backside picture of your ID or passport 🖼:", reply_markup=secordary_markup_e)
            if lan == 'ru':
                bot.send_message(message.from_user.id, "Отправьте фотографию обратной стороны вашего удостоверения личности или паспорта 🖼:", reply_markup=secordary_markup_r)

        elif order.step == 6:
            raw = message.photo[1].file_id
            path = raw + ".jpg"
            file_info = bot.get_file(raw)
            downloaded_file = bot.download_file(file_info.file_path)
            content = ContentFile(downloaded_file)
            order.id_picture2.save(path, content, save=True)
            order.step += 1
            order.save()
            if lan == 'uz':
                bot.send_message(message.from_user.id, 'Manzilinginzi kiriting🏠:', reply_markup=secordary_markup_u)
            if lan == 'en':
                bot.send_message(message.from_user.id, 'Enter your address🏠:', reply_markup=secordary_markup_e)
            if lan == 'ru':
                bot.send_message(message.from_user.id, 'Введите свой адрес🏠:', reply_markup=secordary_markup_r)
        elif order.step == 7:
            order.address = message.text
            order.step += 1
            # order.active_sim = False
            order.save()
            if lan == 'uz':
                bot.send_message(message.from_user.id,
                             f"FISH: {order.full_name}\nTelefon raqam: {order.tel_number}\nTanlangan sim karta turi:  {order.sim_type}\nTanlangan sovg'a turi:  {order.gift}\nYashash manzili:  {order.address}" , reply_markup=secordary_markup_u)
                btn3_u = types.KeyboardButton('Tasdiqlash✅')
                secordary_markup_u.add(btn3_u)
                bot.send_message(message.from_user.id,
                             "Ma'lumotlar to'g'riligini tasdiqlang" , reply_markup=secordary_markup_u)
            if lan == 'en':
                bot.send_message(message.from_user.id,
                             f"Full name: {order.full_name}\nPhone number: {order.tel_number}\nChosen sim type:{order.sim_type}\nChosen gift: {order.gift}\nYour address: {order.address} ", reply_markup=secordary_markup_e)
                btn3_e = types.KeyboardButton('Confirm✅')
                secordary_markup_e.add(btn3_e)
                bot.send_message(message.from_user.id,
                             "Are your all credentials correct?" , reply_markup=secordary_markup_e)
            if lan == 'ru':
                bot.send_message(message.from_user.id,
                             f"Полное имя: {order.full_name}\nТелефонный номер: {order.tel_number}\nВыбранный тип сим-карты:{order.sim_type}\nВыбранный подарок: {order.gift}\nВаш адрес: {order.address} " , reply_markup=secordary_markup_r) 
                btn3_r = types.KeyboardButton('Подтвердить✅')
                secordary_markup_r.add(btn3_r)
                bot.send_message(message.from_user.id,
                             "Все ли ваши учетные данные верны?" , reply_markup=secordary_markup_r)



@bot.callback_query_handler(func=lambda call: True)
def call_data(call):
    client = Client.objects.get(user_id=call.from_user.id)
    lan = client.language
    order = SimOrder.objects.get(id=call.data)
    order.delete()

    
    if lan == 'uz':
        bot.edit_message_text(chat_id=call.from_user.id,
                         text=f"*Buyurtmangiz o'chirildi!*", message_id=call.message.id, parse_mode="Markdown")
    elif lan == 'en':
        bot.edit_message_text(chat_id=call.from_user.id,
                         text=f"*Your order is Ddeleted!*", message_id=call.message.id, parse_mode="Markdown")
    elif lan == 'ru':
        bot.edit_message_text(chat_id=call.from_user.id,
                         text=f"*Ваш заказ удален!*", message_id=call.message.id, parse_mode="Markdown")

def is_integer(n):
    try:
        float(n)
    except ValueError:
        return False
    else:
        return float(n).is_integer()


def cancel_func(message):
    client = Client.objects.get(user_id=message.from_user.id)
    lan = client.language
    order = SimOrder.objects.filter(owner=client, active_sim=True).first()
    secordary_markup_u = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1_u = types.KeyboardButton('Orqaga ↩️')
    btn2_u = types.KeyboardButton('Bekor qilish 🚫')
    secordary_markup_u.add(btn1_u, btn2_u)

    secordary_markup_e = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1_e = types.KeyboardButton('Back ↩️')
    btn2_e = types.KeyboardButton('Cancel 🚫')
    secordary_markup_e.add(btn1_e, btn2_e)

    secordary_markup_r = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1_r = types.KeyboardButton('Назад ↩️')
    btn2_r = types.KeyboardButton('Отмена 🚫')
    secordary_markup_r.add(btn1_r, btn2_r)
    
    if order.step == 1: 
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2) 
        if lan == 'uz':  
            btn2 = types.KeyboardButton('Bekor qilish 🚫')
            markup.add(btn2)
            bot.send_message(message.from_user.id, 'Ismingiz va familiyangizni kiriting 👨‍💼:', reply_markup=markup)
        elif lan == 'en':   
            btn2 = types.KeyboardButton('Cancel 🚫')
            markup.add(btn2)
            bot.send_message(message.from_user.id, 'Enter your last and first name 👨‍💼:', reply_markup=markup)
        elif lan == 'ru':   
            btn2 = types.KeyboardButton('Отмена 🚫')
            markup.add(btn2)
            bot.send_message(message.from_user.id, 'Введите свою фамилию и имя 👨‍💼:', reply_markup=markup)      
    
    elif order.step == 2:
        if lan == 'uz':
            bot.send_message(message.from_user.id, 'Telefon raqamingizni 9x xxx xx xx ko\'rinshda kiriting☎️:', reply_markup=secordary_markup_u)
        if lan == 'en':
            bot.send_message(message.from_user.id, 'Enter your phone number as shown: 9x xxx xx xx☎️:', reply_markup=secordary_markup_e)
        if lan == 'ru':
            bot.send_message(message.from_user.id, 'Введите свой номер телефона, как показано: 9x xxx xx xx☎️:', reply_markup=secordary_markup_r)
    
    elif order.step == 3: 
        markup_t = types.ReplyKeyboardMarkup(resize_keyboard=True)
        sim_options = SimCardOption.objects.all()
        for s in sim_options:
            markup_t.add(types.KeyboardButton(s.sim_option))
        if lan == 'uz':
            markup_t.add(btn1_u, btn2_u)
            bot.send_message(message.from_user.id,
                                     'Sim karta turini tanlang 🗂:', reply_markup=markup_t)
        elif lan == 'en':
            markup_t.add(btn1_e, btn2_e)
            bot.send_message(message.from_user.id,
                                     'Choose the simcard type 🗂:', reply_markup=markup_t)
        elif lan == 'ru':
            markup_t.add(btn1_r, btn2_r)
            bot.send_message(message.from_user.id,
                                     'Выберите тип сим-карты 🗂:', reply_markup=markup_t)      
      
    elif order.step == 4:
        markup_g = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        gifts = Gift.objects.all()
        for g in gifts:
            markup_g.add(types.KeyboardButton(g.name))
        if lan == 'uz':   
            markup_g.add(btn1_u, btn2_u)
            bot.send_message(
                    message.from_user.id, "Sim kartaga bonus sifatida sovg'aga ham ega bo'lasiz.\nSovga turini tanlang 🎁:", reply_markup=markup_g)
        elif lan == 'en':   
            markup_g.add(btn1_e, btn2_e)
            bot.send_message(
                    message.from_user.id, 'You can get a present as a bonus to a simcard.\nWhat do you want to get as a gift?\nChoose below 🎁:', reply_markup=markup_g)
        elif lan == 'ru':   
            markup_g.add(btn1_r, btn2_r)
            bot.send_message(
                    message.from_user.id, 'Вы можете получить подарок в качестве бонуса к симкарте.\nЧто вы хотите получить в подарок?\nВыберите ниже 🎁:', reply_markup=markup_g)   
    elif order.step == 5:
        if lan == 'uz':
            bot.send_message(message.from_user.id, "Passportingiz yoki ID kartangiz oldi qism rasmini jo'nating 🖼:", reply_markup=secordary_markup_u)
        elif lan == 'en':
            bot.send_message(message.from_user.id, "Send the frontside picture of your ID or passport 🖼:", reply_markup=secordary_markup_e)
        elif lan == 'ru':
            bot.send_message(message.from_user.id, "Отправьте фотографию своего удостоверения личности или паспорта на лицевой стороне 🖼:", reply_markup=secordary_markup_r)

    elif order.step == 6:
        if lan == 'uz':
            bot.send_message(message.from_user.id, "Passportingiz yoki ID kartangiz orqa qism rasmini jo'nating 🖼:", reply_markup=secordary_markup_u)
        elif lan == 'en':
            bot.send_message(message.from_user.id, "Send the backside picture of your ID or passport 🖼:", reply_markup=secordary_markup_e)
        elif lan == 'ru':
            bot.send_message(message.from_user.id, "Отправьте фотографию обратной стороны вашего удостоверения личности или паспорта 🖼:", reply_markup=secordary_markup_r)

    elif order.step == 7:
        if lan == 'uz': 
            bot.send_message(message.from_user.id, 'Manzilinginzi kiriting🏠:', reply_markup=secordary_markup_u)
        elif lan == 'en': 
            bot.send_message(message.from_user.id, 'Enter your address🏠:', reply_markup=secordary_markup_e)
        elif lan == 'ru': 
            bot.send_message(message.from_user.id, 'Введите свой адрес🏠:', reply_markup=secordary_markup_r)

bot.polling()

telebot.logger.setLevel(logging.DEBUG)