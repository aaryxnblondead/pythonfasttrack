import customtkinter as ctk
import psycopg2
import tkinter as tk
from tkinter import messagebox

class TodoApp:
        def __init__(self, root):
            self.root = root
            self.root.title("To-Do List App")
            self.root.geometry("400x500")
            ctk.set_appearance_mode("dark")
            ctk.set_default_color_theme("green")

            try:
                self.conn = psycopg2.connect(
                    host='ep-cool-king-a13nnu77.ap-southeast-1.aws.neon.tech',
                    database='adb',
                    user='adb_owner',
                    password='fHsyLIKQ1bx0'
                )
                self.cur = self.conn.cursor()
                self.cur.execute("DROP TABLE IF EXISTS tasks")
                self.cur.execute("""
                    CREATE TABLE tasks (
                        task_id SERIAL PRIMARY KEY,
                        task_name TEXT NOT NULL,
                        completed BOOLEAN DEFAULT FALSE
                    )
                """)
                self.conn.commit()
            except psycopg2.Error as e:
                messagebox.showerror("Database Error", f"Failed to connect to database: {str(e)}")

            self.task_entry = ctk.CTkEntry(self.root, font=("Helvetica", 14), height=35, width=260)
            self.task_entry.place(x=20, y=20)

            self.add_button = ctk.CTkButton(self.root, text="Add Task", font=("Helvetica", 12), 
                                        command=self.add_task, height=35, width=90)
            self.add_button.place(x=290, y=20)

            self.task_listbox = tk.Listbox(self.root, font=("Helvetica", 12), bg="#2c2c34", fg="white", 
                                        selectbackground="#0db39e", selectforeground="white", 
                                        bd=0, highlightthickness=0, relief="flat", width=40, height=15)
            self.task_listbox.place(x=20, y=70)
            
            self.delete_button = ctk.CTkButton(self.root, text="Delete", font=("Helvetica", 12),
                                            fg_color="#e63946", hover_color="#c12c36",
                                            command=self.delete_task, height=35, width=90)
            self.delete_button.place(x=20, y=430)

            self.complete_button = ctk.CTkButton(self.root, text="Complete", font=("Helvetica", 12),
                                            command=self.complete_task, height=35, width=100)
            self.complete_button.place(x=130, y=430)

            self.clear_button = ctk.CTkButton(self.root, text="Clear All", font=("Helvetica", 12),
                                        fg_color="#e63946", hover_color="#c12c36",
                                        command=self.clear_tasks, height=35, width=130)
            self.clear_button.place(x=250, y=430)
            
            self.load_tasks()
        def load_tasks(self):
            self.task_listbox.delete(0, tk.END)
            self.cur.execute("SELECT task_id, task_name, completed FROM tasks ORDER BY task_id")
            tasks = self.cur.fetchall()
            for task in tasks:
                task_id, task_name, completed = task
                display_text = f"{task_id}. {task_name}"
                if completed:
                    display_text = f"✔ {display_text}"
                self.task_listbox.insert(tk.END, display_text)

        def add_task(self):
            task = self.task_entry.get().strip()
            if task:
                self.cur.execute("INSERT INTO tasks (task_name) VALUES (%s) RETURNING task_id", (task,))
                task_id = self.cur.fetchone()[0]
                self.conn.commit()
                
                self.task_listbox.insert(tk.END, f"{task_id}. {task}")
                self.task_entry.delete(0, tk.END)
                print(f"Success: Task '{task}' has been added with ID {task_id}!")
            else:
                messagebox.showwarning("Warning", "Please enter a task!")

        def delete_task(self):
            try:
                selected_index = self.task_listbox.curselection()[0]
                task_text = self.task_listbox.get(selected_index)
                task_id = int(task_text.split('.')[0].replace('✔ ', ''))
                
                self.cur.execute("DELETE FROM tasks WHERE task_id = %s", (task_id,))
                self.conn.commit()
                self.task_listbox.delete(selected_index)
                print(f"Success: Task has been deleted!")
            except IndexError:
                messagebox.showwarning("Warning", "Please select a task to delete!")

        def complete_task(self):
            try:
                selected_index = self.task_listbox.curselection()[0]
                task_text = self.task_listbox.get(selected_index)
                task_id = int(task_text.split('.')[0].replace('✔ ', ''))
                
                self.cur.execute("UPDATE tasks SET completed = TRUE WHERE task_id = %s", (task_id,))
                self.conn.commit()
                self.load_tasks()
                print(f"Success: Task has been marked as complete!")
            except IndexError:
                messagebox.showwarning("Warning", "Please select a task to mark as complete!")

        def clear_tasks(self):
            if messagebox.askyesno("Confirm", "Are you sure you want to clear all tasks?"):
                self.cur.execute("DELETE FROM tasks")
                self.conn.commit()
                self.task_listbox.delete(0, tk.END)
                print("Success: All tasks have been cleared!")

if __name__ == "__main__":
    root = ctk.CTk()
    app = TodoApp(root)
    root.mainloop()