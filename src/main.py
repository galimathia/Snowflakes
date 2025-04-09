from tkinter import *
import random

HEIGHT = 500
WIDTH = 1000
SNOWFLAKE_WIDTH = 5
PENGUIN_WIDTH = 11
PENGUIN_HEIGHT = 22
TAIL_SIZE = 1
DISCOUNT = 0.9
WIND_MAX = 2
WEIGHT = 1
PENGUIN_SPEED = 10
PENGUIN_MAX_MOVE = 5
PENGUIN_MIN_MOVE = 5


class Snowflake:
    def __init__(self, canvas, root, wind, x, y=1):
        self.wind = wind
        self.x = x
        self.y = y
        self.canvas_obj = canvas.create_oval(
            self.x, self.y, self.x+SNOWFLAKE_WIDTH, self.y+SNOWFLAKE_WIDTH,
            fill="white", outline="white", tags=["snowflake"]
        )
        self.canvas = canvas
        self.root = root
        self.speed = random.randint(25, 60)

    def move(self):
        coords = self.canvas.coords(self.canvas_obj)
        if len(coords) == 0:
            return
        if coords[3] > self.canvas.winfo_height():
            self.canvas.delete(self.canvas_obj)
            del self
        else:
            z = random.randint(-1, 1) + self.wind.wind
            self.canvas.move(self.canvas_obj, z, WEIGHT)
            self.root.after(self.speed, self.move)


class Snowdrift:
    def __init__(self, snowflake_width, canvas, root):
        self.columns = []
        self.root = root
        self.canvas = canvas
        columns_number = canvas.winfo_reqwidth()/snowflake_width*2
        columns_number = int(columns_number)
        x1 = 0
        y1 = canvas.winfo_reqheight() - 150
        y2 = canvas.winfo_reqheight()
        for _ in range(columns_number):
            canvas_obj = canvas.create_rectangle(
                x1, y1, x1 + snowflake_width/2, y2,
                fill="white", outline="white", tags=["column"]
            )
            self.columns.append(canvas_obj)
            x1 += snowflake_width/2 + 1
            y1 += random.randint(-1, 1)

    def spread(self, columns, column_index, snowflakes_number):
        added_height = snowflakes_number * SNOWFLAKE_WIDTH / 8
        coords = self.canvas.coords(columns[column_index])
        self.canvas.coords(columns[column_index], coords[0], coords[1] - added_height, coords[2], coords[3])
        tail_height = added_height * DISCOUNT
        for added in range(1, TAIL_SIZE + 1):
            left = column_index - added
            right = column_index + added
            if left >= 0:
                coords1 = self.canvas.coords(self.columns[left])
                self.canvas.coords(
                    self.columns[left],
                    coords1[0], coords1[1] - tail_height,
                    coords1[2], coords1[3]
                )
            if right <= len(self.columns) - 1:
                coords2 = self.canvas.coords(self.columns[right])
                self.canvas.coords(
                    self.columns[right],
                    coords2[0], coords2[1] - tail_height,
                    coords2[2], coords2[3]
                )
            tail_height *= DISCOUNT

    def growth(self):
        for column_index, column in enumerate(self.columns):
            coords = self.canvas.coords(column)
            if len(coords) == 0:
                continue
            overlapping = self.canvas.find_overlapping(coords[0], coords[1], coords[2], coords[3])
            spreading = 0
            for i in overlapping:
                if "snowflake" in self.canvas.gettags(i):
                    self.canvas.delete(i)
                    del i
                    spreading += 1
            self.spread(self.columns, column_index, spreading)
        self.root.after(100, self.growth)


class Wind:
    def __init__(self, root, max):
        self.max = max
        self.root = root
        self.wind = 0
        self.changes = 0
        self.start_wind()

    def start_wind(self):
        if self.wind == self.changes:
            self.changes = random.randint(-self.max, self.max)
            self.root.after(random.randint(5000, 10000), self.start_wind)
        else:
            if self.wind > self.changes:
                self.wind -= 1
            if self.wind < self.changes:
                self.wind += 1
            self.root.after(random.randint(500, 1000), self.start_wind)


class Penguin:
    def __init__(self, x, y, canvas, root, wind):
        self.x = x
        self.y = y
        self.canvas = canvas
        self.root = root
        size_mutation = random.randint(-2, 4)
        self.canvas_obj = canvas.create_oval(
            self.x, self.y, self.x+PENGUIN_WIDTH + size_mutation, self.y+PENGUIN_HEIGHT + size_mutation,
            fill="#0a0a0a", outline="#0a0a0a", tags=["penguin"]
        )
        self.second_canvas_obj = canvas.create_oval(
            self.x, self.y+PENGUIN_WIDTH + size_mutation, self.x+PENGUIN_WIDTH, self.y+PENGUIN_HEIGHT + size_mutation,
            fill="#fff0f5", outline="#fff0f5", tags=["penguin"]
        )
        self.wind = wind
        self.xmove = 0
        self.horizontalmove = 0

    def move(self):
        coords = self.canvas.coords(self.canvas_obj)
        verticalmove = 1
        if len(coords) == 0:
            return
        if coords[3] > self.canvas.winfo_height():
            self.canvas.delete(self.canvas_obj)
            del self
        else:
            overlapping = self.canvas.find_overlapping(coords[0], coords[1], coords[2], coords[3])
            for a in overlapping:
                if "column" in self.canvas.gettags(a):
                    verticalmove -= 1
                if self.horizontalmove >= 3:
                    self.horizontalmove += -1
                elif self.horizontalmove <= -3:
                    self.horizontalmove += 1
                else:
                    if self.wind.wind > 2:
                        self.horizontalmove += random.randint(-1, 0)
                    elif self.wind.wind < -2:
                        self.horizontalmove += random.randint(0, 1)
                    else:
                        self.horizontalmove += random.randint(-1, 1)
            self.canvas.move(self.canvas_obj, self.horizontalmove + self.wind.wind, verticalmove)
            self.canvas.move(self.second_canvas_obj, self.horizontalmove + self.wind.wind, verticalmove)
            self.root.after(PENGUIN_SPEED, self.move)


class Fabric:
    def __init__(self, canvas, root, wind):
        self.wind = wind
        self.min_count = 3
        self.max_count = 5
        self.root = root
        self.canvas = canvas

    def create_snowflakes(self):
        for _ in range(1, random.randint(self.min_count, self.max_count)):
            snowflake_x = random.randint(-300, WIDTH + 300)
            the_snowflake = Snowflake(self.canvas, self.root, self.wind, snowflake_x)
            self.root.after(50, the_snowflake.move)
        self.root.after(200, self.create_snowflakes)
    
    def create_penguins(self):
        for _ in range(0, 11):
            penguin_x = random.randint(0, WIDTH)
            penguin = Penguin(penguin_x, 130, self.canvas, self.root, self.wind)
            self.root.after(50, penguin.move)


def main():
    root = Tk()
    root.title("The snowflakes")
    root.geometry(f'{WIDTH}x{HEIGHT}')
    canvas = Canvas(root, width=WIDTH, height=HEIGHT, background="#AFDEDE")
    canvas.pack(anchor=CENTER, expand=1)
    snowdrift = Snowdrift(SNOWFLAKE_WIDTH, canvas, root)
    snowdrift.growth()
    wind = Wind(root, WIND_MAX)
    fabric = Fabric(canvas, root, wind)
    fabric.create_snowflakes()
    fabric.create_penguins()
    root.mainloop()


if __name__ == "__main__":
    main()
