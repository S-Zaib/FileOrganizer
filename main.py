import os
import sys
import customtkinter as tk

class Organize:
    def __init__(self, path):
        self.path = path
        self.dict = {}
        self.updateDict()

    def updateDict(self):
        # Set Path to this file
        config_file = os.path.join(os.path.dirname(sys.argv[0]), "config.ini")
        print(config_file)
        with open(config_file, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    key, value = line.split("=")
                    self.dict[key] = value

    def moveFolders(self):
        # Move existing folders to a folder called Folders
        os.chdir(self.path) 
        
        for folder in os.listdir():
            if os.path.isdir(folder) and folder != self.dict["folders"] and folder not in self.dict.values():
                    if not os.path.exists(self.dict["folders"]):
                        os.mkdir(self.dict["folders"])
                    target_folder = os.path.join(self.dict["folders"], folder)
                    new_folder = folder
                    counter = 1
                    while os.path.exists(target_folder):
                        new_folder = f"{folder}_{counter}"
                        target_folder = os.path.join(self.dict["folders"], new_folder)
                        counter += 1
                    os.rename(folder, target_folder)

    def moveFiles(self):
        os.chdir(self.path)
        for file in os.listdir():
            if os.path.isfile(file):
                ext = os.path.splitext(file)[1]
                if not os.path.exists(self.dict[ext]):
                    os.mkdir(self.dict[ext])
                if ext in self.dict:
                    target_folder = self.dict[ext]
                else:
                    target_folder = self.dict["*"]

                # Handle duplicate filenames
                new_filename = file
                counter = 1
                while os.path.exists(os.path.join(target_folder, new_filename)):
                    base_name, extension = os.path.splitext(file)
                    new_filename = f"{base_name}_{counter}{extension}"
                    counter += 1

                # Move the file to the appropriate folder with a unique name
                os.rename(file, os.path.join(target_folder, new_filename))

    def organize(self):
        self.moveFolders()
        self.moveFiles()
        # Open the folder
        os.startfile(self.path)


class OrganizerGUI:

    def __init__(self, master):
        self.master = master
        self.path = tk.StringVar()

        # Set Window Size
        master.geometry("250x200")

        # Set Title
        master.title("Organizer")
        self.label = tk.CTkLabel(master, text="Organize your files")
        self.label.pack()

        # Show Path
        self.path_label = tk.CTkLabel(master, text="Set Path by pressing Browse! " + self.path.get())
        self.path_label.pack()

        # Add Browse Button
        self.path_button = tk.CTkButton(master, text="Browse", command=self.browse)
        self.path_button.pack(pady=5)

        # Add Organize Button
        self.organize_button = tk.CTkButton(master, text="Organize", command=self.organize)
        self.organize_button.pack(pady=5)

        # Add Close Button
        self.close_button = tk.CTkButton(master, text="Close", command=master.quit)
        self.close_button.pack(pady=5)

    def browse(self):
        self.path.set(tk.filedialog.askdirectory())
        self.path_label.configure(text="Path: " + self.path.get())


    def organize(self):
        print(self.path.get())
        organize = Organize(self.path.get())
        organize.organize()

root = tk.CTk()
my_gui = OrganizerGUI(root)
root.mainloop()

