import customtkinter as ctk
import tkinter.filedialog as fd
import os
import shutil
import datetime

class App(ctk.CTk):

    def __init__(self):
        super().__init__()
        # this is like the window stuff
        self.title("Blank CTkinter GUI")
        self.geometry("400x300")
        self.selected_folder = None

        # frame to put buttons
        self.mode_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.mode_frame.pack(pady=40)

        # button for date sorting
        self.by_date_btn = ctk.CTkButton(
            self.mode_frame, text="By Date", command=self.mode_by_date
        )
        self.by_date_btn.pack(side="left", padx=10)

        # button for type sorting (not done yet)
        self.by_type_btn = ctk.CTkButton(
            self.mode_frame, text="By Type", command=self.mode_by_type
        )
        self.by_type_btn.pack(side="left", padx=10)

    def on_mode_selected(self):
        # hide the 2 buttons after i click one
        self.by_date_btn.pack_forget()
        self.by_type_btn.pack_forget()

    def mode_by_date(self):
        # what happens when i press the date button
        self.on_mode_selected()
        self.top_label = ctk.CTkLabel(self, text="Mode: By Date", font=("Arial", 20))
        self.top_label.pack(side="top", pady=(0, 10))

        # button to pick folder
        self.select_btn = ctk.CTkButton(self, text="Select Folder", command=self.select_folder)
        self.select_btn.pack(pady=10)

        # show which folder i picked
        self.folder_label = ctk.CTkLabel(self, text="No folder selected", wraplength=350)
        self.folder_label.pack(pady=5)

        # this label is for messages
        self.output_label = ctk.CTkLabel(self, text="")
        self.output_label.pack(pady=5)

        # button to actually sort, its off at first
        self.sort_btn = ctk.CTkButton(self, text="Sort", state="disabled", command=self.run_sort_by_date)
        self.sort_btn.pack(pady=10)

    def select_folder(self):
        # open a file thing to choose folder
        folder = fd.askdirectory()
        if folder:
            self.selected_folder = folder
            self.folder_label.configure(text=f"Selected: {folder}")
            self.output_label.configure(text="Ready. Click 'Sort' to start.")
            if hasattr(self, "sort_btn"):
                self.sort_btn.configure(state="normal")
        else:
            # if nothing was picked
            self.selected_folder = None
            self.folder_label.configure(text="No folder selected")
            self.output_label.configure(text="")
            if hasattr(self, "sort_btn"):
                self.sort_btn.configure(state="disabled")

    def run_sort_by_date(self):
        # checks if folder is ok
        if not self.selected_folder or not os.path.isdir(self.selected_folder):
            self.output_label.configure(text="Invalid folder. Please reselect.")
            return
        # shows message while it works
        self.output_label.configure(text="Sorting... This may take a moment.")
        self.update_idletasks()
        try:
            # does the sort
            output_path = self.sort_by_date(self.selected_folder)
            self.output_label.configure(text=f"Sorted folders created at: {output_path}")
        except Exception as e:
            # if something broke
            self.output_label.configure(text=f"Error: {e}")

    def sort_by_date(self, folder):
        # makes a folder to put sorted files in
        output_path = os.path.join(folder, "sorted_by_date")
        os.makedirs(output_path, exist_ok=True)
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            if os.path.isfile(file_path):
                try:
                    # get the time of the file
                    mtime = os.path.getmtime(file_path)
                    dt = datetime.datetime.fromtimestamp(mtime)
                    year = str(dt.year)
                    month = f"{dt.month:02d}"
                    # put file in year/month folder
                    target_dir = os.path.join(output_path, year, month)
                    os.makedirs(target_dir, exist_ok=True)
                    shutil.copy2(file_path, os.path.join(target_dir, filename))
                except Exception as e:
                    # if 1 file fails just print
                    print(f"Error sorting {filename}: {e}")
        return output_path

    def mode_by_type(self):
        # not done yet lol
        pass


if __name__ == "__main__":
    # some style stuff
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    app = App()
    app.mainloop()
