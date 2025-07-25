import os
import subprocess
import sys
import tkinter as tk
from tkinter import filedialog, messagebox


def install_pyinstaller():
    try:
        import PyInstaller  # noqa
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])


def convert_to_exe(py_path, one_file=True, console=None):
    install_pyinstaller()

    # Use Python's executable to run PyInstaller
    cmd = [
        sys.executable, "-m", "PyInstaller",
        py_path,
        "--noconfirm",
    ]

    if one_file:
        cmd.append("--onefile")

    # Determine if console or windowed mode is appropriate
    if console is None:
        cmd.append("--windowed" if py_path.endswith(".pyw") else "--console")
    else:
        cmd.append("--console" if console else "--windowed")

    try:
        subprocess.run(cmd, check=True)
        messagebox.showinfo("Success", "EXE created successfully in the 'dist' folder.")
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
        messagebox.showerror("Invalid File", "Please select a .py or .pyw file.")
        return

    one_file = var_onefile.get()

    if var_force_console.get() == 1:
        console = True
    elif var_force_console.get() == 2:
        console = False
    else:
        console = None

    convert_to_exe(py_file, one_file, console)


# ===== UI STYLES =====
bg_color = "#ECECEC"   # Light grey, mac-inspired
btn_color = "#D6D6D6"
font_main = ("Segoe UI", 11)
font_footer = ("Segoe UI", 9)

# ===== GUI SETUP =====
app = tk.Tk()
app.title("Lexleigh Python to EXE Converter")
app.geometry("520x350")
app.configure(bg=bg_color)
app.resizable(False, False)

# File selection
tk.Label(app, text="Select your Python (.py or .pyw) file:", font=font_main, bg=bg_color).pack(pady=(20, 10))
entry = tk.Entry(app, width=50, font=font_main, relief="flat", highlightthickness=1)
entry.pack(pady=5)
tk.Button(app, text="Browse", command=browse_file, font=font_main, bg=btn_color, relief="flat").pack(pady=3)

# Options
var_onefile = tk.BooleanVar(value=True)
tk.Checkbutton(app, text="Bundle into one file (--onefile)", variable=var_onefile,
               font=font_main, bg=bg_color, relief="flat").pack(pady=5)

# Console/windowed radio buttons
var_force_console = tk.IntVar(value=0)
frame = tk.Frame(app, bg=bg_color)
tk.Label(frame, text="Console Mode:", font=font_main, bg=bg_color).pack(side=tk.LEFT)
tk.Radiobutton(frame, text="Auto", variable=var_force_console, value=0, bg=bg_color, font=font_main).pack(side=tk.LEFT)
tk.Radiobutton(frame, text="Console", variable=var_force_console, value=1, bg=bg_color, font=font_main).pack(side=tk.LEFT)
tk.Radiobutton(frame, text="Windowed", variable=var_force_console, value=2, bg=bg_color, font=font_main).pack(side=tk.LEFT)
frame.pack(pady=10)

# Convert button
tk.Button(app, text="Convert to EXE", command=run_conversion,
          font=font_main, bg="#BDBDBD", relief="flat", height=2, width=20).pack(pady=15)

# Footer / Attribution
footer = tk.Label(
    app,
    text="© 2025 Lexleigh Communications™. Written by Alexandria Myers",
    font=font_footer,
    fg="gray30",
    bg=bg_color
)
footer.place(relx=1.0, rely=1.0, x=-10, y=-10, anchor="se")

app.mainloop()
