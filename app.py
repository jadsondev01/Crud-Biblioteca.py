from tkinter import Tk
from views.library_view import LibraryView

if __name__ == "__main__":
    root = Tk()
    app = LibraryView(root)
    root.mainloop()
