import customtkinter as ctk
import tkinter.filedialog as fd
import os
import shutil
import datetime
import yaml

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.move_mode = False
        self.title("File Sorter")
        self.geometry("420x400")
        self.selected_folder = None

        self.mode_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.mode_frame.pack(pady=20)

        self.by_date_btn = ctk.CTkButton(
            self.mode_frame, text="By Date", command=self.mode_by_date
        )
        self.by_date_btn.pack(side="left", padx=10)

        self.by_type_btn = ctk.CTkButton(
            self.mode_frame, text="By Type", command=self.mode_by_type
        )
        self.by_type_btn.pack(side="left", padx=10)

    def on_mode_selected(self):
        self.by_date_btn.pack_forget()
        self.by_type_btn.pack_forget()

    def mode_by_date(self):
        self.mode_frame.pack(pady=5)
        self.on_mode_selected()
        self.top_label = ctk.CTkLabel(self, text="Mode: By Date", font=("Arial", 20))
        self.top_label.pack(pady=(0, 0))

        self.move_switch = ctk.CTkSwitch(
            self, text="Move (remove originals)",
            command=lambda: setattr(self, "move_mode", bool(self.move_switch.get()))
        )
        self.move_switch.deselect()
        self.move_switch.pack(pady=(6, 0))

        self.select_btn = ctk.CTkButton(self, text="Select Folder", command=self.select_folder)
        self.select_btn.pack(pady=5)

        self.folder_label = ctk.CTkLabel(self, text="No folder selected", wraplength=350)
        self.folder_label.pack(pady=5)

        self.output_label = ctk.CTkLabel(self, text="")
        self.output_label.pack(pady=5)

        self.sort_btn = ctk.CTkButton(self, text="Sort by Date", state="disabled", command=self.run_sort_by_date)
        self.sort_btn.pack(pady=10)

    def mode_by_type(self):
        self.mode_frame.pack(pady=5)
        self.on_mode_selected()
        self.top_label = ctk.CTkLabel(self, text="Mode: By Type", font=("Arial", 20))
        self.top_label.pack(pady=(0, 0))

        self.move_switch = ctk.CTkSwitch(
            self, text="Move (remove originals)",
            command=lambda: setattr(self, "move_mode", bool(self.move_switch.get()))
        )
        self.move_switch.deselect()
        self.move_switch.pack(pady=(6, 0))

        self.select_btn = ctk.CTkButton(self, text="Select Folder", command=self.select_folder)
        self.select_btn.pack(pady=5)

        self.folder_label = ctk.CTkLabel(self, text="No folder selected", wraplength=350)
        self.folder_label.pack(pady=5)

        self.output_label = ctk.CTkLabel(self, text="")
        self.output_label.pack(pady=5)

        self.sort_btn = ctk.CTkButton(self, text="Sort by Type", state="disabled", command=self.run_sort_by_type)
        self.sort_btn.pack(pady=10)

    def select_folder(self):
        folder = fd.askdirectory()
        if folder:
            self.selected_folder = folder
            self.folder_label.configure(text=f"Selected: {folder}")
            self.output_label.configure(text="Ready. Click 'Sort' to start.")
            if hasattr(self, "sort_btn"):
                self.sort_btn.configure(state="normal")
        else:
            self.selected_folder = None
            self.folder_label.configure(text="No folder selected")
            self.output_label.configure(text="")
            if hasattr(self, "sort_btn"):
                self.sort_btn.configure(state="disabled")

    def run_sort_by_date(self):
        if not self.selected_folder or not os.path.isdir(self.selected_folder):
            self.output_label.configure(text="Invalid folder. Please reselect.")
            return
        self.output_label.configure(text="Sorting by date...")
        self.update_idletasks()
        try:
            output_path = self.sort_by_date(self.selected_folder, move=self.move_mode)
            self.output_label.configure(text=f"Sort finished. Result: {output_path}")
        except Exception as e:
            self.output_label.configure(text=f"Error: {e}")

    def run_sort_by_type(self):
        if not self.selected_folder or not os.path.isdir(self.selected_folder):
            self.output_label.configure(text="Invalid folder. Please reselect.")
            return
        self.output_label.configure(text="Sorting by type...")
        self.update_idletasks()
        try:
            output_path = self.sort_by_type(self.selected_folder, move=self.move_mode)
            self.output_label.configure(text=f"Sort finished. Result: {output_path}")
        except Exception as e:
            self.output_label.configure(text=f"Error: {e}")

    def sort_by_date(self, folder, move=False):
        filecount = 0
        output_path = os.path.join(folder, "sorted_by_date")
        os.makedirs(output_path, exist_ok=True)

        for root, _, files in os.walk(folder):
            for filename in files:
                file_path = os.path.join(root, filename)
                if output_path in file_path:
                    continue
                try:
                    mtime = os.path.getmtime(file_path)
                    dt = datetime.datetime.fromtimestamp(mtime)
                    year, month = str(dt.year), f"{dt.month:02d}"
                    target_dir = os.path.join(output_path, year, month)
                    os.makedirs(target_dir, exist_ok=True)
                    dst = os.path.join(target_dir, filename)
                    if move:
                        shutil.move(file_path, dst)
                    else:
                        shutil.copy2(file_path, dst)
                    filecount += 1
                except Exception as e:
                    print(f"Error sorting {filename}: {e}")

        print(f"Total files sorted by date: {filecount}")
        return output_path

    def sort_by_type(self, folder, move=False):
        filecount = 0
        output_path = os.path.join(folder, "sorted_by_type")
        os.makedirs(output_path, exist_ok=True)

        try:
            with open("rules.yaml", "r") as f:
                rules = yaml.safe_load(f)
        except Exception as e:
            print(f"Error loading rules.yaml: {e}")
            return output_path

        for root, _, files in os.walk(folder):
            for filename in files:
                file_path = os.path.join(root, filename)
                if output_path in file_path:
                    continue
                ext = os.path.splitext(filename)[1].lower()
                matched = False
                for folder_name, exts in rules.items():
                    if ext in exts:
                        target_dir = os.path.join(output_path, folder_name)
                        os.makedirs(target_dir, exist_ok=True)
                        dst = os.path.join(target_dir, filename)
                        if move:
                            shutil.move(file_path, dst)
                        else:
                            shutil.copy2(file_path, dst)
                        filecount += 1
                        matched = True
                        break
                if not matched:
                    others_dir = os.path.join(output_path, "Others")
                    os.makedirs(others_dir, exist_ok=True)
                    dst = os.path.join(others_dir, filename)
                    if move:
                        shutil.move(file_path, dst)
                    else:
                        shutil.copy2(file_path, dst)
                    filecount += 1

        print(f"Total files sorted by type: {filecount}")
        return output_path


if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    app = App()
    app.mainloop()
