from itertools import cycle
import logging
import os

import api
import addonHandler
import config
import globalPluginHandler
import gui
import scriptHandler
from controlTypes import State
from languageHandler import getLanguage
import ui

from . import pytesseract as OCR

from .settings import TesseractOCRSettings

from .recognizer import TesseractOCRRecognizer


addonHandler.initTranslation()


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    scriptCategory = "realTesseractOCR"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(TesseractOCRSettings)
        self.set_ocr_path()

        self.lang = None
        self.languages = []

    def _languages_generator(self) -> str:
        current = False
        for lang in cycle(self.languages):
            if current:
                yield lang
            if lang == self.lang:
                current = True

    def set_ocr_path(self):
        ocr_path = config.conf["real_tesseract_ocr"].get("ocr_path", "")
        if ocr_path:
            OCR.pytesseract.tesseract_cmd = os.path.join(ocr_path, "tesseract")

    def set_language(self):
        self.set_ocr_path()
        self.languages = OCR.get_languages(config="")
        current_lang = getLanguage()
        for lang in self.languages:
            if current_lang in lang:
                self.lang = lang
                self.languages_generator = self._languages_generator()
                break

    def get_language(self):
        if not self.lang:
            try:
                self.set_language()
            except Exception:
                self.lang = None
        return self.lang

    @scriptHandler.script(
        description=_("switch supported language for recognize"),
        gesture="kb:NVDA+ALT+I"
    )
    def script_switch_language(self, gesture):
        if not self.lang:
            self.get_language()
        if self.languages:
            self.lang = next(self.languages_generator)
            text = ": ".join([_("current recognition language"), self.lang])
            ui.message(text)

    @scriptHandler.script(
        description=_("Say OCR image"),
        gesture="kb:NVDA+I"
    )
    def script_image_to_string(self, gesture):
        obj = api.getNavigatorObject()
        if State.OFFSCREEN in obj.states:
            ui.message(_("off screen"))
            return

        try:
            x, y, width, height = obj.location
        except Exception:
            ui.message(_("object has no location"))
            return

        lang = self.get_language()
        ocr = TesseractOCRRecognizer(x, y, width, height, lang)
        try:
            image = ocr.get_screen_image()
            ocr.image_to_text(image)
        except Exception as error:
            logging.error(error, exc_info=True)
            ui.message(_("recognition error occurred"))
