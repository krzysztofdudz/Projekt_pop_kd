from tkinter import *
import tkintermapview
from bs4 import BeautifulSoup
import requests

root = Tk()
root.title("System stacji ładowania pojazdów elektrycznych")
root.geometry("1400x900")

stations = []
employees = []
clients = []


def get_coordinates(city):
    try:
        import requests
        from bs4 import BeautifulSoup
        url = f"https://pl.wikipedia.org/wiki/{city}"
        response = requests.get(url).text
        soup = BeautifulSoup(response, "html.parser")
        lon = float(soup.select(".longitude")[1].text.replace(",", "."))
        lat = float(soup.select(".latitude")[1].text.replace(",", "."))
        return lat, lon
    except:
        return 52.23, 21.0

class Station:
    def __init__(self, name, city):
        self.name = name
        self.city = city
        self.coords = get_coordinates(city)
        self.employees = []
        self.clients = []
        self.marker = map_widget.set_marker(
            self.coords[0], self.coords[1], text=self.get_marker_text()
        )
        stations.append(self)

    def get_marker_text(self):
        emp = ", ".join([e.name for e in self.employees]) or "Brak"
        cli = ", ".join([c.name for c in self.clients]) or "Brak"
        return f"Stacja: {self.name}\\nMiasto: {self.city}\\nPracownicy: {emp}\\nKlienci: {cli}"

    def update_marker(self):
        self.marker.set_text(self.get_marker_text())

class Employee:
    def __init__(self, name, station):
        self.name = name
        self.station = station
        station.employees.append(self)
        employees.append(self)
        station.update_marker()

class Client:
    def __init__(self, name, station):
        self.name = name
        self.station = station
        station.clients.append(self)
        clients.append(self)
        station.update_marker()



def update_station_list():
    station_listbox.delete(0, END)
    for i, s in enumerate(stations):
        station_listbox.insert(i, f"{s.name} ({s.city})")

def update_employee_list():
    employee_listbox.delete(0, END)
    for i, e in enumerate(employees):
        employee_listbox.insert(i, f"{e.name} - {e.station.name}")

def update_client_list():
    client_listbox.delete(0, END)
    for i, c in enumerate(clients):
        client_listbox.insert(i, f"{c.name} - {c.station.name}")


def add_station():
    name = station_name_entry.get()
    city = station_city_entry.get()
    if name and city:
        Station(name, city)
        station_name_entry.delete(0, END)
        station_city_entry.delete(0, END)
        update_station_list()
        refresh_station_dropdowns()

def edit_station():
    i = station_listbox.curselection()
    if not i:
        return
    station = stations[i[0]]
    station_name_entry.delete(0, END)
    station_city_entry.delete(0, END)
    station_name_entry.insert(0, station.name)
    station_city_entry.insert(0, station.city)

    global edit_index
    edit_index = i[0]
    btn_add_station.config(text="Zapisz", command=update_station)


def update_station():
    global edit_index
    name = station_name_entry.get()
    city = station_city_entry.get()
    if name and city and edit_index is not None:
        station = stations[edit_index]
        station.name = name
        station.city = city
        station.coords = get_coordinates(city)
        station.marker.set_position(station.coords[0], station.coords[1])
        station.update_marker()
        update_station_list()
        refresh_station_dropdowns()
        station_name_entry.delete(0, END)
        station_city_entry.delete(0, END)
        btn_add_station.config(text="Dodaj", command=add_station)
        edit_index = None


def delete_station():
    i = station_listbox.curselection()
    if not i:
        return
    station = stations.pop(i[0])
    station.marker.delete()
    for e in station.employees:
        employees.remove(e)
    for c in station.clients:
        clients.remove(c)
    update_station_list()
    update_employee_list()
    update_client_list()
    refresh_station_dropdowns()


def add_employee():
    name = employee_name_entry.get()
    station_name = employee_station_var.get()
    station = next((s for s in stations if s.name == station_name), None)
    if name and station:
        Employee(name, station)
        employee_name_entry.delete(0, END)
        update_employee_list()

def add_client():
    name = client_name_entry.get()
    station_name = client_station_var.get()
    station = next((s for s in stations if s.name == station_name), None)
    if name and station:
        Client(name, station)
        client_name_entry.delete(0, END)
        update_client_list()

def delete_employee():
    i = employee_listbox.curselection()
    if not i:
        return
    emp = employees.pop(i[0])
    emp.station.employees.remove(emp)
    emp.station.update_marker()
    update_employee_list()

