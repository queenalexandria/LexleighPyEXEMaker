import os
import subprocess
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
import platform


def install_pyinstaller():
    try:
        import PyInstaller
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])


def convert_to_exe(py_path, one_file=True, console=None):
    install_pyinstaller()

    cmd = [
        "pyinstaller",
        py_path,
        "--noconfirm",
    ]

    if one_file:
        cmd.append("--onefile")

    if console is None:
        if py_path.endswith(".pyw"):
            cmd.append("--windowed")
        else:
            cmd.append("--console")
    else:
        cmd.append("--console" if console else "--windowed")

    try:
        subprocess.run(cmd, check=True)
        messagebox.showinfo("Success", "Conversion to EXE successful!\nCheck the 'dist' folder.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"PyInstaller failed:\n{e}")


def browse_file():
    file_path = filedialog.askopenfilename(
        title="Select a Python file",
        filetypes=[("Python Files", "*.py *.pyw")]
    )
    if file_path:
        entry.delete(0, tk.END)
        entry.insert(0, file_path)


def run_conversion():
    py_file = entry.get()
    if not (py_file.endswith(".py") or py_file.endswith(".pyw")):
        messagebox.showerror("Invalid File", "Please select a valid .py or .pyw file.")
        return

    one_file = var_onefile.get()

    if var_force_console.get() == 1:
        console = True
    elif var_force_console.get() == 2:
        console = False
    else:
        console = None

    convert_to_exe(py_file, one_file, console)


# === macOS Catalina-like Style Configuration ===
bg_color = "#ECECEC"  # Light grey
btn_color = "#D6D6D6"
font_main = ("Helvetica Neue", 12)
font_footer = ("Helvetica Neue", 9)

# GUI Setup
app = tk.Tk()
app.title("Python to EXE Converter")
app.geometry("520x350")
app.configure(bg=bg_color)
app.resizable(False, False)

# App Icon on macOS (optional)
if platform.system() == "Darwin":
    try:
        from ctypes import cdll
        app.tk.call('tk::mac::standardAboutPanel')
        cdll.LoadLibrary("/System/Library/Frameworks/Carbon.framework/Carbon")
    except Exception:
        pass

# File Selector
tk.Label(app, text="Select your Python (.py or .pyw) file:", font=font_main, bg=bg_color).pack(pady=(20, 10))
entry = tk.Entry(app, width=50, font=font_main, relief="flat", highlightthickness=1, bd=0)
entry.pack(pady=5)
tk.Button(app, text="Browse", command=browse_file, font=font_main, bg=btn_color, relief="flat").pack(pady=3)

# Options
var_onefile = tk.BooleanVar(value=True)
tk.Checkbutton(app, text="Bundle into one file (--onefile)", variable=var_onefile, font=font_main, bg=bg_color, relief="flat").pack(pady=5)

var_force_console = tk.IntVar(value=0)
frame = tk.Frame(app, bg=bg_color)
tk.Label(frame, text="Console Mode:", font=font_main, bg=bg_color).pack(side=tk.LEFT)
tk.Radiobutton(frame, text="Auto", variable=var_force_console, value=0, bg=bg_color, font=font_main).pack(side=tk.LEFT)
tk.Radiobutton(frame, text="Console", variable=var_force_console, value=1, bg=bg_color, font=font_main).pack(side=tk.LEFT)
tk.Radiobutton(frame, text="Windowed", variable=var_force_console, value=2, bg=bg_color, font=font_main).pack(side=tk.LEFT)
frame.pack(pady=10)

# Convert Button
tk.Button(app, text="Convert to EXE", command=run_conversion, font=font_main, bg="#BDBDBD", relief="flat", height=2, width=20).pack(pady=15)

# Footer Branding
footer = tk.Label(
    app,
    text="© 2025 Lexleigh Communications™. Written by Alexandria Myers",
    font=font_footer,
    fg="gray30",
    bg=bg_color
)
footer.place(relx=1.0, rely=1.0, x=-10, y=-10, anchor="se")

app.mainloop()
