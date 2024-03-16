import api
import ui
import wx

from . import pytesseract as OCR


class TesseractOCRRecognizer:

    def __init__(
            self,
            x: int, y: int,
            width: int, height: int,
            language: str = None,
    ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.language: str = language

    def get_screen_image(self):
        bmp = wx.Bitmap(self.width, self.height)
        mem = wx.MemoryDC(bmp)
        mem.Blit(0, 0, self.width, self.height, wx.ScreenDC(), self.x, self.y)
        return bmp

    def image_to_text(self, image) -> str:
        wx.CallAfter(self.recognize, image, self.on_result)

    def recognize(self, image, on_result):
        text = OCR.image_to_string(image, self.language)
        on_result(text)

    def on_result(self, text):
        text = text if text else _("text not found")
        api.copyToClip(text, notify=False)
        ui.message(text)
