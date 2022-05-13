"""The module where the main entry point of the program lives. """

from os import makedirs, listdir, getcwd
from os.path import isfile, join, splitext
from typing import List
from filetype import is_image
from .image_processor import ImageDetails
from .code_generation import CodeGenerator, Mode, ParticleType

from tkinter import Tk, StringVar, DISABLED, Listbox, END
from tkinter.ttk import Button, Label, Entry, Frame
from tkinter.messagebox import showinfo, showerror
from webbrowser import open as webopen


class MyWindow():

    def __init__(self):
        super(MyWindow, self).__init__()
        self.mode_option = {'Horizontal': 'HR', 'Vertical': 'VT'}
        self.root = Tk()
        self.root.title("ImageToSkill")
        self.root.wm_title("ImageToSkill")

        try:
            from ctypes import windll
            windll.shcore.SetProcessDpiAwareness(1)
            ScaleFactor = windll.shcore.GetScaleFactorForDevice(0)
            self.root.tk.call('tk', 'scaling', ScaleFactor / 75)
        except:
            pass

        S_WIDTH = 775
        S_HEIGHT = 250
        self.root.overrideredirect(False)
        self.root.geometry(str(S_WIDTH) + 'x' + str(S_HEIGHT) + '+'
                           + str((self.root.winfo_screenwidth() - S_WIDTH) // 2) + '+' +
                           str((self.root.winfo_screenheight() - S_HEIGHT) // 2 - 18))
        self.root.resizable(False, False)

        self.frame1 = Frame(self.root)
        self.frame1.grid(row=0, column=0)

        self.label1 = Label(self.frame1, text="CurrentDirectory:", font=('Arial', 11))
        self.label1.grid(row=0, column=0, pady=5, padx=5)

        self.var1 = StringVar()
        self.entry1 = Entry(self.frame1, font=('Arial', 11), textvariable=self.var1, width=62)
        self.entry1.grid(row=0, column=1)
        self.var1.set(getcwd() + '/images')
        self.entry1.config(state=DISABLED)

        # 开始执行命令按钮
        self.start_btn = Button(self.frame1, text="Start", width=8, takefocus=False, command=self.main)
        self.start_btn.grid(row=1, column=1)

        self.config_frame = Frame(self.root)
        self.config_frame.grid(row=1, column=0)

        self.text = Label(self.config_frame, text="Config", font=('Arial', 11))
        self.text.grid(row=0, column=0, pady=5)

        self.list = Listbox(self.config_frame, width=12, height=5, font=("Arial", 11), takefocus=False)
        self.list.grid(row=1, column=0, padx=5)
        self.list.insert(END, "Horizontal")
        self.list.insert(END, "Vertical")

        self.frame_inside_frame = Frame(self.config_frame)
        self.frame_inside_frame.grid(row=1, column=1)

        self.parti_type_label = Label(self.frame_inside_frame, text="ParticleType:", font=('Arial', 11))
        self.parti_type_label.grid(row=0, column=0)

        self.parti_type_var = StringVar()
        self.parti_type_entry = Entry(self.frame_inside_frame, width=15, font=('Arial', 11),
                                      textvariable=self.parti_type_var)
        self.parti_type_entry.grid(row=0, column=1, padx=10)

        self.parti_interval_label = Label(self.frame_inside_frame, font=('Arial', 11), text='ParticleInterval:')
        self.parti_interval_label.grid(row=0, column=2)

        self.parti_interval_var = StringVar()
        self.parti_interval_entry = Entry(self.frame_inside_frame, font=('Arial', 11), width=15,
                                          textvariable=self.parti_interval_var)
        self.parti_interval_entry.grid(row=0, column=3, padx=5)

        self.parti_size_label = Label(self.frame_inside_frame, font=('Arial', 11), text='ParticleSize:')
        self.parti_size_label.grid(row=1, column=0, pady=5)

        self.parti_size_var = StringVar()
        self.parti_size_entry = Entry(self.frame_inside_frame, font=('Arial', 11), width=15,
                                      textvariable=self.parti_size_var)
        self.parti_size_entry.grid(row=1, column=1, padx=10)

        self.forward_offset_label = Label(self.frame_inside_frame, font=('Arial', 11), text='BaseForwardOffset:')
        self.forward_offset_label.grid(row=1, column=2)

        self.forward_offset_var = StringVar()
        self.forward_offset_entry = Entry(self.frame_inside_frame, font=('Arial', 11), width=15,
                                          textvariable=self.forward_offset_var)
        self.forward_offset_entry.grid(row=1, column=3, pady=5)

        self.side_offset_label = Label(self.frame_inside_frame, font=('Arial', 11), text='BaseSideOffset:')
        self.side_offset_label.grid(row=2, column=0)

        self.side_offset_var = StringVar()
        self.side_offset_entry = Entry(self.frame_inside_frame, width=15, font=('Arial', 11),
                                       textvariable=self.side_offset_var)
        self.side_offset_entry.grid(row=2, column=1, padx=10)

        self.y_offset_label = Label(self.frame_inside_frame, font=('Arial', 11), text="BaseYOffset:")
        self.y_offset_label.grid(row=2, column=2)

        self.y_offset_var = StringVar()
        self.y_offset_entry = Entry(self.frame_inside_frame, font=('Arial', 11), width=15,
                                    textvariable=self.y_offset_var)
        self.y_offset_entry.grid(row=2, column=3, padx=5)

        # 帮助按钮
        self.help_btn = Button(self.frame_inside_frame, text='Help', width=8, takefocus=False, command=self.get_help)
        self.help_btn.grid(row=3, column=1, pady=5)

        self.particle_help = Button(self.frame_inside_frame, text='ParticleHelp', width=11, takefocus=False,
                                    command=self.get_help_particle)
        self.particle_help.grid(row=3, column=2)

        self.root.mainloop()

    def main(self):
        """The main entry point of the program. """

        # Get config from gui
        try:
            self.main_mode = self.mode_option[self.list.get('anchor')]
        except KeyError:
            self.main_mode = ''
        self.type_particle = self.parti_type_var.get()
        self.interval_particle = self.parti_interval_var.get()
        self.size_particle = self.parti_size_var.get()
        self.base_forward = self.forward_offset_var.get()
        self.base_side = self.side_offset_var.get()
        self.base_y = self.y_offset_var.get()

        # Images need to be put into the `./images` directory
        images_directory: str = getcwd() + "/images"
        makedirs(images_directory, exist_ok=True)

        if self.main_mode == '' or self.type_particle == '' or self.interval_particle == '':
            showerror('Config Missing', 'Please fill up all the config blank or choose any mode in the listbox!')
        elif self.size_particle == '' or self.base_forward == '' or self.base_side == '' or self.base_y == '':
            showerror('Config Missing', 'Please fill up all the config blank or choose any mode in the listbox!')
        else:

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
                            mode=Mode(self.main_mode),
                            particle_type=ParticleType(self.type_particle),
                            particle_interval=float(self.interval_particle),
                            particle_size=float(self.size_particle),
                            base_forward_offset=float(self.base_forward),
                            base_side_offset=float(input(self.base_side)),
                            base_y_offset=float(self.base_y),
                            image=ImageDetails.from_path(join(images_directory, i))
                        )
                        for line in generator.generate_code():
                            yaml_file.write(line)
            else:
                showinfo("ImageNoFound", 'Execution ended due to no image found.')

    def get_help(self):
        webopen('https://github.com/woongzeyi/image_to_skill#image_to_skill')

    def get_help_particle(self):
        webopen('https://git.mythiccraft.io/mythiccraft/MythicMobs/-/wikis/skills/effects/particles/types')


if __name__ == "__main__":
    # main()
    MyWindow()
