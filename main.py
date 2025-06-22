from tkinter import *
import tkintermapview

root = Tk()
root.title("System stacji ładowania pojazdów elektrycznych")
root.geometry("1400x900")

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

map_widget = tkintermapview.TkinterMapView(root, width=1400, height=500, corner_radius=5)
map_widget.pack(pady=10)
map_widget.set_position(52.23, 21.0)
map_widget.set_zoom(6)

root.mainloop()