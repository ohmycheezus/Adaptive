from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog, messagebox
from weather import cityweather
from data import Database
from timer import RepeatedTimer
import time
import webbrowser
import os
import pyowm
import func
from geoloc import Locator


app_direct = func.direct_name()
default_var = func.getdefault()
db = Database('maindata.db')
locator = Locator()

app = Tk()

app.title('Adaptive')
app.geometry('800x800')
app.iconbitmap(
    os.environ.get('FAVICONLOC'))
app.resizable(0, 0)


def populate_list():
    parts_list.delete(0, END)
    for row in db.fetch():
        parts_list.insert(END, row)


def remove_city():
    db.remove(selected_city[0])
    populate_list()


def returnCity():
    global city_var
    city_var = city_text.get()
    return city_var


def cityInformation():
    returnCity()
    city_output.configure(
        text=f'Observation: {city_var}. Temperature: {str(cityweather(city_var))} in celcius')
    adapt_button.place(x=480, y=275)


def weather_now():
    if city_text.get().strip() == '':
        messagebox.showerror('Input error', 'Please input correct city name')
    else:
        try:
            cityweather(returnCity())
        except pyowm.exceptions.api_response_error.NotFoundError:
            messagebox.showwarning('Warning!', 'The city does not exist or your input is incorrect')
        else:
            db.insert(returnCity())
            parts_list.delete(0, END)
            parts_list.insert(END, (returnCity()))
            populate_list()


def select_city(event):
    global selected_city
    index = parts_list.curselection()[0]
    selected_city = parts_list.get(index)
    city_input.delete(0, END)
    city_input.insert(END, selected_city[1])
    cityInformation()


def setcolorful():
    if round(cityweather(city_var)) <= -15:
        func.setdeskwallpaper(
            app_direct + r'\temperature\-20.jpg')
    elif round(cityweather(city_var)) <= -10:
        func.setdeskwallpaper(
            app_direct + r'\temperature\-15.jpg')
    elif round(cityweather(city_var)) <= -5:
        func.setdeskwallpaper(
            app_direct + r'\temperature\-10.jpg')
    elif round(cityweather(city_var)) <= 0:
        func.setdeskwallpaper(
            app_direct + r'\temperature\-5.jpg')
    elif round(cityweather(city_var)) <= 5:
        func.setdeskwallpaper(
            app_direct + r'\temperature\0.jpg')
    elif round(cityweather(city_var)) <= 10:
        func.setdeskwallpaper(
            app_direct + r'\temperature\5.jpg')
    elif round(cityweather(city_var)) <= 15:
        func.setdeskwallpaper(
            app_direct + r'\temperature\10.jpg')
    elif round(cityweather(city_var)) <= 20:
        func.setdeskwallpaper(
            app_direct + r'\temperature\15.jpg')
    elif round(cityweather(city_var)) <= 25:
        func.setdeskwallpaper(
            app_direct + r'\temperature\20.jpg')
    elif round(cityweather(city_var)) <= 30:
        func.setdeskwallpaper(
            app_direct + r'\temperature\25.jpg')
    elif round(cityweather(city_var)) <= 35:
        func.setdeskwallpaper(
            app_direct + r'\temperature\30.jpg')
    elif round(cityweather(city_var)) <= 40:
        func.setdeskwallpaper(
            app_direct + r'\temperature\35.jpg')
    else:
        messagebox.showerror('ERROR', 'Something went wrong!')

def dropdown(anoption):
    if anoption == 'per 10 minutes':
        return 600.0
    elif anoption == 'per 5 minutes':
        return 300.0
    else: 
        return 60.0 


def autoLocate():
    try:
        cityweather(locator.autolocation())
    except:
        messagebox.showerror('Autodetection Error', 'Sorry, we are unable to determine your location.') 
    else:
        city_output.configure(
        text=f'Observation: {locator.autolocation()}. Temperature: {str(cityweather(locator.autolocation()))} in celcius')
        adapt_button.place(x=480, y=275)
        db.insert(locator.autolocation())
        parts_list.delete(0, END)
        parts_list.insert(END, (locator.autolocation()))
        populate_list()        
# drop-down menu

option = StringVar(app)
option.set("per minute")
drop_down_menu = OptionMenu(
    app, option, 'per minute', 'per 5 minutes', 'per 10 minutes', command = dropdown)
drop_down_menu.place(x=560, y=187)


interval_timer = RepeatedTimer(1.0, setcolorful)

refresh_timer = RepeatedTimer(dropdown(option), lambda: city_output.configure(
        text=f'Observation: {city_var}. Temperature: {str(cityweather(city_var))} in celcius'))


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit? Wallpaper will be set to Default"):
        func.setdefault(default_var)
        if interval_timer.is_running:
            interval_timer.stop()
            refresh_timer.stop()
        app.destroy()


def toAdapt():
    stop_button.place(x=550, y=275)
    interval_timer.start()
    refresh_timer.start()


def toStop():
    city_output.configure(text='Adaptation was stopped')
    interval_timer.stop()
    refresh_timer.stop()
    func.setdefault(default_var)


# App personalities


header_label = Label(app, text='Adaptive', font=(
    'Lilita One', 28), fg='#0088ff')
header_label.pack(anchor='center', pady= 25)
logo = ImageTk.PhotoImage(Image.open(r'Images\favicon-32x32.png'))
logo_label = Label(image=logo)
logo_label.place(relx=.60, rely=.038)


# user city input


city_label = Label(
    app, text='Input your city here:', font=('Robot', 14))
city_label.place(x=50 , y=120)
city_text = StringVar()
city_input = Entry(app, textvariable=city_text)
city_input.place(x=230, y=125)
city_button = Button(app, text='Add', command=weather_now,
                     fg='white', bg='#428bca', width=10, borderwidth=0)
city_button.place(x=360, y=125)
city_output = Label(app, text='', font=('Open Sans', 12))
city_output.place(x=60, y=280)

# how fast wallpaper is going to change

time_label = Label(
    app, text='How fast do you want to change your wallpaper: 1 change', font=('Robot', 14))
time_label.place(x=50, y=190)


# adaptive button

adapt_button = Button(app, text='Adapt', command=toAdapt, fg='white',
                      bg='#428bca', width=8, height = 2, font=('Open Sans', 10), borderwidth=0)
# city_lists

parts_list = Listbox(app, height=15, width=120)
parts_list.place(x=30, y=330)
parts_list.bind("<<ListboxSelect>>", select_city)

# remove button

remove_button = Button(app, text='Remove', command=remove_city,
                       height=2, width=8, bg='#d9534f', fg='white', borderwidth=0, font =('Open Sans', 10))
remove_button.place(x=693, y=530)

# stop button

stop_button = Button(app, text='Stop', command=toStop, borderwidth=0,
                     bg='#d9534f', fg='white', width=8,height =2, font=('Open Sans', 10))

#Autodetection

detect_button = Button(app, text = 'AUTODETECTION', command = autoLocate, borderwidth = 0, fg = 'white', bg = '#232020', width=14,height = 2, font = ('Open Sans', 12))
detect_button.place(x=550, y=110)


# My personalities


person_label = Label(app, text='© 2019 George Reutov(marstheboy).', fg='blue')
person_label.bind(
    '<Button-1>', lambda e: webbrowser.open_new('https://github.com/Marstheboy'))
person_label.place(relx=.39, rely=0.95)


# closing window

app.protocol("WM_DELETE_WINDOW", on_closing)

# database manipulations

populate_list()

app.mainloop()
