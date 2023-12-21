from pathlib import Path
import os
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, messagebox

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\danil\OneDrive\Desktop\JR\ShoPinas\build\assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

window = Tk()

window.geometry("750x525+400+150")
window.configure(bg = "#FFFFFF")

canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 525,
    width = 750,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    612.0,
    375.0,
    image=image_image_1
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    360.0,
    307.0,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=229.0,
    y=289.0,
    width=262.0,
    height=34.0
)

canvas.create_text(
    229.0,
    273.0,
    anchor="nw",
    text="Username",
    fill="#000000",
    font=("Josefin Sans", 13 * -1)
)

canvas.create_rectangle(
    230.0,
    323.9999999442982,
    491.0,
    325.0,
    fill="#032FA1",
    outline="")

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    362.0,
    386.0,
    image=entry_image_2
)
entry_2 = Entry(
    bd=0,
    show ="*",
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_2.place(
    x=231.0,
    y=368.0,
    width=262.0,
    height=34.0
)

entry_2.bind("<Return>", (lambda event:fetch_credentials(entry_1, entry_2)))

canvas.create_rectangle(
    230.0,
    402.9999999442982,
    491.0,
    404.0,
    fill="#032FA1",
    outline="")

canvas.create_text(
    231.0,
    344.0,
    anchor="nw",
    text="Password",
    fill="#000000",
    font=("Josefin Sans", 13 * -1)
)

canvas.create_text(
    99.0,
    50.0,
    anchor="nw",
    text="Sho",
    fill="#FF0000",
    font=("Josefin Sans", 128 * -1)
)

canvas.create_text(
    391.0,
    50.0,
    anchor="nw",
    text="i",
    fill="#F3BF07",
    font=("Josefin Sans", 128 * -1)
)

canvas.create_text(
    314.0,
    50.0,
    anchor="nw",
    text="P nas",
    fill="#032FA1",
    font=("Josefin Sans", 128 * -1)
)

canvas.create_text(
    231.0,
    203.0,
    anchor="nw",
    text="SALES TRACKER",
    fill="#424550",
    font=("Josefin Sans", 32 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: fetch_credentials(entry_1, entry_2),
    relief="flat"
)

def fetch_credentials(
    entry_1=entry_1,
    entry_2=entry_2, 
):
    username = entry_1.get()
    password = entry_2.get()

    if(
        username == "user" and password == "admin"
    ):
        print(username, password)
        window.destroy()
        os.system('python home.py')
        
    else:
        messagebox.showerror(title="Invalid Credentials", message="Check Username and Password" )
    
button_1.place(
    x=314.0,
    y=432.0,
    width=129.0,
    height=40.0
)
window.resizable(False, False)
window.mainloop()
