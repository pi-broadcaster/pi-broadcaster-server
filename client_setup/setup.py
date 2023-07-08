import os, sys, shutil

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

print("Đang cài các thư viện để chạy chương trình...")

print("[+]Python 3.11.4")
os.system(resource_path("python-3.11.4.exe") + " /passive PrependPath=1 AppendPath=1 Shortcuts=0 Include_doc=0 TargetDir=\"C:\\Python311\"")

print("[+]Thư viện pysftp, paramiko")
os.system("\"C:\\Python311\\Scripts\\pip.exe\" install -r " + resource_path("requirements.txt"))

print("[+]Bonjour DNS")
if sys.maxsize > 2**32:
    os.system(resource_path("Bonjour64.msi") + " /passive")
else:
    os.system(resource_path("Bonjour.msi") + " /passive")

print("[+]Chuẩn bị hoàn tất")
os.system("mkdir \"C:\\Program Files\\pi-dashboard\"")
shutil.move(resource_path("main.pyw"), "C:\\Program Files\\pi-dashboard")
shutil.move(resource_path("icon.ico"), "C:\\Program Files\\pi-dashboard")
os.system("echo py -3.11 main.pyw > \"C:\\Program Files\\pi-dashboard\\main.bat\"")
os.system(resource_path("nircmd.exe") + " shortcut \"C:\\Program Files\\pi-dashboard\\main.bat\" \"" + os.path.normpath(os.path.expanduser("~/Desktop")) + "\" \"Bang dieu khien\" \"\" \"" + resource_path("icon.ico") + "\"")

input("Cài đặt hoàn tất. Nhấn ENTER để thoát.")