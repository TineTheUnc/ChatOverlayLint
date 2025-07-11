import asyncio, os,shutil,tkinter as tk,threading,pytchat
import tkinter.font as tkfont
from datetime import datetime
from tkinter import filedialog,messagebox
from appdirs import user_data_dir
from pytchat.core import PytchatCore
from  pytchat import  CompatibleProcessor
from pytchat.processors.default.processor import Chatdata

appname = "LiveChatApp"
appauthor = "Tine"

data_dir = user_data_dir(appname, appauthor)
os.makedirs(data_dir, exist_ok=True)
assert_dir = os.path.join(data_dir,"asset")
os.makedirs(assert_dir, exist_ok=True)
scopes = ["https://www.googleapis.com/auth/youtube.readonly"]


def _start_toplevel_move(event, widget):
    widget._drag_start_x = event.x
    widget._drag_start_y = event.y

def _set_geometry(widget,x,y):
    if (type(widget) is tk.Toplevel):
        widget.geometry(f"+{x}+{y}")
    else:
        _set_geometry(widget.master,x,y)

def _on_toplevel_move(event, widget):
    try:
        x = widget.winfo_pointerx() - widget._drag_start_x
        y = widget.winfo_pointery() - widget._drag_start_y
    except:
        widget._drag_start_x = event.x
        widget._drag_start_y = event.y
        x = widget.winfo_pointerx() - widget._drag_start_x
        y = widget.winfo_pointery() - widget._drag_start_y
    _set_geometry(widget,x,y)



def make_toplevel_draggable(widget):
    widget.bind("<Button-1>", lambda e: _start_toplevel_move(e, widget))
    widget.bind("<B1-Motion>", lambda e: _on_toplevel_move(e, widget))


def open_file():
    filepath = filedialog.askopenfilename(
        title="เลือกไฟล์ client_secret.json",
        filetypes=[("Text files", "*.json")]
    )
    if filepath:
        shutil.copy(filepath,os.path.join(assert_dir,"client_secret.json"))


class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Chat")
        self.chats = []
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.client: PytchatCore | None = None
        self.loop = asyncio.new_event_loop()
        self.loop.create_task(self.updater())
        threading.Thread(target=self.run_asyncio_loop, daemon=True).start()
        self.liveid_input = tk.Entry(self)
        self.start_button = tk.Button(self, text="Start",background="green", command=self.start)
        if hasattr(self, 'client') and self.client is not None:
            self.start_button.config(background="gray")
        self.toggle_button = tk.Button(self, text="Read Chat",background="green", command=self.read_chat)
        label = tk.Label(self,text="Live Id :")
        label.place(x=20, y=10)
        self.liveid_input.place(x=70, y=10)
        self.start_button.place(x=20, y=40)
        self.toggle_button.place(x=20, y=70)

    async def updater(self):
        try:
            while True:
                self.update()
                if self.client:
                    if self.client.is_alive():
                        await self.get_chat()
                    else:
                        try:
                            self.client.raise_for_status()
                        except pytchat.ChatDataFinished:
                            self.quit()
                        except Exception as e:
                            self.start()
                await asyncio.sleep(1/120)
        except asyncio.CancelledError:
            return

    async def get_chat(self):
        try:
            chatdata: Chatdata = self.client.get()
            if len(chatdata.items) == 0:
                return
            overlay = tk.Toplevel(self)
            overlay.geometry("300x150+300+200")
            overlay.overrideredirect(True)
            overlay.attributes('-topmost', True)  # อยู่หน้าตลอด
            overlay.attributes('-alpha', 0.9)  # โปร่งใสนิด ๆ
            overlay.configure(bg='green')
            overlay.attributes("-transparentcolor", "green")
            win_w, win_h = self.winfo_screenwidth(), 20 + (30 * len(chatdata.items))
            screen_h = self.winfo_screenheight()
            x = 0
            y = screen_h - win_h - 50
            overlay.geometry(f"{win_w}x{win_h}+{x}+{y - 50}")
            overlay.attributes('-topmost', True)
            i = 0
            async for chat in chatdata.async_items():
                bg = '#{:06X}'.format(chat.bgColor)
                if chat.type == "superChat":
                    msg = f"[{chat.amountString}] {chat.author.name} : {chat.message}"
                elif chat.type == "textMessage":
                    msg = f"{chat.author.name} : {chat.message}"
                elif chat.type == "newSponsor":
                    msg = f"New member {chat.author.name}"
                else:
                    continue
                self.chats.append(chat)
                if chat.author.isChatSponsor:
                    color = "#559900"
                elif chat.author.isChatOwner:
                    color = "#FFD600"
                elif chat.author.isChatModerator:
                    color = "#5E84F1"
                else:
                    color = "#FFFFFF"
                text = tk.Label(overlay, text=msg, fg=color, bg=bg, font=("Arial", 16))
                text.place(x=10, y=10 + (30 * i))
                i += 1
            self.after(5000, overlay.destroy)
        except Exception as e:
            messagebox.showerror("เกิดข้อผิดพลาด", str(e))

    def run_asyncio_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def start(self):
        if self.client:
            self.client.terminate()
        self.client = None
        if self.liveid_input.get() == "":
            messagebox.showerror("เกิดข้อผิดพลาด", "โปรดใส่ live id")
        else:
            self.chats = []
            self.start_button.config(background="gray")
            try:
                self.client = pytchat.create(self.liveid_input.get())
            except Exception as e:
                messagebox.showerror("เกิดข้อผิดพลาด", str(e))



    def close(self):
        if self.client:
            self.client.terminate()
        self.loop.stop()
        self.destroy()

    def read_chat(self):
        if hasattr(self, 'chat_list') and self.chat_list.winfo_exists():
            return
        self.chat_list = tk.Toplevel()
        win_w, win_h = self.winfo_screenwidth(), 20 + (30 * len(self.chats))
        self.chat_list.geometry(f"{win_w}x{win_h}")
        self.chat_list.title("Chat")

        scrollbar = tk.Scrollbar(self.chat_list, orient="vertical", borderwidth=0)
        scrollbar.configure(bg='white')
        scrollbar.pack(side="left", fill="y")

        # สร้าง listbox
        my_font = tkfont.Font(family="Arial", size=14, weight="bold")
        listbox = tk.Listbox(self.chat_list, yscrollcommand=scrollbar.set, borderwidth=0, highlightthickness=0,
                             font=my_font)
        listbox.pack(side="right", fill="both", expand=True)
        for chat in self.chats:
            if chat.type == "superChat":
                msg = f"{datetime.strptime(chat.datetime, "%Y-%m-%d %H:%M:%S").strftime("%I:%M %p")} || [{chat.amountString}] {chat.author.name} : {chat.message}"
            else:
                msg = f"{datetime.strptime(chat.datetime, "%Y-%m-%d %H:%M:%S").strftime("%I:%M %p")} || {chat.author.name} : {chat.message}"
            listbox.insert("end", msg)
        # เชื่อม scrollbar กับ listbox
        scrollbar.config(command=listbox.yview)
        make_toplevel_draggable(self.chat_list)
        make_toplevel_draggable(listbox)
        make_toplevel_draggable(scrollbar)







if __name__ == "__main__":
    app = App()
    app.mainloop()
