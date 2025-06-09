import json

class ContactManager:
    def __init__(self, filename="contacts.json"):
        self.filename = filename
        self.contacts = self.load_contacts()

    def load_contacts(self):
        """Đọc dữ liệu từ file JSON khi khởi động"""
        try:
            with open(self.filename, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []  

    def save_contacts(self):
        """Lưu dữ liệu vào file JSON"""
        with open(self.filename, "w") as file:
            json.dump(self.contacts, file, indent=4)

    def add_contact(self, name, phone, email):
        """Thêm mới liên hệ"""
        self.contacts.append({"name": name, "phone": phone, "email": email})
        self.save_contacts()

    def update_contact(self, index, name, phone, email):
        """Cập nhật thông tin liên hệ"""
        if 0 <= index < len(self.contacts):
            self.contacts[index] = {"name": name, "phone": phone, "email": email}
            self.save_contacts()

    def delete_contact(self, index):
        """Xóa liên hệ"""
        if 0 <= index < len(self.contacts):
            del self.contacts[index]
            self.save_contacts()