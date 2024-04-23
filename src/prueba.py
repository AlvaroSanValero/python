import tkinter as tk

# Create the main application window
root = tk.Tk()

# Create a canvas widget with a specified size
canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()

# Create a rectangle and get its ID for further manipulation
rect_id = canvas.create_rectangle(50, 50, 150, 150, fill='blue')  # (x1, y1, x2, y2)


def update_rectangle():
    # New coordinates for the rectangle (new width and height)
    new_x1, new_y1 = 50, 50  # Top-left corner
    new_x2, new_y2 = 200, 200  # Bottom-right corner

    # Update the rectangle's coordinates
    canvas.coords(rect_id, new_x1, new_y1, new_x2, new_y2)


# Create a button to update the rectangle's size
update_button = tk.Button(root, text="Update Rectangle", command=update_rectangle)
update_button.pack()

# Optionally, you could use an event to trigger the update
root.after(2000, update_rectangle)  # Update after 2 seconds

# Start the Tkinter event loop
root.mainloop()
