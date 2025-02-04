import os, random, winreg

def set(root, address):
    basename = os.path.basename(address)
    try:
        root.iconbitmap(basename)
    except Exception:
            root.iconbitmap(address)

def rand(root, icon_dir = ""):
    if icon_dir == "":
        # Open the registry key corresponding to the library
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, fr"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders")
        # Retrieve the path from the registry
        pic_dir, _ = winreg.QueryValueEx(key, 'My Pictures')
        icon_dir = os.path.join(pic_dir, "Default/Icon")

    icon_List = os.listdir(icon_dir)
    full_path = [os.path.join(icon_dir, basename) for basename in icon_List if basename.endswith('.ico')]

    len_full_path = len(full_path)
    rand = random.randint(0, len_full_path-1)

    root.iconbitmap(full_path[rand])