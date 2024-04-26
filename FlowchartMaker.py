import tkinter as tk
from tkinter import ttk, colorchooser, filedialog

class FlowchartMaker:
    def __init__(self, root):
        self.root = root
        self.root.title("Flowchart Maker")

        self.canvas = tk.Canvas(self.root, bg="white", width=800, height=600)
        self.canvas.pack(expand=True, fill="both")

        self.shapes = []  # List to store flowchart shapes
        self.current_shape = None  # Currently selected shape
        self.current_tool = "rectangle"  # Default tool

        self.init_tools()
        self.init_bindings()

    def init_tools(self):
        tools_frame = ttk.Frame(self.root)
        tools_frame.pack(side="left", fill="y")

        shapes = ["Rectangle", "Diamond", "Arrow"]
        for shape in shapes:
            button = ttk.Button(tools_frame, text=shape, command=lambda s=shape.lower(): self.set_tool(s))
            button.pack(fill="x")

        color_button = ttk.Button(tools_frame, text="Color", command=self.pick_color)
        color_button.pack(fill="x")

        save_button = ttk.Button(tools_frame, text="Save", command=self.save_flowchart)
        save_button.pack(fill="x")

        load_button = ttk.Button(tools_frame, text="Load", command=self.load_flowchart)
        load_button.pack(fill="x")

    def init_bindings(self):
        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw_shape)
        self.canvas.bind("<ButtonRelease-1>", self.finish_draw)

    def start_draw(self, event):
        if self.current_tool == "rectangle":
            self.current_shape = self.canvas.create_rectangle(event.x, event.y, event.x, event.y, outline="black")
        elif self.current_tool == "diamond":
            self.current_shape = self.canvas.create_polygon(event.x, event.y, event.x + 50, event.y + 25,
                                                            event.x, event.y + 50, event.x - 50, event.y + 25,
                                                            outline="black")
        elif self.current_tool == "arrow":
            self.current_shape = self.canvas.create_line(event.x, event.y, event.x + 50, event.y + 25,
                                                         arrow=tk.LAST, fill="black")

    def draw_shape(self, event):
        if self.current_shape:
            if self.current_tool == "rectangle":
                self.canvas.coords(self.current_shape, self.canvas.coords(self.current_shape)[0],
                                    self.canvas.coords(self.current_shape)[1], event.x, event.y)
            elif self.current_tool == "diamond":
                self.canvas.coords(self.current_shape, event.x, event.y,
                                    event.x + 50, event.y + 25,
                                    event.x, event.y + 50,
                                    event.x - 50, event.y + 25)
            elif self.current_tool == "arrow":
                self.canvas.coords(self.current_shape, self.canvas.coords(self.current_shape)[0],
                                    self.canvas.coords(self.current_shape)[1], event.x, event.y)

    def finish_draw(self, event):
        self.shapes.append(self.current_shape)
        self.current_shape = None

    def set_tool(self, tool):
        self.current_tool = tool

    def pick_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.canvas.itemconfig(self.current_shape, outline=color)

    def save_flowchart(self):
        filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if filename:
            with open(filename, "w") as file:
                for shape in self.shapes:
                    file.write(f"{self.canvas.type(shape)} {self.canvas.coords(shape)} {self.canvas.itemcget(shape, 'outline')}\n")

    def load_flowchart(self):
        filename = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if filename:
            with open(filename, "r") as file:
                for line in file:
                    parts = line.split()
                    shape_type = parts[0]
                    coords = [float(x) for x in parts[1:9]]
                    outline_color = parts[-1]
                    if shape_type == "rectangle":
                        shape = self.canvas.create_rectangle(coords, outline=outline_color)
                    elif shape_type == "polygon":
                        shape = self.canvas.create_polygon(coords, outline=outline_color)
                    elif shape_type == "line":
                        shape = self.canvas.create_line(coords, arrow=tk.LAST, fill=outline_color)
                    self.shapes.append(shape)

def main():
    root = tk.Tk()
    app = FlowchartMaker(root)
    root.mainloop()

if __name__ == "__main__":
    main()
