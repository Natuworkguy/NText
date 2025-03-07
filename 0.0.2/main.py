import os
if os.name != 'nt':
    import sys
    try:
        import readline
    except ModuleNotFoundError:
        print('Dependency "readline" not found')
        sys.exit()
class TextEditor:
    def __init__(self):
        self.fileisopen = False
        try:
            print("""
███╗   ██╗████████╗███████╗██╗  ██╗████████╗
████╗  ██║╚══██╔══╝██╔════╝╚██╗██╔╝╚══██╔══╝
██╔██╗ ██║   ██║   █████╗   ╚███╔╝    ██║
██║╚██╗██║   ██║   ██╔══╝   ██╔██╗    ██║
██║ ╚████║   ██║   ███████╗██╔╝ ██╗   ██║
╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝  ╚═╝   ╚═╝
            """)
            if os.name != "nt":
                if os.getuid() == 0:
                    print("            (Administrator)")
        except UnicodeDecodeError as bannererror:
            print("NTextError: %s. Continuing." % bannererror)
        self.filename = None
        self.content = []

    def create_file(self, filename):
        self.filename = filename
        self.content = []
        with open(filename, 'w') as file:
            file.write("\n")
        print(f"Created new file '{filename}'")

    def open_file(self, filename):
        try:
            with open(filename, 'r') as f:
                self.content = f.readlines()
            self.filename = filename
            print(f"Opened file '{filename}'")
            self.fileisopen = True
        except FileNotFoundError:
            print(f"File '{filename}' not found")
        except IsADirectoryError:
            print("_Object[File: %s]: Is a directory" % filename)
        except PermissionError as permissionerror_text:
            print(permissionerror_text)
        except UnicodeDecodeError as err:
            print(err)

    def save_file(self):
        if self.filename and self.fileisopen:
            with open(self.filename, 'w') as f:
                f.writelines(self.content)
            print(f"Saved file '{self.filename}'")
        else:
            print("No file is currently open")

    def edit_line(self, line_number, new_content):
        if self.fileisopen:
            if 0 <= line_number < len(self.content):
                self.content[line_number] = new_content + '\n'
                print(f"Edited line {line_number + 1}")
            else:
                print(f"Line {line_number + 1} does not exist")
        else:
            print("No file is currently open")
    def add_line(self, new_content):
        if self.fileisopen:
            self.content.append(new_content + '\n')
            print(f"Added new line")
        else:
            print("No file is currently open")

    def delete_line(self, line_number):
        if self.fileisopen:
            if 0 <= line_number < len(self.content):
                self.content.pop(line_number)
                print(f"Deleted line {line_number + 1}")
            else:
                print(f"Line {line_number + 1} does not exist")
        else:
            print("No file is currently open")
    def search_text(self, text):
        if self.fileisopen:
            results = [i for i, line in enumerate(self.content) if text in line]
            if results:
                for line_number in results:
                    print(f"Found '{text}' in line {line_number + 1}: {self.content[line_number].strip()}")
            else:
                print(f"'{text}' not found in the file")
        else:
            print("No file is currently open")

    def display_content(self):
        if self.fileisopen:
            for i, line in enumerate(self.content):
                print(f"{i + 1}: {line}", end='')
        else:
            print("No file is currently open")
    def helptext(self):
        print("""
        ________________________________________________________________________
        [create <file_to_create>]: Create a new file                           ]
        [open <file>]: Open a file                                             ]
        [save]: Save the file                                                  ]
        [edit <line> <new_content>]: Change the contents of a line             ]
        [add <new_line_content>]: Make a new line at the end of the file       ]
        [delete <line>]: Delete a line                                         ]
        [search <text>]: Search the file for a pattern                         ]
        [display]: Display file contents                                       ]
        [list <arguments>]: List the contents of the current working directory:]
        [    Arguments:                                                        ]
        [       [A]: Show hidden files                                         ]
        [       [L]: Show more file information                                ]
        [dir <directory>]: Change the current working directory                ]
        [exit]: Exit NText                                                     ]
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        """)

    def run(self):
        while True:
            try:
                command = input("NText> ").strip().split()
            except KeyboardInterrupt:
                print("\nExiting NText")
                sys.exit()

            if not command:
                continue

            if command[0] == 'create' and len(command) == 2:
                self.create_file(command[1])
            elif command[0] == 'create':
                print("Command '%s' takes arguments. Use 'help' for help text" % command[0])
            elif command[0] == 'open' and len(command) == 2:
                self.open_file(command[1])
            elif command[0] == 'open':
                print("Command '%s' takes arguments. Use 'help' for help text" % command[0])
            elif command[0] == 'save':
                self.save_file()
            elif command[0] == 'edit' and len(command) >= 3:
                self.edit_line(int(command[1]) - 1, ' '.join(command[2:]))
            elif command[0] == 'edit':
                print("Command '%s' takes arguments. Use 'help' for help text" % command[0])
            elif command[0] == 'add' and len(command) >= 2:
                self.add_line(' '.join(command[1:]))
            elif command[0] == 'add':
                print("Command '%s' takes arguments. Use 'help' for help text" % command[0])
            elif command[0] == 'delete' and len(command) == 2:
                self.delete_line(int(command[1]) - 1)
            elif command[0] == 'delete':
                print("Command '%s' takes arguments. Use 'help' for help text" % command[0])
            elif command[0] == 'search' and len(command) == 2:
                self.search_text(command[1])
            elif command[0] == 'search':
                print("Command '%s' takes arguments. Use 'help' for help text" % command[0])
            elif command[0] == 'display':
                self.display_content()
            elif len(command) > 1 and command[0] == 'list' and command[1] == 'A':
                os.system('ls -a')
            elif len(command) > 1 and command[0] == 'list' and command[1] == 'L':
                os.system('ls -l')
            elif len(command) > 1 and command[0] == 'list' and command[1] in ['AL', 'LA']:
                os.system('ls -la')
            elif command[0] == 'list':
                os.system('ls')
            elif command[0] == 'dir' and len(command) == 2:
                try:
                    os.chdir(command[1])
                    print(f"Changed directory to '{command[1]}'")
                except FileNotFoundError:
                    print(f"Directory '{command[1]}' not found")
                except PermissionError as permissionerror_text:
                    print(permissionerror_text)
                except NotADirectoryError:
                    print(f"{command[1]}: Not a directory")
            elif command[0] == 'dir':
                print("Command 'dir' takes a directory path as argument. Use 'help' for help text")
            elif command[0] == "help":
                self.helptext()
            elif command[0] == 'exit' or command[0] == '_session[exit]':
                break
            else:
                print(f"{command[0]}: NexLang Command not found")

if __name__ == "__main__":
    editor = TextEditor()
    if os.name != 'nt':
        editor.run()
    else:
        print("Cannot run in NT.")
        os.system("pause")
