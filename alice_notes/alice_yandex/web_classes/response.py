from .buttons import ButtonList
from ..images.image import Image


class Response:
    def __init__(self, text: str, end_session: bool = False, text_tts: str = None, buttons: ButtonList | None = None,
                 image: Image | None = None):
        self.text = text
        self.end_session = end_session
        self.text_tts = text_tts
        self.buttons = buttons
        self.image = image
        if buttons is None:
            self.buttons = ButtonList()
        if text_tts is None:
            self.text_tts = text
