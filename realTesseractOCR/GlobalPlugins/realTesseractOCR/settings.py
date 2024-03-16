import addonHandler
import config
import gui
from gui.settingsDialogs import SettingsPanel

import wx


addonHandler.initTranslation()


confspec = {
    "ocr_path": "string(default='')",
}
config.conf.spec["real_tesseract_ocr"] = confspec


class TesseractOCRSettings(SettingsPanel):
    title = "realTesseractOCR"

    def makeSettings(self, settingsSizer):
        settings_sizer_helper = gui.guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
        group_sizer = wx.StaticBoxSizer(wx.VERTICAL, self, label=_("Path to installed Tesseract-OCR"))
        group_box = group_sizer.GetStaticBox()
        group_helper = settings_sizer_helper.addItem(gui.guiHelper.BoxSizerHelper(self, sizer=group_sizer))

        browse_text = _("Browse...")
        dir_dialog_title = _("Select a directory")
        directory_path_helper = gui.guiHelper.PathSelectionHelper(group_box, browse_text, dir_dialog_title)
        directory_entry_control = group_helper.addItem(directory_path_helper)
        
        self.ocr_path = directory_entry_control.pathControl
        self.ocr_path.Value = config.conf["real_tesseract_ocr"].get("ocr_path", "")

    def onSave(self):
        config.conf["real_tesseract_ocr"]["ocr_path"] = self.ocr_path.GetValue()
