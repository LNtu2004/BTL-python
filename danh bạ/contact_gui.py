import tkinter as tk
from tkinter import ttk, messagebox
from contacts import ContactManager

class ContactApp:
    def __init__(self, root):
        self.manager = ContactManager()
        self.root = root
        self.root.title("Quản lý danh bạ")

        # Frame nhập liệu
        frame = tk.Frame(root)
        frame.pack(pady=10)

        tk.Label(frame, text="Tên").grid(row=0, column=0)
        tk.Label(frame, text="SĐT").grid(row=1, column=0)
        tk.Label(frame, text="Email").grid(row=2, column=0)

        self.name_entry = tk.Entry(frame)
        self.phone_entry = tk.Entry(frame)
        self.email_entry = tk.Entry(frame)

        self.name_entry.grid(row=0, column=1)
        self.phone_entry.grid(row=1, column=1)
        self.email_entry.grid(row=2, column=1)

        # Frame tìm kiếm
        search_frame = tk.Frame(root)
        search_frame.pack(pady=5)

        tk.Label(search_frame, text="Tìm tên:").grid(row=0, column=0)
        self.search_entry = tk.Entry(search_frame)
        self.search_entry.grid(row=0, column=1)
        tk.Button(search_frame, text="Tìm", command=self.search_contacts).grid(row=0, column=2)

        # Buttons chức năng
        btn_frame = tk.Frame(root)
        btn_frame.pack()

        tk.Button(btn_frame, text="Thêm", command=self.add_contact).grid(row=0, column=0)
        tk.Button(btn_frame, text="Sửa", command=self.update_contact).grid(row=0, column=1)
        tk.Button(btn_frame, text="Xóa", command=self.delete_contact).grid(row=0, column=2)

        # Treeview hiển thị danh bạ
        self.tree = ttk.Treeview(root, columns=("Tên", "SĐT", "Email"), show="headings")
        self.tree.heading("Tên", text="Tên")
        self.tree.heading("SĐT", text="SĐT")
        self.tree.heading("Email", text="Email")
        self.tree.pack(pady=10)

        # Xử lý chọn dòng trên Treeview
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        self.load_contacts()

    def load_contacts(self, filtered_contacts=None):
        """Tải danh bạ lên Treeview (có thể lọc nếu tìm kiếm)"""
        self.tree.delete(*self.tree.get_children())
        contacts_to_display = filtered_contacts if filtered_contacts else self.manager.contacts
        for contact in contacts_to_display:
            self.tree.insert("", "end", values=(contact["name"], contact["phone"], contact["email"]))

    def save_contacts(self):
        """Ghi dữ liệu vào file JSON"""
        self.manager.save_contacts()

    def add_contact(self):
        """Thêm mới liên hệ"""
        name, phone, email = self.name_entry.get(), self.phone_entry.get(), self.email_entry.get()
        if name and phone and email:
            self.manager.add_contact(name, phone, email)
            self.save_contacts()
            self.load_contacts()
            self.clear_fields()
        else:
            messagebox.showerror("Lỗi", "Vui lòng nhập đủ thông tin.")

    def update_contact(self):
        """Cập nhật thông tin liên hệ"""
        selected_item = self.tree.selection()
        if selected_item:
            index = self.tree.index(selected_item[0])
            name, phone, email = self.name_entry.get(), self.phone_entry.get(), self.email_entry.get()
            self.manager.update_contact(index, name, phone, email)
            self.save_contacts()
            self.load_contacts()
            self.clear_fields()
        else:
            messagebox.showerror("Lỗi", "Chọn một liên hệ để sửa.")

    def delete_contact(self):
        """Xóa liên hệ"""
        selected_item = self.tree.selection()
        if selected_item:
            index = self.tree.index(selected_item[0])
            self.manager.delete_contact(index)
            self.save_contacts()
            self.load_contacts()
            self.clear_fields()
        else:
            messagebox.showerror("Lỗi", "Chọn một liên hệ để xóa.")

    def search_contacts(self):
        """Tìm kiếm liên hệ theo tên"""
        search_name = self.search_entry.get().strip().lower()
        if search_name:
            filtered_contacts = [c for c in self.manager.contacts if search_name in c["name"].lower()]
            self.load_contacts(filtered_contacts)
        else:
            self.load_contacts()

    def on_select(self, event):
        """Xử lý chọn dòng trong Treeview để điền vào ô nhập"""
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0])['values']
            self.name_entry.delete(0, tk.END)
            self.phone_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)
            self.name_entry.insert(0, values[0])
            self.phone_entry.insert(0, values[1])
            self.email_entry.insert(0, values[2])

    def clear_fields(self):
        """Xóa ô nhập sau khi thao tác"""
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ContactApp(root)
    root.mainloop()