from tkinter import *
import tkintermapview

root = Tk()
root.title("System stacji ładowania pojazdów elektrycznych")
root.geometry("1400x900")

top_frame = Frame(root)
top_frame.pack()

map_widget = tkintermapview.TkinterMapView(root, width=1400, height=500, corner_radius=5)
map_widget.pack(pady=10)
map_widget.set_position(52.23, 21.0)
map_widget.set_zoom(6)

root.mainloop()