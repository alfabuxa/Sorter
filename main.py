import customtkinter as ctk
# This code is already properly organized in the App class below
# The setup calls should remain in the if __name__ == "__main__" block

class App(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("Blank CTkinter GUI")
        self.geometry("400x300")

        # Create a frame to hold the mode selection buttons
        self.mode_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.mode_frame.pack(pady=40)

        # "By Date" button
        self.by_date_btn = ctk.CTkButton(
            self.mode_frame, text="By Date", command=self.on_mode_selected
        )
        self.by_date_btn.pack(side="left", padx=10)

        # "By Type" button
        self.by_type_btn = ctk.CTkButton(
            self.mode_frame, text="By Type", command=self.on_mode_selected
        )
        self.by_type_btn.pack(side="left", padx=10)

    def on_mode_selected(self):
        self.by_date_btn.pack_forget()
        self.by_type_btn.pack_forget()


if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    app = App()
    app.mainloop()