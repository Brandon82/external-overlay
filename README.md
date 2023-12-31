# external-overlay
An external Python overlay that attaches/hooks onto a given Windows application and draws on top of it.
- Uses the [DearPyGui](https://github.com/hoffstadt/DearPyGui) (DPG) GUI framework for drawing (DX11)
- Uses the PyWin32 library (Windows API) for attaching to the target application

![Example](https://i.gyazo.com/8a00c8288d4830772c130d39fcff7c12.gif)

## Installation
Install the following dependencies:
- Python 3.8+
- `pip install -r requirements.txt`

## Usage
```
from external_overlay import ExternalOverlay

def ui(tar_hwnd=None):
    with dpg.window():
        dpg.add_text("Hello World")

overlay = ExternalOverlay("Untitled - Notepad", ui)
overlay.start()
```
- Create a new `ExternalOverlay` object with the window name and a UI function as parameters
- The UI function should contain the DPG components to overlay
- Call `start()` to start the overlay render loop