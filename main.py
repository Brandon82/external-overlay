from external_overlay import ExternalOverlay
from ui import ui

def main():
    overlay = ExternalOverlay("Untitled - Notepad", ui)
    overlay.start()

if __name__ == "__main__":
    main()