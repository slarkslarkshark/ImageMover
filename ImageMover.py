from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFile
from pathlib import Path
import shutil
import pickle
ImageFile.LOAD_TRUNCATED_IMAGES = True

class ImageMoverData:
    def __init__(self, history, main_path, path2, path3, path_ind_next, step, img_names):
        self.history = history
        self.main_path = main_path
        self.path2 = path2
        self.path3 = path3
        self.path_ind_next = path_ind_next
        self.step = step
        self.img_names = img_names

class ImageMover:
    def __init__(self, root, _main_path="", _path2="", _path3=""):
        self.root = root
        self.root.title("Image Mover")
        self.end = False
        
        self.selected_index = []
        self.img_labels = []

        self.imgs_frame = Frame(self.root, width=1300, height=700, borderwidth=0)
        self.buttons_frame = Frame(self.root, width=350, height=100, borderwidth=0)
        self.save_frame = Frame(self.root, width=1300, height=100, borderwidth=0)
        self.start_frame = Frame(self.root, width=700, height=700, borderwidth=0)

        self.path_ind_next = 0
        self.imgs = []
        self.imgs_with_frame = []
        self.img_names = []
        self.default_img = ImageTk.PhotoImage(Image.new('RGB', (224, 224), (255, 255, 255)))

        self.load_button = Button(self.start_frame, text="Загрузить", command=self.load)
        self.load_button.pack()

        self.path_label = Label(self.start_frame, text="Введите путь к основной папке:", font=("Arial", 10) )
        self.path_label.pack()
        main_path = StringVar() 
        main_path.set(_main_path) 
        self.main_path_entry = Entry(self.start_frame, width=50, textvariable=main_path)
        self.main_path_entry.pack()
        
        path2 = StringVar() 
        path2.set(_path2)  
        self.path_label2 = Label(self.start_frame, text="Введите путь к папке 2:", font=("Arial", 10))
        self.path_label2.pack()
        self.path_entry2 = Entry(self.start_frame, width=50, textvariable=path2)
        self.path_entry2.pack()
        
        self.path_label3 = Label(self.start_frame, text="Введите путь к папке 3:", font=("Arial", 10))
        self.path_label3.pack()
        path3 = StringVar() 
        path3.set(_path3) 
        self.path_entry3 = Entry(self.start_frame, width=50, textvariable=path3)
        self.path_entry3.pack()

        self.start_button = Button(self.start_frame, text="Начать", font=("Arial", 10, "bold"), command=lambda: self.start("start"))
        self.start_button.pack(pady=10)

        self.start_frame.pack()

        self.end_frame = Frame(self.root, width=500, height=500, borderwidth=0)
        self.count_label_end = Label(self.end_frame, text="Разметка закончена!", font=("Arial", 20))
        self.count_label_end.pack(pady=20)
        self.new_markup = Button(self.end_frame, text="Новая разметка", font=("Arial", 10, "bold"), command=self.new)
        self.new_markup.pack()
        self.save_button_end = Button(self.end_frame, text="Сохранить", font=("Arial", 10, "bold"), command=self.save)
        self.save_button_end.pack()
        self.cancel_button_end = Button(self.end_frame, text="Отмена", font=("Arial", 10, "bold"), command=self.cancel)
        self.cancel_button_end.pack()

    def new(self):
        self.end_frame.pack_forget()
        del self.history
        self.__init__(self.root)

    def load(self):
        file_path = filedialog.askopenfilename(filetypes=[("Pickle files", "*.pkl"), ("All files", "*.*")])
        if file_path:
            try:
                with open(file_path, 'rb') as f:
                    Data = pickle.load(f)
                    self.history = Data.history
                    self.main_path = Data.main_path
                    self.path2 = Data.path2
                    self.path3 = Data.path3
                    self.path_ind_next = Data.path_ind_next
                    self.step = Data.step
                    self.img_names = Data.img_names
                messagebox.showinfo("Успех", "Данные успешно загружены!")
                self.start("load")
            except Exception as exc:
                messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {exc}")

    def save(self):
        if self.selected_index or (self.step in self.history and self.history[self.step]):
            messagebox.showinfo("Ошибка", "Завершите или отмените действия на этом шаге!")
        else:
            file_path = filedialog.asksaveasfilename(defaultextension=".pkl",
                                                    filetypes=[("Pickle files", "*.pkl"), ("All files", "*.*")])
            if file_path:
                Data = ImageMoverData(self.history, self.main_path, self.path2, self.path3,
                                    self.path_ind_next, self.step, self.img_names)
                with open(file_path, 'wb') as f:
                    pickle.dump(Data, f)
                messagebox.showinfo("Успех", "Данные успешно сохранены!")

    def start(self, flag):
        self.start_frame.pack_forget()

        if flag == "start":
            self.step = 1
            self.history = dict()
            self.main_path = self.main_path_entry.get()
            self.path2 = self.path_entry2.get()
            self.path3 = self.path_entry3.get()

            if not self.main_path or not self.path2 or not self.path3:
                messagebox.showinfo("Ошибка", "Введите все пути до папок")
                self.__init__(self.root, self.main_path, self.path2, self.path3)
                return
            
            self.main_path = Path(self.main_path)
            self.path2 = Path(self.path2)
            self.path3 = Path(self.path3)

            if not self.main_path.is_dir() or not self.path2.is_dir() or not self.path3.is_dir():
                messagebox.showinfo("Ошибка", "Неверное имя директории")
                self.__init__(self.root)
                return

            self.img_names = list(map(lambda x: x.name, self.main_path.glob("*.jpg")))
            self.img_names += list(map(lambda x: x.name, self.main_path.glob("*.jpeg")))
            self.img_names += list(map(lambda x: x.name, self.main_path.glob("*.png")))
        
        self.imgs_frame.pack(side=TOP)
        self.buttons_frame.pack(side=BOTTOM)
        self.save_frame.pack(side=RIGHT)

        self.move_button2 = Button(self.buttons_frame, text=Path(self.path2).name, font=("Arial", 10, "bold"),
                                   command=lambda folder_index=2: self.move_img_to_folder(folder_index))
        self.move_button2.pack(side=LEFT, pady=10)

        self.next_button = Button(self.buttons_frame, text="Далее", font=("Arial", 10, "bold"), command=self.next)
        self.next_button.pack(side=LEFT, pady=10)

        self.move_button3 = Button(self.buttons_frame, text=Path(self.path3).name, font=("Arial", 10, "bold"),
                                   command=lambda folder_index=3: self.move_img_to_folder(folder_index))
        self.move_button3.pack(side=LEFT, pady=10)

        self.cancel_button = Button(self.buttons_frame, text="Отмена", font=("Arial", 10, "bold"), command=self.cancel)
        self.cancel_button.pack(side=LEFT, pady=10)

        self.save_button = Button(self.save_frame, text="Сохранить", command=self.save)
        self.save_button.pack(side=RIGHT)

        self.n2 = self.get_n(self.path2)
        self.n3 = self.get_n(self.path3)

        self.count_label = Label(self.root, text=0, font=("Arial", 10))

        self.load_next_imgs()

    def next(self):
        self.step += 1
        self.path_ind_next += 15
        self.load_next_imgs()

    def move_imgs_from_history(self):
        for file_path in self.history[self.step]:
                path = self.history[self.step][file_path].parent
                if path == self.history[self.step][file_path]:
                    self.n2 -= 1
                elif path == self.path3:
                    self.n3 -= 1

                shutil.move(self.history[self.step][file_path], file_path)
                print(f"Отмена: {self.history[self.step][file_path]} -> {file_path}")
        del self.history[self.step]

    def cancel(self):

        if self.path_ind_next == 0:
            return
        
        if self.step not in self.history.keys():
            self.step -= 1
            self.path_ind_next -= 15
            if self.step in self.history.keys():
                self.move_imgs_from_history()
        else:
            self.move_imgs_from_history()

        if self.end:
            self.end = False
            self.end_frame.pack_forget()
            self.imgs_frame.pack(side=TOP)
            self.buttons_frame.pack(side=BOTTOM)
            self.save_frame.pack(side=RIGHT)

        self.load_next_imgs()
 
    def draw_border(self, img, border_size=7):
        img_b = img.copy()
        draw = ImageDraw.Draw(img_b)
        width, height = img_b.size
        top_left = (0, 0)
        bottom_right = (width, height)
        draw.rectangle([top_left, bottom_right], outline="red", width=border_size)
        return img_b

    def load_next_imgs(self):
        self.imgs = []
        self.imgs_with_frame = []
        self.selected_index = []
        if self.path_ind_next >= len(self.img_names):
            for label in self.img_labels:
                label.destroy()
            self.count_label.destroy()

            self.imgs_frame.pack_forget()
            self.buttons_frame.pack_forget()
            self.save_frame.pack_forget()
            
            self.end_frame.pack()
            self.end = True
        else:
            self.path_ind = self.path_ind_next
            for i in range(self.path_ind_next, min(self.path_ind + 15, len(self.img_names))):
                img = Image.open(self.main_path / self.img_names[i])
                img = img.resize((224, 224))
                self.imgs.append(img)

            self.count_label.destroy()
            self.count_label = Label(self.root, text=len(self.img_names) - self.path_ind, font=("Arial", 10))
            self.count_label.pack(side=TOP)

            for label in self.img_labels:
                label.destroy()
            self.img_labels = []
            
            for i in range(min(15, len(self.imgs))):
                img = self.imgs[i]
                self.imgs_with_frame.append(ImageTk.PhotoImage(self.draw_border(img)))
                self.imgs[i] = ImageTk.PhotoImage(img)
                label = Label(self.imgs_frame, image=self.imgs[i])
                if i < 5:
                    label.grid(row=0, column=i)
                elif i < 10:
                    label.grid(row=1, column=i-5)
                else:
                    label.grid(row=2, column=i-10)
                label.bind(f"<Button-1>", lambda e, index=i: self.select_imgs(e, index))
                self.img_labels.append(label)

    def select_imgs(self, e, index):
        if self.imgs[index] != self.default_img:
            if index in self.selected_index:
                self.selected_index.remove(index)
                self.img_labels[index].config(image=self.imgs[index])
            else:
                self.selected_index.append(index)
                self.img_labels[index].config(image=self.imgs_with_frame[index])

    def get_n(self, path):
        names = [name.stem for name in path.glob("*.jpg")]
        names += [name.stem for name in path.glob("*.jpeg")]
        names += [name.stem for name in path.glob("*.png")]
        if len(names) == 0:
            return 1
        
        names = list(map(lambda x: int(x), names))
        return sorted(names)[-1] + 1

    def move_img_to_folder(self, folder_index):
        if self.selected_index:  
            for index in self.selected_index:

                if folder_index == 2:
                    n = self.n2
                    folder_path = self.path2
                    self.n2 += 1
                else:
                    n = self.n3
                    folder_path = self.path3
                    self.n3 += 1

                self.move_img(folder_path, index, n)
                self.img_labels[index].config(image=self.default_img)
                self.imgs[index] = self.default_img
                self.selected_index = []
            
    def move_img(self, target_folder, index, n):
        if self.step not in self.history.keys():
            self.history[self.step] = dict()

        img_name = self.img_names[self.path_ind + index]
        full_name = self.main_path / img_name
        new_full_name = target_folder / f"{n}.jpg"

        shutil.move(full_name, new_full_name)
        self.history[self.step][full_name] = new_full_name
        print(f"Перемещено: {full_name} -> {new_full_name}")

if __name__ == "__main__":
    root = Tk()
    app = ImageMover(root)
    root.mainloop()
