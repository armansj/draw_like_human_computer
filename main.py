import filecmp
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import pyautogui
import time

def upload_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if not file_path:
        return
    display_original_image(file_path)
    image = cv2.imread(file_path)
    edges = extract_edges(image)

    global scaled_edges
    scaled_edges = scale_edges(edges, canvas_width, canvas_height, image.shape[1], image.shape[0])

    canvas.delete("all")
    root.after(100, simulate_mouse_painting)

def display_original_image(file_path):
    img = Image.open(file_path)
    img.thumbnail((300, 300))
    img_tk = ImageTk.PhotoImage(img)

    img_label.config(image=img_tk)
    img_label.image = img_tk

def extract_edges(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, threshold1=50, threshold2=150)

    edge_points = [(x, y) for y in range(edges.shape[0]) for x in range(edges.shape[1]) if edges[y, x] != 0]
    return edge_points

def scale_edges(edges, canvas_width, canvas_height, img_width, img_height):
    x_scale = canvas_width / img_width
    y_scale = canvas_height / img_height
    return [(int(x * x_scale), int(y * y_scale)) for x, y in edges]

def simulate_mouse_painting():
    global scaled_edges
    if not scaled_edges:
        return

    x, y = scaled_edges.pop(0)
    canvas.create_oval(x, y, x + 1, y + 1, fill="black", outline="black")
    canvas_x = root.winfo_rootx() + canvas.winfo_x()
    canvas_y = root.winfo_rooty() + canvas.winfo_y()
    pyautogui.moveTo(canvas_x + x, canvas_y + y)
    root.after(1, simulate_mouse_painting)
root = tk.Tk()
root.title("Mouse pencil painter")

canvas_width = 1200
canvas_height = 900
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="white")
canvas.pack()

img_label = tk.Label(root)
img_label.pack(pady=10)

upload_btn = tk.Button(root, text="Upload Image", command=upload_image)
upload_btn.pack(pady=20)

scaled_edges = []

root.config(cursor="pencil")

root.mainloop()