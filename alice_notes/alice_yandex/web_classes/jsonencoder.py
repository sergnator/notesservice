import logging
from .response import Response
from flask import jsonify
from .request import RequestData


def to_json_from_class(response: Response, request: RequestData):
	logging.debug("start convert from class to json")

	response_json = dict()
	response_json["response"] = dict()
	response_json["session"] = request.session
	response_json["version"] = request.version

	logging.debug("session and version convert")

	response_json["response"]["text"] = response.text
	response_json["response"]["text_tts"] = response.text_tts

	logging.debug("start convert buttons")

	response_json["response"]["buttons"] = [
		{"title": button.title, "url": button.url, "payload": button.payload, "hide": button.hide} for button in
		response.buttons._list]
	for button in response_json['response']['buttons']:
		if button['url'] == "":
			del button["url"]
		if button["payload"] == dict():
			del button["payload"]

	logging.debug("convert buttons stop")

	response_json["response"]["end_session"] = response.end_session
	if response.image is not None:
		logging.debug("convert image")

		response_json["response"]["card"] = {}
		response_json["response"]["card"]["type"] = response.image.type
		response_json["response"]["card"]["title"] = response.image.title
		response_json["response"]["card"]["image_id"] = response.image.id

	logging.debug("convert end")
	logging.debug("sending")

	return jsonify(response_json)