def delete_client():
    i = client_listbox.curselection()
    if not i:
        return
    cli = clients.pop(i[0])
    cli.station.clients.remove(cli)
    cli.station.update_marker()
    update_client_list()




top_frame = Frame(root)
top_frame.pack()

station_frame = LabelFrame(top_frame, text="Stacje", padx=10, pady=10)
station_frame.grid(row=0, column=0, padx=5, pady=5)

station_name_entry = Entry(station_frame)
station_city_entry = Entry(station_frame)
Label(station_frame, text="Nazwa:").grid(row=0, column=0)
station_name_entry.grid(row=0, column=1)
Label(station_frame, text="Miasto:").grid(row=1, column=0)
station_city_entry.grid(row=1, column=1)

station_listbox = Listbox(station_frame, width=30)
station_listbox.grid(row=3, column=0, columnspan=2)

employee_frame = LabelFrame(top_frame, text="Pracownicy", padx=10, pady=10)
employee_frame.grid(row=0, column=1, padx=5, pady=5)

client_frame = LabelFrame(top_frame, text="Klienci", padx=10, pady=10)
client_frame.grid(row=0, column=2, padx=5, pady=5)

client_name_entry = Entry(client_frame)
Label(client_frame, text="Nazwa:").grid(row=0, column=0)
client_name_entry.grid(row=0, column=1)

Label(client_frame, text="Stacja:").grid(row=1, column=0)
client_station_var = StringVar()
client_station_dropdown = OptionMenu(client_frame, client_station_var, "")
client_station_dropdown.grid(row=1, column=1)

client_listbox = Listbox(client_frame, width=30)
client_listbox.grid(row=3, column=0, columnspan=2)

button_frame_client = Frame(client_frame)
button_frame_client.grid(row=4, column=0, columnspan=2, pady=5)

btn_add_client = Button(button_frame_client, text="Dodaj", command=add_client)
btn_add_client.pack(side=LEFT, padx=5)


employee_name_entry = Entry(employee_frame)
Label(employee_frame, text="Imię:").grid(row=0, column=0)
employee_name_entry.grid(row=0, column=1)

Label(employee_frame, text="Stacja:").grid(row=1, column=0)
employee_station_var = StringVar()
employee_station_dropdown = OptionMenu(employee_frame, employee_station_var, "")
employee_station_dropdown.grid(row=1, column=1)

employee_listbox = Listbox(employee_frame, width=30)
employee_listbox.grid(row=3, column=0, columnspan=2)

button_frame_employee = Frame(employee_frame)
button_frame_employee.grid(row=4, column=0, columnspan=2, pady=5)

btn_add_employee = Button(button_frame_employee, text="Dodaj", command=add_employee)
btn_add_employee.pack(side=LEFT, padx=5)



button_frame_station = Frame(station_frame)
button_frame_station.grid(row=2, column=0, columnspan=2)


btn_add_station = Button(button_frame_station, text="Dodaj", command=add_station)
btn_add_station.pack(side=LEFT, padx=5)

btn_edit_station = Button(button_frame_station, text="Edytuj", command=edit_station)
btn_edit_station.pack(side=LEFT, padx=5)


btn_delete_station = Button(button_frame_station, text="Usuń", command=delete_station)
btn_delete_station.pack(side=LEFT, padx=5)

btn_delete_employee = Button(button_frame_employee, text="Usuń", command=delete_employee)
btn_delete_employee.pack(side=LEFT, padx=5)

btn_delete_client = Button(button_frame_client, text="Usuń", command=delete_client)
btn_delete_client.pack(side=LEFT, padx=5)


def refresh_station_dropdowns():
    menu_emp = employee_station_dropdown["menu"]
    menu_cli = client_station_dropdown["menu"]

    menu_emp.delete(0, END)
    menu_cli.delete(0, END)

    for s in stations:
        menu_emp.add_command(label=s.name, command=lambda val=s.name: employee_station_var.set(val))
        menu_cli.add_command(label=s.name, command=lambda val=s.name: client_station_var.set(val))

    if stations:
        employee_station_var.set(stations[0].name)
        client_station_var.set(stations[0].name)


map_widget = tkintermapview.TkinterMapView(root, width=1400, height=500, corner_radius=5)
map_widget.pack(pady=10)
map_widget.set_position(52.23, 21.0)
map_widget.set_zoom(6)

root.mainloop()