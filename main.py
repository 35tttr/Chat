import threading
from socket import *
from customtkinter import *

class MainWindow(CTk):
    def __init__(self):
        super().__init__()
        self.title("Онлайн Чат")
        self.geometry("700x500")
        self.resizable(False, False)

        self.username = "Анонім"

        try:
            self.sock = socket(AF_INET, SOCK_STREAM)
            self.sock.connect(("0.tcp.eu.ngrok.io", 18095))
            threading.Thread(target=self.receive_messages, daemon=True).start()
        except Exception as e:
            print("Не вдалося підключитися:", e)

        self.menu_visible = False
        self.animating = False
        self.menu_max_width = 200
        self.current_width = 0

        self.toggle_button = CTkButton(self, text="☰", width=30, command=self.toggle_menu)
        self.toggle_button.place(x=0, y=0)
        self.toggle_button.lift()

        self.menu_frame = CTkFrame(self, width=self.current_width, height=500)
        self.menu_frame.place(x=0, y=0)
        self.menu_frame.pack_propagate(False)

        self.name_label = CTkLabel(self.menu_frame, text="Ім’я користувача", font=("Arial", 16))
        self.name_entry = CTkEntry(self.menu_frame, placeholder_text="Введіть ім’я", width=150)
        self.save_button = CTkButton(self.menu_frame, text="Зберегти", width=150, height=40, command=self.save_name)
        self.username_label = CTkLabel(self.menu_frame, text=f"Поточне ім’я: {self.username}")

        self.ad_label = CTkLabel(self.menu_frame, text="Купуйте Premium більше можливостей!", text_color="red", font=("Arial", 14, "bold"), wraplength=180, justify="center")
        self.ad_button = CTkButton(self.menu_frame, text="Дізнатися більше", width=150, fg_color="orange", command=self.premium)

        self.ad1_label = CTkLabel(self.menu_frame, text="Найкраща програма ОНЛАЙН ЧАТ! Рекламуй отримай +1 день Premium", text_color="green", font=("Arial", 14, "bold"), wraplength=180, justify="center")

        self.name_label.pack(pady=10)
        self.name_entry.pack(pady=10)
        self.save_button.pack(pady=5)
        self.username_label.pack(pady=10)
        self.ad_label.pack(pady=20)
        self.ad_button.pack(pady=5)
        self.ad1_label.pack(pady=20)

        self.chat_frame = CTkScrollableFrame(self, width=660, height=400)
        self.chat_frame.place(x=35, y=40)

        self.message_entry = CTkEntry(self, placeholder_text="Введіть повідомлення...", width=550, height=40)
        self.message_entry.place(x=35, y=450)

        self.send_button = CTkButton(self, text="Надіслати", width=100, height=40, command=self.send_message)
        self.send_button.place(x=600, y=450)

        self.update_layout()


    def premium(self): 
        self.display_message("Premium версія надає більше можливостей!")
        self.display_message("Ви можете отримати Premium версію")
        
        

    def save_name(self):
        self.username = self.name_entry.get().strip() or "Анонім"
        self.username_label.configure(text=f"Поточне ім’я: {self.username}")

    def toggle_menu(self):
        if self.animating:
            return
        self.menu_visible = not self.menu_visible
        self.animating = True
        self.target_width = self.menu_max_width if self.menu_visible else 0
        self.animate_menu()

    def animate_menu(self):
        step = 10 if self.menu_visible else -10
        self.current_width += step
        if (self.menu_visible and self.current_width <= self.target_width) or \
           (not self.menu_visible and self.current_width >= self.target_width):
            self.menu_frame.configure(width=self.current_width)
            self.update_layout()
            self.after(10, self.animate_menu)
        else:
            self.current_width = self.target_width
            self.menu_frame.configure(width=self.current_width)
            self.update_layout()
            self.animating = False

    def update_layout(self):
        menu_width = self.current_width
        self.chat_frame.place(x=menu_width + 5, y=40)
        self.chat_frame.configure(width=660 - menu_width, height=400)

        self.message_entry.place(x=menu_width + 5, y=450)
        self.message_entry.configure(width=550 - menu_width)
        self.toggle_button.place(x=menu_width + 5, y=0)
        self.send_button.place(x=600, y=450)

    def send_message(self):
        message = self.message_entry.get()
        if message:
            self.display_message(f"Ви: {message}")
            try:
                data = f"TEXT@{self.username}@{message}\n"
                self.sock.sendall(data.encode('utf-8'))
            except:
                self.display_message("[Помилка] Не вдалося надіслати повідомлення")
            self.message_entry.delete(0, 'end')

    def receive_messages(self):
        buffer = ""
        while True:
            try:
                chunk = self.sock.recv(4096)
                if not chunk:
                    break
                buffer += chunk.decode()

                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    self.handle_message(line.strip())
            except:
                break
        self.sock.close()

    def handle_message(self, line):
        parts = line.split("@")
        if parts[0] == "TEXT" and len(parts) >= 3:
            author, message = parts[1], parts[2]
            self.display_message(f"{author}: {message}")

    def display_message(self, text):
        label = CTkLabel(self.chat_frame, text=text, anchor="w", justify="left", wraplength=600)
        label.pack(fill="x", padx=5, pady=2)


set_appearance_mode("light")
app = MainWindow()
app.mainloop()
