import requests
import logging
from datetime import datetime

class Image:
	def __init__(self, id_of_image, _loader):
		if not isinstance(_loader, ImageLoader):
			raise TypeError(f"Got {type(_loader)} _loader insted ImageLoader")
		self.id = id_of_image
		self.title = "Картинка"
		self.type = "BigImage"
		self.__loader: ImageLoader = _loader
		logging.debug("image created")

	def delete(self):
		self.__loader.delete_image(self)


class ImageLoader:
	def __init__(self, token, id_of_skill):
		self.token = token
		self.id = id_of_skill
		self.__all_images: list[Image] = []

	def load_by_id(self, id_image):
		logging.debug("start load image by id")
		res = requests.get(f'https://dialogs.yandex.net/api/v1/skills/{self.id}/images',
		                   headers={"Authorization": "OAuth " + self.token}).json()
		for img in res["images"]:
			if img["id"] == id_image:
				logging.debug("load complete")
				return Image(id_image, self)
		logging.debug("load fail")
	def load_file(self, path):
		logging.debug("start load image by filename")
		res = requests.post(f'https://dialogs.yandex.net/api/v1/skills/{self.id}/images',
		                    files={"file": open(path, 'rb')},
		                    headers={"Authorization": "OAuth " + self.token})
		logging.debug("load complete")
		img = Image(res.json()['image']['id'], self)
		self.__all_images.append(img)
		return img

	def load_url(self, url):
		res = requests.post(f'https://dialogs.yandex.net/api/v1/skills/{self.id}/images', json={"url": url},
		                    headers={"Authorization": "OAuth " + self.token}) # TODO: not work

	def delete_image(self, img: Image):
		res = requests.delete(
			f"https://dialogs.yandex.net/api/v1/skills/{self.id}/images/{img.id}",
			headers={"Authorization": "OAuth " + self.token})
		logging.debug("image delete: " + str(img.id))
		return res.json()

	def clear(self):
		logging.debug("clear start")
		for image in self.__all_images:
			image.delete()
		logging.debug("clear stop")

