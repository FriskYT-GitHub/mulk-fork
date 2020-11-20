
# -*- coding: utf-8 -*-
import random, time, os
from vk_api import VkApi
from vk_api import VkUpload
import datetime, random, json
from PIL import Image, ImageFont, ImageDraw
from vk_api.longpoll import VkLongPoll, VkEventType

isBusy = False
def main(alert = False):
	token = "ccedf2d543bb4c485af86ce978f6ff310cee2cc50ad615e61b1218b303d81a25d3b820678cae7826b690c"
	vk_session = VkApi(token = token)
	upload = VkUpload(vk_session)

	session_api = vk_session.get_api()
	longpoll = VkLongPoll(vk_session)

	def getname(user_id):
		user_get = vk_session.get_api().users.get(user_ids = (user_id))
		user_get = user_get[0]
		firstname = user_get["first_name"]
		lastname = user_get["last_name"]
		return {"firstname": firstname, "lastname": lastname}

	def peermsg(peer_id, message):
		vk_session.method("messages.send", {"peer_id": peer_id, "message": message, "random_id": random.randint(0, 2048)})

	def message(user_id, message, forward = False):
		context = {"user_id": user_id, "message": message, "random_id": random.randint(0, 2048)}
		"""if forward
		context.update({forward_messages = event.message_id})"""

		vk_session.method("messages.send", context)

	def photomsg(peer_id, photos, message = ""):
		attachments = []
		upload_image = upload.photo_messages(photos = photos)[0]
		attachments.append("photo{}_{}".format(upload_image["owner_id"], upload_image["id"]))
		context = {"peer_id": peer_id, 'random_id': random.randint(0, 2048),
			"attachment": ",".join(attachments)}
		context.update(message = message)
		vk_session.method("messages.send", context)


	def licgen(fullname, catgirl, message = [""], user_id = ""):
		licenses = ["azuki", "chocola", "coconut", "vanilla", "maple", "cinnamon", "milk", "shigure", "kashou"]
		if (catgirl not in licenses):
			peermsg(user_id, "Извини, я искала везде, но не нашла такой лицензии. Возможно, ты неправильно написал имя кошечки?")
		else:

	        	licPath = "license-" + str(event.user_id) + ".jpg"
			if catgirl == "kashou":
				image = Image.open("kashou/0.jpg")
			elif catgirl == "shigure" or catgirl == "milk":
				image = Image.open(catgirl + "/{}.jpg".format(str(random.randint(0, 1))))
			else:
				image = Image.open(catgirl + "/{}.jpg".format(str(random.randint(0, 2))))

			if message != [""]:
				namelist = message
				del namelist[0]
				del namelist[0]
				fullname = ""
				for count in range(len(namelist)):
					fullname += " " + namelist[count]

			if len(fullname) < 21:
				now = datetime.datetime.now()
				issuedate = now.strftime("%d.%m.%Y")
				draw = ImageDraw.Draw(image)
				font = ImageFont.truetype("font.otf", 50)
				draw.text((450, 187), fullname, font = font, fill = (245, 245, 245))
				draw.text((685, 255), issuedate, font = font, fill = (245, 245, 245))
				image.save(licPath, optimize = 1)
				return True
			else:
				peermsg(event.peer_id, """Прости! Твое имя слишком длинное, чтобы уместить его на лицензии.
Пожалуйста, напиши сокращенное имя (Владислав => Влад) вместе с коммандой""")
				peermsg(event.peer_id, ("Пример: /licgen " + catgirl + " Влад Ефремов\nВместо /licgen " + catgirl))
				return False
	if alert == True:
		peermsg(389769778, """Произошла критическая ошибка на сервере!
			Свяжитесь с [friskyt|программистом] вашего бота.""")
	for event in longpoll.listen():
		if event.type == VkEventType.MESSAGE_NEW and event.to_me:
			message = event.text
			if message.lower().startswith("/licgen "):
				name = getname(event.user_id)
				name["firstname"] + " " + name["lastname"]
				if len(message.split()) < 3:
					if licgen((name["firstname"] + " " + name["lastname"]),
						message.lower().split()[1], user_id = event.user_id):
						photomsg(event.peer_id, "license-" + str(event.user_id) + ".jpg")
						os.remove("license-" + str(event.user_id) + ".jpg")
				else:
					if licgen((name["firstname"] + " " + name["lastname"]),
						message.lower().split()[1], (message.split())):
						photomsg(event.peer_id, "license-" + str(event.user_id) + ".jpg")
						os.remove("license-" + str(event.user_id) + ".jpg")

try:
	main()
except:
	main()
