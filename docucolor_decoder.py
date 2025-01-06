import tkinter as tk
from tkinter import messagebox

class DocucolorDecoder:
    def __init__(self):
        self.root = tk.Tk()
        self.root.configure(bg='black')
        self.root.title("Docucolor Decoder")
        
        # Initialize variables
        self.code = tk.StringVar()
        self.dots = {}  # Store dot references
        self.col = list(range(15))  # 0-14 columns
        self.row = [0, 64, 32, 16, 8, 4, 2, 1]  # Row values for binary encoding
        
        # Create frames with dark theme
        self.f1 = tk.Frame(self.root, bg='black')  # Main frame
        self.f3 = tk.Frame(self.root, bg='black')  # Result frame
        self.f4 = tk.Frame(self.root, bg='black')  # Button frame
        
        for frame in (self.f1, self.f3, self.f4):
            frame.pack(pady=2)
            
        # Canvas for dots visualization
        self.canvas = tk.Canvas(self.f1, bg='black', width=630, height=390)
        self.canvas.pack()
        
        self.create_grid()
        self.create_dots()
        self.create_labels()
        self.create_buttons()
        
        # Bind Escape key to quit
        self.root.bind('<Escape>', lambda e: self.root.quit())
        
        # Initial reset
        self.reset()

    def create_dot(self, x, y, tag):
        """Create an interactive dot on the canvas"""
        dot = self.canvas.create_oval(x, y, x+20, y+20, 
                                    tags=tag, fill='darkblue')
        self.canvas.tag_bind(dot, '<Button-1>', 
                            lambda e, t=tag: self.change_dot_color(t))
        self.dots[tag] = dot

    def change_dot_color(self, tag):
        """Toggle dot color between active (yellow) and inactive (darkblue)"""
        current_color = self.canvas.itemcget(self.dots[tag], 'fill')
        new_color = 'yellow' if current_color == 'darkblue' else 'darkblue'
        self.canvas.itemconfig(self.dots[tag], fill=new_color)
        self.decode()

    def get_col(self, cols, rows):
        """Calculate binary values for given columns based on active dots"""
        result = []
        for i in cols:
            value = 0
            for j in rows:
                tag = f"{i}:{j}"
                if self.canvas.itemcget(self.dots[tag], 'fill') == 'yellow':
                    value += j
            result.append(value)
        return result

    def check_parity(self):
        """Verify row and column parity for error detection"""
        row_errors = []
        col_errors = []
        
        # Check column parity (excluding special columns)
        for i in self.col:
            count = sum(1 for j in self.row if 
                       self.canvas.itemcget(self.dots[f"{i}:{j}"], 'fill') == 'yellow')
            if count % 2 == 0:
                if i not in (2, 3, 8, 0):  # Skip special columns
                    col_errors.append(i)
                    
        # Check row parity (excluding parity row)
        for j in self.row:
            count = sum(1 for i in self.col if 
                       self.canvas.itemcget(self.dots[f"{i}:{j}"], 'fill') == 'yellow')
            if count % 2 == 0 and j != 0:  # Skip parity row
                row_errors.append(j)
                
        if not row_errors and not col_errors:
            return "OK"
        return f"ROW {row_errors} COL {col_errors}"

    def decode(self):
        """Decode the dot matrix pattern to extract date and serial number"""
        try:
            rows = self.row[1:]  # Exclude parity row
            
            # Decode serial number (rightmost columns)
            serial = self.get_col(reversed(self.col[10:]), rows)
            
            # Decode date (year, month, day)
            ymd = self.get_col(reversed(self.col[5:8]), rows)
            year, month, day = ymd
            
            # Decode time (hour, minute)
            hm = self.get_col([4, 1], rows)
            hour, minute = hm
            
            # Format values with validation
            serial = ''.join(map(str, serial))
            year = year + 2000 if year < 70 else year + 1900
            month = month if month < 13 else "MM"
            day = day if day < 32 else "DD"
            hour = hour if hour < 24 else "HH"
            minute = minute if minute < 60 else "MM"
            
            # Check parity
            parity = self.check_parity()
            
            # Update result display
            self.code.set(f"Date: {year}-{month}-{day} at {hour}:{minute} -- "
                         f"Printer Serial Number: {serial} -- Parity Check: {parity}")
        except Exception as e:
            self.code.set("Error decoding pattern")

    def reset(self):
        """Reset grid to default state"""
        # Reset all dots to inactive
        for i in self.col:
            for j in self.row:
                tag = f"{i}:{j}"
                self.canvas.itemconfig(self.dots[tag], fill='darkblue')
        
        # Clear result
        self.code.set("")

    def create_grid(self):
        """Create grid with column and row labels"""
        x = 50
        y = 30
        
        # Create vertical labels
        self.canvas.create_text(x, y, text="parity", angle=90, fill='white')
        labels = [
            ("minute", "white"), ("unused", "grey"), ("unused", "grey"),
            ("hour", "white"), ("day", "white"), ("month", "white"),
            ("year", "white"), ("unused", "grey")
        ]
        
        for label, color in labels:
            x += 40
            self.canvas.create_text(x, y, text=label, angle=90, fill=color)
            
        # Create serial number label
        self.canvas.create_text(530, y, text="serial", fill='white')
        
        # Create column numbers
        x = 50
        for i in self.col:
            self.canvas.create_text(x, 70, text=str(i), fill='white')
            x += 40
            
        # Create row numbers
        y = 90
        for j in ['parity'] + [str(x) for x in self.row[1:]]:
            self.canvas.create_text(20, y, text=j, fill='white')
            y += 40

    def create_dots(self):
        """Create interactive dots on the grid"""
        x = 40
        for i in self.col:
            y = 80
            for j in self.row:
                self.create_dot(x, y, f"{i}:{j}")
                y += 40
            x += 40

    def create_labels(self):
        """Create result display label"""
        label = tk.Label(self.f3, textvariable=self.code, 
                        fg='yellow', bg='darkblue', width=104)
        label.pack(pady=4)

    def create_buttons(self):
        """Create control buttons"""
        for text, command in [
            ("Reset", self.reset),
            ("About", self.show_about),
            ("Exit", self.root.quit)
        ]:
            btn = tk.Button(self.f4, text=text, command=command,
                          relief='flat', fg='white', bg='blue', width=14)
            btn.pack(side='left', padx=2, pady=2)

    def show_about(self):
        """Display information about the application"""
        about = tk.Toplevel(self.root)
        about.configure(bg='black')
        about.title("About Docucolor Decoder")
        
        msg = ("Docucolor Decoder - (v1.0)\n\n"
               "This tool decodes printer tracking dots patterns found in "
               "color laser printer output. It can identify the printer's "
               "serial number and the date/time when the document was printed.\n\n"
               "Useful for:\n"
               "- Digital forensics\n"
               "- CTF challenges\n"
               "- Printer identification")
        
        message = tk.Message(about, text=msg, justify='left', aspect=250,
                           relief='flat', bg='black', fg='lightblue')
        message.pack(pady=10)
        
        tk.Button(about, text="OK", command=about.destroy,
                 relief='flat', fg='white', bg='blue').pack(pady=5)

    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = DocucolorDecoder()
    app.run()