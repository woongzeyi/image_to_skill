"""The module where the main entry point of the program lives. """

from os import makedirs, listdir, getcwd
from os.path import isfile, join, splitext
from typing import List
from filetype import is_image

# Remove . when testing module
from .image_processor import ImageDetails
from .code_generation import CodeGenerator, Mode, ParticleType
from .gui import Ui_MainWindow

# New module import
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from webbrowser import open as webopen
from sys import argv as sysArgs
from sys import exit as sysExit


class MyWindow(QMainWindow):

    def __init__(self):
        super(MyWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.showpath = getcwd() + '\\images'
        self.ui.pathLine.setText(self.showpath)
        self.ui.pathLine.setReadOnly(1)

    def checkConfig(self):

        parti_type = self.ui.typeEdit.text()
        interval = self.ui.intervalEdit.text()
        parti_size = self.ui.sizeEdit.text()
        forward = self.ui.forwardEdit.text()
        side = self.ui.sideEdit.text()
        base_y = self.ui.yEdit.text()

        if (parti_type == '' or interval == '' or parti_size == '' or forward == '' or side == '' or base_y == ''
        ):
            return True
        else:
            return False

    async def start(self):

        if self.checkConfig():
            QMessageBox.critical(self, 'Config Missing', 'Please fill up all config before click start button')
        else:
            if self.ui.ht_radio.isChecked():
                mode = "HR"
                await self.main(mode)
            elif self.ui.vt_radio.isChecked():
                mode = "VT"
                await self.main(mode)
            else:
                QMessageBox.critical(self, 'Mode Invalid', 'Please choose a mode')

    def help(self):
        webopen('https://github.com/woongzeyi/image_to_skill#image_to_skill')

    def help_particle(self):
        webopen('https://git.mythiccraft.io/mythiccraft/MythicMobs/-/wikis/skills/effects/particles/types')

    def main(self, Main_mode):
        """The main entry point of the program. """

        # Images need to be put into the `./images` directory
        images_directory: str = getcwd() + "/images"
        makedirs(images_directory, exist_ok=True)

        # Opening a non-image file with PIL will throw an exception
        images: List[str] = [
            f
            for f in listdir(images_directory)
            if isfile(join(images_directory, f))
            if is_image(join(images_directory, f))
        ]
        print(f"Images found: \n{images}\n")

        if images:
            for i in images:
                print(f"<< {i} >>")
                with open(
                        join(images_directory, splitext(i)[0] + ".yml"),
                        'w',
                        encoding="utf-8"
                ) as yaml_file:
                    generator = CodeGenerator(
                        mode=Mode(Main_mode),
                        particle_type=ParticleType(self.ui.typeEdit.text()),
                        particle_interval=float(self.ui.intervalEdit.text()),
                        particle_size=float(self.ui.sizeEdit.text()),
                        base_forward_offset=float(self.ui.forwardEdit.text()),
                        base_side_offset=float(self.ui.sideEdit.text()),
                        base_y_offset=float(self.ui.yEdit.text()),
                        image=ImageDetails.from_path(join(images_directory, i))
                    )
                    for line in generator.generate_code():
                        yaml_file.write(line)
            else:
                QMessageBox.critical(self, 'No File Found', 'Execution ended due to no image found.')

    def get_help(self):
        webopen('https://github.com/woongzeyi/image_to_skill#image_to_skill')

    def get_help_particle(self):
        webopen('https://git.mythiccraft.io/mythiccraft/MythicMobs/-/wikis/skills/effects/particles/types')


if __name__ == "__main__":
    app = QApplication(sysArgs)
    window = MyWindow()
    window.show()
    sysExit(app.exec_())
