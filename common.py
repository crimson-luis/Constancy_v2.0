from cryptography.fernet import Fernet
from tkinter import messagebox
import ntsecuritycon as con
from ctypes import windll
import win32security
from processing import log_handler
import win32api
import win32con
import sys
import os

logged_user = dict()
GWL_EXSTYLE = -20
WS_EX_APPWINDOW = 0x00040000
WS_EX_TOOLWINDOW = 0x00000080
M_FONT = "Roboto 10"
EMAIL_REGEX = r"^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$"
M_COLOR = {
    "p0": "white",
    "txt": "#9a69cb",
    "cbg": "#451473",  # 5e4278
    "darker": "#24093e",  # 321a4c
    "rp0": "#7a5796",
    "rp1": "#ffd9ff",
    "success": "#00a000",
    "error": "#a30000",
}


def set_appwindow(window):
    # Honestly forgot what most of this stuff does. I think it's so that you can see
    # the program in the task bar while using overrideredirect. Most of it is taken
    # from a post I found on stackoverflow.
    hwnd = windll.user32.GetParent(window.winfo_id())
    stylew = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    stylew = stylew & ~WS_EX_TOOLWINDOW
    stylew = stylew | WS_EX_APPWINDOW
    res = windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, stylew)
    # re-assert the new window style
    window.wm_withdraw()
    window.after(10, lambda: window.wm_deiconify())


def del_win(root):
    log_handler.Logger().log_it("syslog", "info", "Application aborted.")
    root.destroy()


def f_invoker(button, event=None):
    button.invoke()
    return event


def f_error_msg(index, txt):
    messagebox.showerror("Erro {}!".format(index), txt)


def file_permissions(
    file,
    sys_acess=con.FILE_ALL_ACCESS,
    user_acess=con.FILE_ALL_ACCESS,
    admin_acess=con.FILE_GENERIC_WRITE,
):
    """Set permissions and hide the file (System-> con.FILE_ALL_ACCESS; Admin->
    con.FILE_GENERIC_WRITE; User-> con.FILE_GENERIC_WRITE)."""
    # SID for system, admin and user.
    system, domain, _type = win32security.LookupAccountName("", "SYSTEM")
    admins, domain, _type = win32security.LookupAccountName("", "Administrators")
    user, domain, _type = win32security.LookupAccountName("", win32api.GetUserName())

    # Find DACL part of file security.
    sd = win32security.GetFileSecurity(file, win32security.DACL_SECURITY_INFORMATION)

    # Create DACL and ACEs and set to file.
    dacl = win32security.ACL()
    dacl.AddAccessAllowedAce(win32security.ACL_REVISION, sys_acess, system)
    dacl.AddAccessAllowedAce(win32security.ACL_REVISION, user_acess, user)
    dacl.AddAccessAllowedAce(win32security.ACL_REVISION, admin_acess, admins)

    # Put DACL into descriptor and update sd.
    sd.SetSecurityDescriptorDacl(1, dacl, 0)
    win32security.SetFileSecurity(file, win32security.DACL_SECURITY_INFORMATION, sd)
    hide_file(file)


def hide_file(file):
    win32api.SetFileAttributes(file, win32con.FILE_ATTRIBUTE_HIDDEN)


def change_key():
    """Change/create the cryptography key, intended to be used one time every installation
    because once one key is used it won't work if changed."""
    key_path = resource_path("data/lk.key")
    if not os.path.isfile(key_path):
        with open(key_path, "wb") as file:
            new_key = Fernet.generate_key()
            file.write(new_key)
        file_permissions(
            key_path,
            con.FILE_ALL_ACCESS,
            con.FILE_GENERIC_WRITE,
            con.FILE_GENERIC_WRITE,
        )


def get_key():
    """Open key file, remove permissions, read key, re-add permissions and return the
    Fernet key object."""
    key_path = resource_path("data/lk.key")
    # giving permission to read then removing again... ugly? maybe but works
    file_permissions(
        key_path, con.FILE_ALL_ACCESS, con.FILE_ALL_ACCESS, con.FILE_GENERIC_WRITE
    )
    with open(key_path, "rb") as file:
        key = file.read()
    file_permissions(
        key_path, con.FILE_ALL_ACCESS, con.FILE_GENERIC_WRITE, con.FILE_GENERIC_WRITE
    )
    return Fernet(key)


def f_encrypt(password):
    f_key = get_key()
    token = f_key.encrypt(str(password).encode())
    return token


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)
