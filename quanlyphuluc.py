import json
import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from pathlib import Path

# Cấu hình giao diện
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class JSONEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quản lý Phụ lục JSON")
        self.root.geometry("800x600")
        
        # Biến lưu trữ dữ liệu
        self.data = []
        self.json_file = "phuluc.json"
        
        # Tải dữ liệu hiện có
        self.load_data()
        
        # Tạo giao diện
        self.create_widgets()
        
        # Hiển thị dữ liệu
        self.display_data()
    
    def load_data(self):
        """Tải dữ liệu từ file JSON"""
        try:
            if Path(self.json_file).exists():
                with open(self.json_file, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
            else:
                self.data = []
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải file JSON: {str(e)}")
            self.data = []
    
    def save_data(self):
        """Lưu dữ liệu vào file JSON (đã sắp xếp)"""
        try:
            # Sắp xếp dữ liệu theo tên
            sorted_data = sorted(self.data, key=lambda x: x['name'])
            
            with open(self.json_file, 'w', encoding='utf-8') as f:
                json.dump(sorted_data, f, indent=4, ensure_ascii=False)
            
            return True
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lưu file JSON: {str(e)}")
            return False
    
    def create_widgets(self):
        """Tạo các widget cho giao diện"""
        # Frame chính
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame nhập liệu
        self.input_frame = ctk.CTkFrame(self.main_frame)
        self.input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ctk.CTkLabel(self.input_frame, text="Tên:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.name_entry = ctk.CTkEntry(self.input_frame, width=400)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        ctk.CTkLabel(self.input_frame, text="Đường dẫn:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.url_entry = ctk.CTkEntry(self.input_frame, width=400)
        self.url_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        # Nút thêm
        self.add_button = ctk.CTkButton(
            self.input_frame, 
            text="Thêm mục", 
            command=self.add_item
        )
        self.add_button.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Frame hiển thị dữ liệu
        self.display_frame = ctk.CTkFrame(self.main_frame)
        self.display_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Thanh cuộn
        self.scrollbar = ctk.CTkScrollbar(self.display_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Listbox hiển thị dữ liệu
        self.listbox = tk.Listbox(
            self.display_frame,
            yscrollcommand=self.scrollbar.set,
            font=('Arial', 12),
            selectbackground='#3B8ED0',
            selectforeground='white'
        )
        self.listbox.pack(fill=tk.BOTH, expand=True)
        self.scrollbar.configure(command=self.listbox.yview)
        
        # Nút xóa mục đã chọn
        self.delete_button = ctk.CTkButton(
            self.main_frame,
            text="Xóa mục đã chọn",
            command=self.delete_selected,
            fg_color="#D35B58",
            hover_color="#C34C49"
        )
        self.delete_button.pack(pady=5)
    
    def display_data(self):
        """Hiển thị dữ liệu trong Listbox"""
        self.listbox.delete(0, tk.END)
        for item in self.data:
            self.listbox.insert(tk.END, f"{item['name']} - {item['url']}")
    
    def add_item(self):
        """Thêm mục mới vào dữ liệu"""
        name = self.name_entry.get().strip()
        url = self.url_entry.get().strip()
        
        if not name or not url:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ tên và đường dẫn")
            return
        
        # Thêm mục mới
        self.data.append({
            "name": name,
            "url": url
        })
        
        # Lưu và sắp xếp lại dữ liệu
        if self.save_data():
            # Tải lại dữ liệu để đảm bảo đồng bộ
            self.load_data()
            self.display_data()
            
            # Xóa nội dung nhập
            self.name_entry.delete(0, tk.END)
            self.url_entry.delete(0, tk.END)
            
            messagebox.showinfo("Thành công", "Đã thêm mục mới và lưu file JSON")
    
    def delete_selected(self):
        """Xóa mục đã chọn"""
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn mục cần xóa")
            return
        
        # Xác nhận trước khi xóa
        if not messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa mục này?"):
            return
        
        # Xóa mục đã chọn
        index = selected[0]
        del self.data[index]
        
        # Lưu lại dữ liệu
        if self.save_data():
            # Tải lại dữ liệu để đảm bảo đồng bộ
            self.load_data()
            self.display_data()
            messagebox.showinfo("Thành công", "Đã xóa mục và lưu file JSON")

if __name__ == "__main__":
    root = ctk.CTk()
    app = JSONEditorApp(root)
    root.mainloop()
