import json
from tkinter import *
from tkinter import messagebox
from random import *
import pyperclip

FONT_NAME = "Courier"

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

#Password Generator Project


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    password_input.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #


def save_to_file():
    website = website_input.get()
    email = email_input.get()
    password = password_input.get()

    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if not website or not email or not password:
        messagebox.showinfo(title="website", message="Please don't leave any fields empty!")
    else:
        is_ok = messagebox.askokcancel(title=website, message=f"There are the details entered: \nEmail: {email}"
                                                              f" \nPassword: {password} \nIs it ok to save?")
        if is_ok:
            try:
                with open("data.json", mode="r") as f:
                    data = json.load(f)
                    data.update(new_data)
                with open("data.json", mode="w") as f:
                    json.dump(data, f, indent=4)
            except FileNotFoundError:
                with open("data.json", mode="w") as f:
                    json.dump(new_data, f, indent=4)
            finally:
                website_input.delete(0, END)
                password_input.delete(0, END)

# ----------------------------- SEARCH -------------------------------- #


def find_password():
    website = website_input.get()
    data = False

    try:
        with open("data.json", mode="r") as f:
            data = json.load(f)
    except FileNotFoundError:
        messagebox.showinfo(message="No Data File Found")

    if data:
        if website in data:
            messagebox.showinfo(title=website,
                                message=f"email: {data[website]['email']}\n"
                                        f"password: {data[website]['password']}")
        else:
            messagebox.showinfo(title=website, message="No details for the website exists")

# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)

canvas = Canvas(width=200, height=200, highlightthickness=0)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

website_label = Label(text="Website:", font=(FONT_NAME, 12))
website_label.grid(row=1, column=0)

email_label = Label(text="Email/Username:", font=(FONT_NAME, 12))
email_label.grid(row=2, column=0)

password_label = Label(text="Password:", font=(FONT_NAME, 12))
password_label.grid(row=3, column=0)

website_input = Entry(width=46)
website_input.grid(row=1, column=1, columnspan=2)
website_input.insert(0, "Facebook")

email_input = Entry(width=46)
email_input.grid(row=2, column=1, columnspan=2)
email_input.insert(0, "example@email.com")

password_input = Entry(width=24)
password_input.grid(row=3, column=1)

gen_button = Button(text="Generate Password", font=(FONT_NAME, 12), width=15, command=generate_password)
gen_button.grid(row=3, column=2)

search_button = Button(text="Search", font=(FONT_NAME, 12), width=15, command=find_password)
search_button.grid(row=1, column=2)

add_button = Button(text="Add", font=(FONT_NAME, 12), width=35, command=save_to_file)
add_button.grid(row=4, column=1, columnspan=2)

window.mainloop()
