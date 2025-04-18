import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import pymysql
import csv
from datetime import datetime
import random
from tkinter import ttk
import os
import shutil
import sys
import subprocess

class MainApp:
    def __init__(self):
        # App configuration
        self.app = ctk.CTk()
        self.app.title("Entrepôt Brahem Management System")
        
        # Set window size and position (centered on screen)
        window_width = 1200
        window_height = 600
        screen_width = self.app.winfo_screenwidth()
        screen_height = self.app.winfo_screenheight()
        
        # Calculate position
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        
        self.app.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.app.minsize(1000, 700)
        
        # Style configuration
        ctk.set_appearance_mode("light")
        self.setup_style()
        
        # Database connection
        self.conn = self.connection()
        self.cursor = self.conn.cursor()
        
        # Initialize database table
        self.initialize_database()
        
        # Data variables
        self.placeholder_vars = [ctk.StringVar() for _ in range(5)]
        self.job_options = ['Truck driver', 'Guard', 'Warehouse']
        self.numeric = '1234567890'
        self.alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        
        # Create widgets
        self.create_widgets()
        self.refresh_table()
        
        self.app.mainloop()
    
    def initialize_database(self):
       
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS stocks (
                    `Employe_id` VARCHAR(10) PRIMARY KEY,
                    `name` VARCHAR(100),
                    `Phone number` VARCHAR(20),
                    `salary` VARCHAR(20),
                    `job` VARCHAR(50),
                    `date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    `excel_file_path` VARCHAR(255)
                )
            """)
            self.conn.commit()
        except Exception as e:
            CTkMessagebox(title="Database Error", message=f"Failed to initialize database: {str(e)}", icon="cancel")

    def setup_style(self):
        """Configure custom styles for widgets"""
        self.button_style = {
            "font": ("Arial", 12, "bold"),
            "height": 35,
            "border_width": 0
        }
        
        self.entry_style = {
            "font": ("Arial", 12),
            "height": 35
        }
    
    def connection(self):
        """Create database connection"""
        return pymysql.connect(
            host='localhost',
            user='root',
            password='',
            db='stockmanagementsystem'
        )
    
    def generate_id(self):
        """Generate random employee ID"""
        employee_id = ''.join(random.choice(self.numeric) for _ in range(3))
        employee_id += '-' + random.choice(self.alpha)
        self.placeholder_vars[0].set(employee_id)
    
    def read(self):
        """Read data from database"""
        self.cursor.connection.ping()
        sql = "SELECT `Employe_id`, `name`, `Phone number`, `salary`, `job`, `date`, `excel_file_path` FROM stocks ORDER BY `Employe_id` DESC"
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        self.conn.commit()
        return results
    
    def refresh_table(self):
        """Refresh the treeview with current data"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            results = self.read()
            for row in results:
                self.tree.insert("", "end", values=row[:6])  # Exclude excel_file_path from display
        except Exception as e:
            CTkMessagebox(title="Error", message=f"Failed to load data: {str(e)}", icon="cancel")

    def create_widgets(self):
        """Create all GUI elements"""
        # Main container
        main_frame = ctk.CTkFrame(self.app, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title frame with centered text and Excel button
        title_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        title_frame.pack(fill="x", pady=(0, 20))
        
        # Create a grid layout for the title frame (3 columns)
        title_frame.grid_columnconfigure(0, weight=1)
        title_frame.grid_columnconfigure(1, weight=2)
        title_frame.grid_columnconfigure(2, weight=1)
        
        # Excel import button on the right (column 2)
        self.import_button = ctk.CTkButton(
            title_frame,
            text="📤 Import Excel",
            command=self.import_excel,
            **self.button_style,
            fg_color="#4CAF50",
            hover_color="#45a049"
        )
        self.import_button.grid(row=0, column=2, padx=10, sticky="e")
        
        # Centered title label (column 1)
        ctk.CTkLabel(
            title_frame,
            text="ENTREPÔT BRAHEM MANAGEMENT SYSTEM",
            font=("Arial", 20, "bold")
        ).grid(row=0, column=1, sticky="nsew")
        
        # Form and buttons frame
        form_frame = ctk.CTkFrame(main_frame)
        form_frame.pack(fill="x", pady=(0, 20))
        
        # Form entries
        labels = ["Employe ID", "Name", "Phone number", "Salary", "Job"]
        for i, text in enumerate(labels):
            ctk.CTkLabel(form_frame, text=text).grid(row=i, column=0, padx=10, pady=5, sticky="e")
        
        self.entry_id = ctk.CTkEntry(form_frame, textvariable=self.placeholder_vars[0], **self.entry_style)
        self.entry_name = ctk.CTkEntry(form_frame, textvariable=self.placeholder_vars[1], **self.entry_style)
        self.entry_phone = ctk.CTkEntry(form_frame, textvariable=self.placeholder_vars[2], **self.entry_style)
        self.entry_salary = ctk.CTkEntry(form_frame, textvariable=self.placeholder_vars[3], **self.entry_style)
        self.combo_job = ctk.CTkComboBox(form_frame, values=self.job_options, variable=self.placeholder_vars[4], **self.entry_style)
        
        self.entry_id.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        self.entry_name.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        self.entry_phone.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        self.entry_salary.grid(row=3, column=1, padx=10, pady=5, sticky="ew")
        self.combo_job.grid(row=4, column=1, padx=10, pady=5, sticky="ew")
        
        # Generate ID button
        ctk.CTkButton(
            form_frame,
            text="GENERATE ID",
            command=self.generate_id,
            **self.button_style
        ).grid(row=0, column=2, padx=10, pady=5)
        
        # Action buttons
        buttons = [
            ("SAVE", self.save),
            ("UPDATE", self.update),
            ("DELETE", self.delete),
            ("SELECT", self.select),
            ("FIND", self.find),
            ("CLEAR", self.clear),
            ("EXPORT EXCEL", self.export_excel),
            ("DATABASE", self.open_database_window),
            ("📂 ATTACH EXCEL", self.save_employee_excel),
            ("📄 OPEN EXCEL", self.open_employee_excel)
        ]
        
        for i, (text, command) in enumerate(buttons):
            row = 5 + (i // 4)
            col = i % 4
            ctk.CTkButton(
                form_frame,
                text=text,
                command=command,
                **self.button_style
            ).grid(row=row, column=col, padx=10, pady=5, sticky="ew")
        
        # Treeview frame
        tree_frame = ctk.CTkFrame(main_frame)
        tree_frame.pack(fill="both", expand=True)
        
        # Treeview
        self.tree = ttk.Treeview(
            tree_frame,
            columns=("Employe Id", "Name", "Phone number", "Salary", "Job", "Date"),
            show="headings",
            height=25
        )
        
        # Configure columns
        columns = {
            "Employe Id": 100,
            "Name": 150,
            "Phone number": 120,
            "Salary": 100,
            "Job": 120,
            "Date": 120
        }
        
        for col, width in columns.items():
            self.tree.column(col, width=width)
            self.tree.heading(col, text=col)
        
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

    # ======================== CORE FUNCTIONS ========================
    def save(self):
        """Save new employee record"""
        employee_id = self.placeholder_vars[0].get()
        name = self.placeholder_vars[1].get()
        phone = self.placeholder_vars[2].get()
        salary = self.placeholder_vars[3].get()
        job = self.placeholder_vars[4].get()
        
        if not all([employee_id, name, phone, salary, job]):
            CTkMessagebox(title="Warning", message="Please fill up all entries", icon="warning")
            return
        
        if len(employee_id) < 5 or not (employee_id[3] == '-' and 
                                      all(c in self.numeric for c in employee_id[:3]) and 
                                      employee_id[4] in self.alpha):
            CTkMessagebox(title="Warning", message="Invalid Employee ID format", icon="warning")
            return
        
        try:
            self.cursor.connection.ping()
            sql = f"SELECT * FROM stocks WHERE `Employe_id` = '{employee_id}'"
            self.cursor.execute(sql)
            if self.cursor.fetchall():
                CTkMessagebox(title="Warning", message="Employee ID already exists", icon="warning")
                return
            
            sql = f"""INSERT INTO stocks (`Employe_id`, `name`, `Phone number`, `salary`, `job`) 
                      VALUES ('{employee_id}','{name}','{phone}','{salary}','{job}')"""
            self.cursor.execute(sql)
            self.conn.commit()
            
            for var in self.placeholder_vars:
                var.set('')
                
            self.refresh_table()
            CTkMessagebox(title="Success", message="Employee record saved successfully", icon="check")
            
        except Exception as e:
            CTkMessagebox(title="Error", message=f"Error while saving: {str(e)}", icon="cancel")

    def update(self):
        """Update existing employee record"""
        try:
            selected_item = self.tree.selection()[0]
            selected_id = self.tree.item(selected_item)['values'][0]
        except:
            CTkMessagebox(title="Warning", message="Please select a record to update", icon="warning")
            return
        
        # Get current form values but keep the original ID
        original_id = selected_id
        name = self.placeholder_vars[1].get()
        phone = self.placeholder_vars[2].get()
        salary = self.placeholder_vars[3].get()
        job = self.placeholder_vars[4].get()
        
        if not all([original_id, name, phone, salary, job]):
            CTkMessagebox(title="Warning", message="Please fill up all entries", icon="warning")
            return
        
        try:
            self.cursor.connection.ping()
            sql = f"""UPDATE stocks SET `name`='{name}', `Phone number`='{phone}', 
                      `salary`='{salary}', `job`='{job}' WHERE `Employe_id`='{original_id}'"""
            self.cursor.execute(sql)
            self.conn.commit()
            
            for var in self.placeholder_vars:
                var.set('')
            
            self.refresh_table()
            CTkMessagebox(title="Success", message="Employee record updated successfully", icon="check")
            
        except Exception as e:
            CTkMessagebox(title="Error", message=f"Error while updating: {str(e)}", icon="cancel")

    def delete(self):
        """Delete employee record"""
        try:
            selected_item = self.tree.selection()[0]
        except:
            CTkMessagebox(title="Warning", message="Please select a record to delete", icon="warning")
            return
        
        confirm = CTkMessagebox(title="Confirm", message="Delete the selected record?", 
                              icon="question", option_1="Cancel", option_2="Delete")
        if confirm.get() == "Cancel":
            return
        
        employee_id = self.tree.item(selected_item)['values'][0]
        
        try:
            self.cursor.connection.ping()
            # First delete the associated Excel file if it exists
            sql = f"SELECT excel_file_path FROM stocks WHERE Employe_id = '{employee_id}'"
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            
            if result and result[0]:
                try:
                    os.remove(result[0])
                except Exception as e:
                    print(f"Warning: Could not delete file {result[0]}: {str(e)}")
            
            # Then delete the database record
            sql = f"DELETE FROM stocks WHERE `Employe_id` = '{employee_id}'"
            self.cursor.execute(sql)
            self.conn.commit()
            
            self.refresh_table()
            CTkMessagebox(title="Success", message="Record deleted successfully", icon="check")
            
        except Exception as e:
            CTkMessagebox(title="Error", message=f"Error while deleting: {str(e)}", icon="cancel")

    def select(self):
        """Select record from treeview"""
        try:
            selected_item = self.tree.selection()[0]
            values = self.tree.item(selected_item)['values']
            
            for i in range(5):
                self.placeholder_vars[i].set(values[i])
                
        except:
            CTkMessagebox(title="Warning", message="Please select a record", icon="warning")

    def find(self):
        """Find records by search criteria"""
        fields = [
            self.placeholder_vars[0].get(),  # ID
            self.placeholder_vars[1].get(),  # Name
            self.placeholder_vars[2].get(),  # Phone
            self.placeholder_vars[3].get(),  # Salary
            self.placeholder_vars[4].get()   # Job
        ]
        
        if not any(fields):
            CTkMessagebox(title="Warning", message="Please fill at least one search field", icon="warning")
            return
        
        try:
            self.cursor.connection.ping()
            conditions = []
            if fields[0]: conditions.append(f"`Employe_id` LIKE '%{fields[0]}%'")
            if fields[1]: conditions.append(f"`name` LIKE '%{fields[1]}%'")
            if fields[2]: conditions.append(f"`Phone number` LIKE '%{fields[2]}%'")
            if fields[3]: conditions.append(f"`salary` LIKE '%{fields[3]}%'")
            if fields[4]: conditions.append(f"`job` LIKE '%{fields[4]}%'")
            
            sql = f"""SELECT `Employe_id`, `name`, `Phone number`, `salary`, `job`, `date` 
                      FROM stocks WHERE {' OR '.join(conditions)} ORDER BY `Employe_id` DESC"""
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            
            if not results:
                CTkMessagebox(title="Info", message="No matching records found", icon="info")
                return
            
            # Clear and populate treeview with results
            for item in self.tree.get_children():
                self.tree.delete(item)
                
            for row in results:
                self.tree.insert("", "end", values=row)
                
        except Exception as e:
            CTkMessagebox(title="Error", message=f"Search error: {str(e)}", icon="cancel")

    def clear(self):
        """Clear form fields"""
        for var in self.placeholder_vars:
            var.set('')

    def export_excel(self):
        """Export data to CSV file"""
        try:
            self.cursor.connection.ping()
            sql = "SELECT `Employe_id`, `name`, `Phone number`, `salary`, `job`, `date` FROM stocks ORDER BY `Employe_id` DESC"
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            
            date = datetime.now().strftime("%Y-%m-%d_%H-%M")
            filename = f"employees_{date}.csv"
            
            with open(filename, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Employe Id", "Name", "Phone number", "Salary", "Job", "Date"])
                writer.writerows(results)
            
            CTkMessagebox(title="Success", message=f"Data exported to {filename}", icon="check")
            
        except Exception as e:
            CTkMessagebox(title="Error", message=f"Export failed: {str(e)}", icon="cancel")

    def open_database_window(self):
        """Open database view in new window"""
        db_window = ctk.CTkToplevel(self.app)
        db_window.title("Employee Database")
        db_window.geometry("1000x600")
        
        tree_frame = ctk.CTkFrame(db_window)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        tree = ttk.Treeview(
            tree_frame,
            columns=("Employe Id", "Name", "Phone number", "Salary", "Job", "Date"),
            show="headings",
            height=25
        )
        
        columns = {
            "Employe Id": 100,
            "Name": 150,
            "Phone number": 120,
            "Salary": 100,
            "Job": 120,
            "Date": 120
        }
        
        for col, width in columns.items():
            tree.column(col, width=width)
            tree.heading(col, text=col)
        
        tree.pack(fill="both", expand=True)
        
        try:
            results = self.read()
            for row in results:
                tree.insert("", "end", values=row[:6])  # Exclude excel_file_path
        except Exception as e:
            CTkMessagebox(title="Error", message=f"Failed to load data: {str(e)}", icon="cancel")

    def import_excel(self):
        """Import employee data from Excel file"""
        try: 
            from tkinter import filedialog
            import openpyxl
            
            filepath = filedialog.askopenfilename(
                title="Select Excel File",
                filetypes=[("Excel Files", "*.xlsx *.xls")]
            )
            
            if not filepath:
                return  # User cancelled
            
            workbook = openpyxl.load_workbook(filepath)
            sheet = workbook.active
            
            for row in sheet.iter_rows(min_row=2, values_only=True):  # Skip header
                emp_id, name, phone, salary, job = row[:5]  # Get first 5 columns
                
                # Validate data
                if not all([emp_id, name, phone, salary, job]):
                    continue
                
                try:
                    self.cursor.connection.ping()
                    sql = f"""INSERT INTO stocks 
                              (`Employe_id`, `name`, `Phone number`, `salary`, `job`) 
                              VALUES (%s, %s, %s, %s, %s)"""
                    self.cursor.execute(sql, (emp_id, name, phone, salary, job))
                    self.conn.commit()
                    
                except pymysql.IntegrityError:
                    # Skip duplicate entries
                    continue
                except Exception as e:
                    CTkMessagebox(title="Error", 
                                message=f"Error importing record {emp_id}: {str(e)}", 
                                icon="cancel")
                    continue
            
            self.refresh_table()
            CTkMessagebox(title="Success", 
                         message="Excel data imported successfully!", 
                         icon="check")
            
        except Exception as e:
            CTkMessagebox(title="Error", 
                         message=f"Failed to import Excel: {str(e)}", 
                         icon="cancel")

    # ======================== EXCEL ATTACHMENT FUNCTIONS ========================
    def save_employee_excel(self):
        """Save an Excel file for the selected employee"""
        try:
            selected_item = self.tree.selection()[0]
            employee_id = self.tree.item(selected_item)['values'][0]
        except:
            CTkMessagebox(title="Warning", message="Please select an employee first!", icon="warning")
            return

        # Ask for the Excel file to upload
        from tkinter import filedialog
        filepath = filedialog.askopenfilename(
            title="Select Excel File for Employee",
            filetypes=[("Excel Files", "*.xlsx *.xls")]
        )

        if not filepath:
            return  # User cancelled

        # Create employee_data directory if it doesn't exist
        os.makedirs("employee_data", exist_ok=True)

        # Generate normalized path
        new_filename = os.path.normpath(os.path.join("employee_data", f"{employee_id}_data.xlsx"))
        
        try:
            # Copy the file
            shutil.copy(filepath, new_filename)
            
            # Get absolute path
            abs_path = os.path.abspath(new_filename)
            
            # Update database with normalized absolute path
            self.cursor.connection.ping()
            sql = "UPDATE stocks SET excel_file_path = %s WHERE Employe_id = %s"
            self.cursor.execute(sql, (abs_path, employee_id))
            self.conn.commit()
            
            CTkMessagebox(title="Success", 
                         message=f"Excel file saved for {employee_id} at:\n{abs_path}", 
                         icon="check")
        except Exception as e:
            CTkMessagebox(title="Error", 
                         message=f"Failed to save file: {str(e)}", 
                         icon="cancel")

    def open_employee_excel(self):
        """Open the Excel file associated with the selected employee"""
        try:
            selected_item = self.tree.selection()[0]
            employee_id = self.tree.item(selected_item)['values'][0]
        except:
            CTkMessagebox(title="Warning", message="Please select an employee first!", icon="warning")
            return

        try:
            self.cursor.connection.ping()
            sql = f"SELECT excel_file_path FROM stocks WHERE Employe_id = '{employee_id}'"
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            
            if not result or not result[0]:
                CTkMessagebox(title="Info", message="No Excel file linked to this employee.", icon="info")
                return

            filepath = os.path.normpath(result[0])
            print(f"Attempting to open: {filepath}")  # Debug output
            
            if os.path.exists(filepath):
                try:
                    if os.name == 'nt':  # Windows
                        os.startfile(filepath)
                    elif os.name == 'posix':  # macOS/Linux
                        opener = 'open' if sys.platform == 'darwin' else 'xdg-open'
                        subprocess.run([opener, filepath])
                except Exception as e:
                    CTkMessagebox(title="Error", 
                                message=f"Failed to open file: {str(e)}", 
                                icon="cancel")
            else:
                CTkMessagebox(title="Error", 
                             message=f"File not found at:\n{filepath}", 
                             icon="cancel")
        except Exception as e:
            CTkMessagebox(title="Error", 
                         message=f"Database error: {str(e)}", 
                         icon="cancel")

def main():
    app = MainApp()
    return MainApp()

if __name__ == "__main__":
    
    pass