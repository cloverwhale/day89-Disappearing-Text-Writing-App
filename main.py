from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter.ttk import Progressbar

TYPING_SECS = 60
IDLE_SECS = 5
total_timer = None
idle_timer = None


def idle_countdown(count):
    global idle_timer
    if count > 0:
        idle_timer = root.after(1000, idle_countdown, count - 1)
        lb_erase_timer.config(text=f"Countdown:{count}")
    else:
        lb_erase_timer.config(text=f"Countdown:0")
        text_typing_area.delete(1.0, END)
        text_typing_area.insert(END, "Sorry, your progress is lost.")
        disable_ui()
        stop_timer()


def reset_idle_timer(event):
    global idle_timer
    root.after_cancel(idle_timer)
    idle_countdown(IDLE_SECS)


def progress(count):
    global total_timer
    if count > 0:
        total_timer = root.after(1000, progress, count - 1)
        progress_bar['value'] = 100 - count / TYPING_SECS * 100
    else:
        progress_bar['value'] = 100
        disable_ui()
        stop_timer()
        btn_save.config(state="active")
        lb_info.config(text="You can save your progress now.")


def start(event):
    lb_info.config(text="Do not stop typing or your progress will be lost.")
    text_typing_area.config(state="normal")
    text_typing_area.unbind("<KeyPress>")
    text_typing_area.bind("<KeyRelease>", reset_idle_timer)
    idle_countdown(IDLE_SECS)
    progress(TYPING_SECS)


def reset():
    stop_timer()
    text_typing_area.config(state="normal")
    text_typing_area.delete(1.0, END)
    text_typing_area.config(state="disabled")
    text_typing_area.bind("<KeyPress>", start)
    progress_bar['value'] = 0
    btn_save.config(state="disabled")
    lb_info.config(text="")
    lb_erase_timer.config(text=f"Countdown:{IDLE_SECS}")


def disable_ui():
    text_typing_area.config(state="disabled")
    text_typing_area.unbind("<KeyRelease>")


def stop_timer():
    global total_timer
    global idle_timer
    root.after_cancel(total_timer)
    root.after_cancel(idle_timer)


def save_file():
    text_file = filedialog.asksaveasfilename(initialdir="./", title="Save file",
                                             filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
    text_to_save = text_typing_area.get(1.0, END)
    with open(text_file, "w") as f:
        f.write(text_to_save)
    messagebox.showinfo(message="Your file is saved.")


root = Tk()
root.title("Disappearing Text Editor")

lb_erase_timer = Label(root, text=f"Countdown:{IDLE_SECS}")
lb_erase_timer.grid(row=0, column=0, sticky="w", padx=10, pady=10)

lb_info = Label(root, text="")
lb_info.grid(row=0, column=1, sticky="e", padx=5, pady=10)

progress_bar = Progressbar(root, orient=HORIZONTAL, length=200, mode='determinate')
progress_bar.grid(row=1, column=0, sticky="ew", columnspan=2)

text_typing_area = Text(root, width=90, height=15, spacing2=5,
                        wrap="word", font=("Arial", 16, "normal"),
                        padx=5, pady=5)
text_typing_area.grid(row=2, column=0, columnspan=2)
text_typing_area.bind("<KeyPress>", start)
scroll_v = Scrollbar(root, orient=VERTICAL, command=text_typing_area.yview)
scroll_v.grid(row=2, column=2, sticky="ns")
text_typing_area["yscrollcommand"] = scroll_v.set

btn_frame = Frame(root)
btn_frame.grid(row=3, column=0, sticky="w", padx=10, pady=5)

btn_restart = Button(btn_frame, text="Reset", command=reset)
btn_restart.grid(row=0, column=0, sticky="e", pady=10)
btn_save = Button(btn_frame, text="Save", command=save_file, state="disabled")
btn_save.grid(row=0, column=1, sticky="w", pady=10)

root.mainloop()
