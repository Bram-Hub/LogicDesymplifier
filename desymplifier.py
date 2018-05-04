from desympgui import DesympGUI

if __name__ == "__main__":
    gui = DesympGUI()
    gui.master.title("Desymplifier")
    gui.master.maxsize(1000, 800)

    gui.start()
