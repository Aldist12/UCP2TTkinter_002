import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
import threading
import time

class ModernNotification:
    def __init__(self, parent, message, notification_type="info", duration=3000):
        self.parent = parent
        self.message = message
        self.type = notification_type
        self.duration = duration
        
        # Warna berdasarkan tipe notifikasi
        self.colors = {
            "success": {"bg": "#10B981", "fg": "white"},
            "error": {"bg": "#EF4444", "fg": "white"},
            "warning": {"bg": "#F59E0B", "fg": "white"},
            "info": {"bg": "#3B82F6", "fg": "white"}
        }
        
        self.show_notification()
    
    def show_notification(self):
        # Buat window notifikasi
        self.notification = tk.Toplevel(self.parent)
        self.notification.withdraw()  # Sembunyikan dulu
        self.notification.overrideredirect(True)  # Hilangkan title bar
        self.notification.attributes('-alpha', 0.0)  # Mulai transparan
        self.notification.attributes('-topmost', True)  # Selalu di atas
        
        # Frame utama notifikasi
        color = self.colors.get(self.type, self.colors["info"])
        frame = tk.Frame(self.notification, bg=color["bg"], padx=20, pady=15)
        frame.pack(fill='both', expand=True)
        
        # Icon berdasarkan tipe
        icons = {
            "success": "✓",
            "error": "✗",
            "warning": "⚠",
            "info": "ⓘ"
        }
        
        # Label icon
        icon_label = tk.Label(frame, text=icons.get(self.type, "ⓘ"), 
                             bg=color["bg"], fg=color["fg"], 
                             font=('Arial', 16, 'bold'))
        icon_label.pack(side='left', padx=(0, 10))
        
        # Label pesan
        message_label = tk.Label(frame, text=self.message, 
                               bg=color["bg"], fg=color["fg"],
                               font=('Arial', 11, 'normal'),
                               wraplength=300)
        message_label.pack(side='left', fill='x', expand=True)
        
        # Posisikan di tengah atas parent window
        self.notification.update_idletasks()
        parent_x = self.parent.winfo_x()
        parent_y = self.parent.winfo_y()
        parent_width = self.parent.winfo_width()
        
        notif_width = self.notification.winfo_reqwidth()
        x = parent_x + (parent_width - notif_width) // 2
        y = parent_y + 50
        
        self.notification.geometry(f"+{x}+{y}")
        self.notification.deiconify()
        
        # Animasi fade in
        self.fade_in()
        
        # Auto hide setelah duration
        self.parent.after(self.duration, self.fade_out)
    
    def fade_in(self):
        alpha = self.notification.attributes('-alpha')
        if alpha < 0.95:
            self.notification.attributes('-alpha', alpha + 0.05)
            self.parent.after(20, self.fade_in)
    
    def fade_out(self):
        alpha = self.notification.attributes('-alpha')
        if alpha > 0:
            self.notification.attributes('-alpha', alpha - 0.05)
            self.parent.after(20, self.fade_out)
        else:
            self.notification.destroy()

class EmployeeManagement:
    def __init__(self, root):
        self.root = root
        self.root.title("✨ Sistem Management Pegawai Modern")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)
        
        # Set tema modern
        self.setup_theme()
        
        # Inisialisasi database
        self.init_database()
        
        # Setup GUI
        self.setup_gui()
        
        # Load data awal
        self.load_data()
    
    def setup_theme(self):
        """Setup tema modern untuk aplikasi"""
        style = ttk.Style()
        
        # Gunakan tema yang tersedia
        available_themes = style.theme_names()
        if 'clam' in available_themes:
            style.theme_use('clam')
        elif 'alt' in available_themes:
            style.theme_use('alt')
        
        # Konfigurasi warna modern
        self.colors = {
            'primary': '#2563EB',      # Blue 600
            'primary_light': '#DBEAFE', # Blue 100
            'success': '#10B981',       # Emerald 500
            'success_light': '#D1FAE5', # Emerald 100
            'warning': '#F59E0B',       # Amber 500
            'error': '#EF4444',         # Red 500
            'background': '#F8FAFC',    # Slate 50
            'card': '#FFFFFF',          # White
            'text': '#1E293B',          # Slate 800
            'text_light': '#64748B',    # Slate 500
            'border': '#E2E8F0'         # Slate 200
        }
        
        # Style kustomisasi
        style.configure('Title.TLabel', font=('Segoe UI', 24, 'bold'), 
                       foreground=self.colors['primary'])
        style.configure('Heading.TLabel', font=('Segoe UI', 12, 'bold'), 
                       foreground=self.colors['text'])
        style.configure('Modern.TButton', padding=(15, 8))
        style.configure('Success.TButton', foreground=self.colors['success'])
        style.configure('Danger.TButton', foreground=self.colors['error'])
        
        # Set background root
        self.root.configure(bg=self.colors['background'])
    
    def show_notification(self, message, type_notif="info"):
        """Tampilkan notifikasi modern"""
        ModernNotification(self.root, message, type_notif)
    
    def init_database(self):
        """Inisialisasi database SQLite"""
        try:
            self.conn = sqlite3.connect('data_pegawai.db')
            self.cursor = self.conn.cursor()
            
            # Membuat tabel pegawai jika belum ada
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS pegawai (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nama TEXT NOT NULL UNIQUE,
                    alamat TEXT NOT NULL,
                    posisi TEXT NOT NULL,
                    tahun_masuk INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            self.conn.commit()
            self.show_notification("Database berhasil diinisialisasi", "success")
        except sqlite3.Error as e:
            self.show_notification(f"Gagal menginisialisasi database: {e}", "error")
    
    def setup_gui(self):
        """Setup antarmuka pengguna dengan tema modern"""
        # Konfigurasi root untuk responsive
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Canvas untuk scrollable content
        canvas = tk.Canvas(self.root, bg=self.colors['background'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        # Bind canvas resize untuk responsive content
        def configure_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            # Update canvas window width untuk responsive
            canvas_width = event.width
            canvas.itemconfig(canvas_window, width=canvas_width)
        
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.bind('<Configure>', configure_scroll_region)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Frame utama dengan padding - gunakan grid untuk better control
        main_frame = tk.Frame(scrollable_frame, bg=self.colors['background'])
        main_frame.pack(fill='both', expand=True, padx=30, pady=20)
        
        # Konfigurasi grid untuk main_frame
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Header dengan gradient effect (simulasi)
        header_frame = tk.Frame(main_frame, bg=self.colors['primary'], height=100)
        header_frame.grid(row=0, column=0, sticky='ew', pady=(0, 30))
        header_frame.grid_propagate(False)
        header_frame.grid_columnconfigure(0, weight=1)
        
        # Judul dengan icon
        title_frame = tk.Frame(header_frame, bg=self.colors['primary'])
        title_frame.grid(row=0, column=0, sticky='ew')
        title_frame.grid_columnconfigure(0, weight=1)
        
        title_label = tk.Label(title_frame, text="🏢 SISTEM MANAGEMENT PEGAWAI", 
                              font=('Segoe UI', 20, 'bold'),
                              fg='white', bg=self.colors['primary'])
        title_label.grid(row=0, column=0, pady=(15, 5))
        
        subtitle_label = tk.Label(title_frame, text="Kelola data pegawai dengan mudah dan modern", 
                                 font=('Segoe UI', 10),
                                 fg='white', bg=self.colors['primary'])
        subtitle_label.grid(row=1, column=0, pady=(0, 15))
        
        # Card untuk input form
        input_card = tk.Frame(main_frame, bg=self.colors['card'], relief='solid', bd=1)
        input_card.grid(row=1, column=0, sticky='ew', pady=(0, 20))
        input_card.grid_columnconfigure(0, weight=1)
        
        # Header card
        card_header = tk.Frame(input_card, bg=self.colors['primary_light'], height=50)
        card_header.grid(row=0, column=0, sticky='ew')
        card_header.grid_propagate(False)
        card_header.grid_columnconfigure(0, weight=1)
        
        card_title = tk.Label(card_header, text="📝 Form Data Pegawai", 
                             font=('Segoe UI', 14, 'bold'),
                             fg=self.colors['text'], bg=self.colors['primary_light'])
        card_title.grid(row=0, column=0, pady=15)
        
        # Form content
        form_frame = tk.Frame(input_card, bg=self.colors['card'])
        form_frame.grid(row=1, column=0, sticky='ew', padx=30, pady=20)
        form_frame.grid_columnconfigure(0, weight=1)
        
        # Grid untuk form yang lebih rapi
        form_grid = tk.Frame(form_frame, bg=self.colors['card'])
        form_grid.grid(row=0, column=0, sticky='ew')
        form_grid.grid_columnconfigure(0, weight=1)
        
        # Input fields dengan style modern
        self.create_modern_input(form_grid, "👤 Nama Lengkap:", 0, "nama_var", "nama_entry")
        self.create_modern_input(form_grid, "🏠 Alamat:", 1, "alamat_var", "alamat_entry")
        self.create_modern_input(form_grid, "💼 Posisi/Jabatan:", 2, "posisi_var", "posisi_entry")
        self.create_modern_input(form_grid, "📅 Tahun Masuk:", 3, "tahun_var", "tahun_entry")
        
        # Button frame dengan style modern
        button_frame = tk.Frame(form_frame, bg=self.colors['card'])
        button_frame.grid(row=1, column=0, pady=(20, 0))
        
        # Tombol dengan warna berbeda
        self.create_modern_button(button_frame, "➕ Tambah", self.add_employee, self.colors['success'])
        self.create_modern_button(button_frame, "✏️ Update", self.update_employee, self.colors['primary'])
        self.create_modern_button(button_frame, "🗑️ Hapus", self.delete_employee, self.colors['error'])
        self.create_modern_button(button_frame, "🧹 Clear", self.clear_fields, self.colors['text_light'])
        self.create_modern_button(button_frame, "🔄 Refresh", self.load_data, self.colors['text_light'])
        
        # Card untuk pencarian
        search_card = tk.Frame(main_frame, bg=self.colors['card'], relief='solid', bd=1)
        search_card.grid(row=2, column=0, sticky='ew', pady=(0, 20))
        search_card.grid_columnconfigure(0, weight=1)
        
        search_header = tk.Frame(search_card, bg=self.colors['primary_light'], height=50)
        search_header.grid(row=0, column=0, sticky='ew')
        search_header.grid_propagate(False)
        search_header.grid_columnconfigure(0, weight=1)
        
        search_title = tk.Label(search_header, text="🔍 Pencarian Data", 
                               font=('Segoe UI', 14, 'bold'),
                               fg=self.colors['text'], bg=self.colors['primary_light'])
        search_title.grid(row=0, column=0, pady=15)
        
        search_content = tk.Frame(search_card, bg=self.colors['card'])
        search_content.grid(row=1, column=0, sticky='ew', padx=30, pady=20)
        search_content.grid_columnconfigure(0, weight=1)
        
        search_label = tk.Label(search_content, text="🔎 Cari berdasarkan nama:", 
                               font=('Segoe UI', 10), fg=self.colors['text'], bg=self.colors['card'])
        search_label.grid(row=0, column=0, sticky='w')
        
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_content, textvariable=self.search_var, 
                               font=('Segoe UI', 11), relief='solid', bd=1,
                               bg='white', fg=self.colors['text'])
        search_entry.grid(row=1, column=0, sticky='ew', pady=(5, 0), ipady=8)
        search_entry.bind('<KeyRelease>', self.search_employee)
        
        # Card untuk tabel data
        table_card = tk.Frame(main_frame, bg=self.colors['card'], relief='solid', bd=1)
        table_card.grid(row=3, column=0, sticky='nsew', pady=(0, 20))
        table_card.grid_columnconfigure(0, weight=1)
        table_card.grid_rowconfigure(1, weight=1)  # Biar tabel bisa expand
        
        # Configure main_frame untuk tabel yang expandable
        main_frame.grid_rowconfigure(3, weight=1)
        
        table_header = tk.Frame(table_card, bg=self.colors['primary_light'], height=50)
        table_header.grid(row=0, column=0, sticky='ew')
        table_header.grid_propagate(False)
        table_header.grid_columnconfigure(0, weight=1)
        
        table_title = tk.Label(table_header, text="📊 Data Pegawai", 
                              font=('Segoe UI', 14, 'bold'),
                              fg=self.colors['text'], bg=self.colors['primary_light'])
        table_title.grid(row=0, column=0, pady=15)
        
        # Treeview dengan style modern
        tree_frame = tk.Frame(table_card, bg=self.colors['card'])
        tree_frame.grid(row=1, column=0, sticky='nsew', padx=20, pady=20)
        tree_frame.grid_columnconfigure(0, weight=1)
        tree_frame.grid_rowconfigure(0, weight=1)
        
        # Style treeview
        style = ttk.Style()
        style.configure("Modern.Treeview", background="white", foreground=self.colors['text'],
                       fieldbackground="white", font=('Segoe UI', 10))
        style.configure("Modern.Treeview.Heading", font=('Segoe UI', 11, 'bold'))
        
        self.tree = ttk.Treeview(tree_frame, style="Modern.Treeview",
                                columns=('ID', 'Nama', 'Alamat', 'Posisi', 'Tahun Masuk'), 
                                show='headings', height=12)
        
        # Konfigurasi kolom dengan icon
        self.tree.heading('ID', text='🆔 ID')
        self.tree.heading('Nama', text='👤 Nama Lengkap')
        self.tree.heading('Alamat', text='🏠 Alamat')
        self.tree.heading('Posisi', text='💼 Posisi')
        self.tree.heading('Tahun Masuk', text='📅 Tahun Masuk')
        
        # Lebar kolom dengan alignment yang konsisten
        self.tree.column('ID', width=60, anchor=tk.CENTER, minwidth=50)
        self.tree.column('Nama', width=200, anchor=tk.CENTER, minwidth=150)
        self.tree.column('Alamat', width=250, anchor=tk.CENTER, minwidth=200)
        self.tree.column('Posisi', width=150, anchor=tk.CENTER, minwidth=120)
        self.tree.column('Tahun Masuk', width=120, anchor=tk.CENTER, minwidth=100)
        
        # Scrollbar dengan style
        scrollbar_tree = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_tree.set)
        
        # Grid layout
        self.tree.grid(row=0, column=0, sticky='nsew')
        scrollbar_tree.grid(row=0, column=1, sticky='ns')
        
        # Bind events
        self.tree.bind('<Double-1>', self.on_item_select)
        self.tree.bind('<Button-1>', self.on_single_click)
        
        # Status bar modern
        status_frame = tk.Frame(main_frame, bg=self.colors['primary'], height=40)
        status_frame.grid(row=4, column=0, sticky='ew', pady=(20, 0))
        status_frame.grid_propagate(False)
        status_frame.grid_columnconfigure(0, weight=1)
        
        self.status_var = tk.StringVar()
        self.status_var.set("🟢 Aplikasi siap digunakan")
        status_label = tk.Label(status_frame, textvariable=self.status_var, 
                               font=('Segoe UI', 10), fg='white', bg=self.colors['primary'])
        status_label.grid(row=0, column=0, pady=10)
        
        # Grid canvas dan scrollbar dengan proper weights
        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Bind mouse wheel untuk scroll
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # ID tersembunyi untuk update
        self.selected_id = None
        
    def create_modern_input(self, parent, label_text, row, var_name, entry_name):
        """Buat input field dengan style modern"""
        # Frame untuk setiap input
        input_frame = tk.Frame(parent, bg=self.colors['card'])
        input_frame.grid(row=row, column=0, sticky='ew', pady=10)
        input_frame.grid_columnconfigure(0, weight=1)
        
        # Label
        label = tk.Label(input_frame, text=label_text, 
                        font=('Segoe UI', 11, 'bold'), 
                        fg=self.colors['text'], bg=self.colors['card'])
        label.grid(row=0, column=0, sticky='w')
        
        # Variable dan Entry
        var = tk.StringVar()
        setattr(self, var_name, var)
        
        entry = tk.Entry(input_frame, textvariable=var, 
                        font=('Segoe UI', 11), relief='solid', bd=1,
                        bg='white', fg=self.colors['text'])
        entry.grid(row=1, column=0, sticky='ew', pady=(5, 0), ipady=8)
        setattr(self, entry_name, entry)
        
    def create_modern_button(self, parent, text, command, color):
        """Buat tombol dengan style modern"""
        button = tk.Button(parent, text=text, command=command,
                          font=('Segoe UI', 10, 'bold'), 
                          bg=color, fg='white', relief='flat',
                          padx=20, pady=8, cursor='hand2')
        button.pack(side='left', padx=5)
        
        # Hover effect
        def on_enter(e):
            button.config(bg=self.lighten_color(color))
        def on_leave(e):
            button.config(bg=color)
            
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
        
    def lighten_color(self, color):
        """Buat warna lebih terang untuk hover effect"""
        # Implementasi sederhana untuk lighten color
        color_map = {
            self.colors['success']: '#34D399',
            self.colors['primary']: '#3B82F6', 
            self.colors['error']: '#F87171',
            self.colors['text_light']: '#94A3B8'
        }
        return color_map.get(color, color)
    
    def add_employee(self):
        """Menambah pegawai baru dengan validasi nama unik"""
        if not self.validate_input():
            return
        
        try:
            # Cek apakah nama sudah ada
            self.cursor.execute('SELECT COUNT(*) FROM pegawai WHERE LOWER(nama) = LOWER(?)', 
                              (self.nama_var.get().strip(),))
            if self.cursor.fetchone()[0] > 0:
                self.show_notification("Nama pegawai sudah terdaftar! Gunakan nama yang berbeda.", "warning")
                self.nama_entry.focus()
                return
            
            self.cursor.execute('''
                INSERT INTO pegawai (nama, alamat, posisi, tahun_masuk)
                VALUES (?, ?, ?, ?)
            ''', (self.nama_var.get().strip(), self.alamat_var.get().strip(), 
                  self.posisi_var.get().strip(), int(self.tahun_var.get())))
            
            self.conn.commit()
            self.status_var.set(f"✅ Pegawai {self.nama_var.get()} berhasil ditambahkan")
            self.show_notification(f"Pegawai '{self.nama_var.get()}' berhasil ditambahkan!", "success")
            self.clear_fields()
            self.load_data()
            
        except sqlite3.IntegrityError:
            self.show_notification("Nama pegawai sudah terdaftar! Gunakan nama yang berbeda.", "warning")
        except sqlite3.Error as e:
            self.show_notification(f"Gagal menambah pegawai: {e}", "error")
            self.status_var.set("❌ Gagal menambah pegawai")
    
    def update_employee(self):
        """Update data pegawai dengan validasi nama unik"""
        if not self.selected_id:
            self.show_notification("Pilih pegawai yang akan diupdate terlebih dahulu!", "warning")
            return
        
        if not self.validate_input():
            return
        
        try:
            # Cek apakah nama sudah ada (kecuali untuk record yang sedang diedit)
            self.cursor.execute('SELECT COUNT(*) FROM pegawai WHERE LOWER(nama) = LOWER(?) AND id != ?', 
                              (self.nama_var.get().strip(), self.selected_id))
            if self.cursor.fetchone()[0] > 0:
                self.show_notification("Nama pegawai sudah terdaftar! Gunakan nama yang berbeda.", "warning")
                self.nama_entry.focus()
                return
            
            old_name = self.get_employee_name(self.selected_id)
            
            self.cursor.execute('''
                UPDATE pegawai SET nama=?, alamat=?, posisi=?, tahun_masuk=?
                WHERE id=?
            ''', (self.nama_var.get().strip(), self.alamat_var.get().strip(), 
                  self.posisi_var.get().strip(), int(self.tahun_var.get()), self.selected_id))
            
            self.conn.commit()
            self.status_var.set(f"✅ Data pegawai berhasil diupdate")
            self.show_notification(f"Data pegawai '{old_name}' berhasil diupdate!", "success")
            self.clear_fields()
            self.load_data()
            
        except sqlite3.IntegrityError:
            self.show_notification("Nama pegawai sudah terdaftar! Gunakan nama yang berbeda.", "warning")
        except sqlite3.Error as e:
            self.show_notification(f"Gagal mengupdate pegawai: {e}", "error")
            self.status_var.set("❌ Gagal mengupdate pegawai")
    
    def get_employee_name(self, employee_id):
        """Ambil nama pegawai berdasarkan ID"""
        try:
            self.cursor.execute('SELECT nama FROM pegawai WHERE id=?', (employee_id,))
            result = self.cursor.fetchone()
            return result[0] if result else "Unknown"
        except:
            return "Unknown"
    
    def delete_employee(self):
        """Hapus pegawai dengan konfirmasi modern"""
        selection = self.tree.selection()
        if not selection:
            self.show_notification("Pilih pegawai yang akan dihapus terlebih dahulu!", "warning")
            return
        
        item = self.tree.item(selection[0])
        employee_name = item['values'][1]
        
        # Konfirmasi hapus dengan dialog modern
        result = messagebox.askyesno(
            "🗑️ Konfirmasi Hapus", 
            f"Yakin ingin menghapus data pegawai:\n\n'{employee_name}'?\n\nTindakan ini tidak dapat dibatalkan.",
            icon='warning'
        )
        
        if result:
            try:
                employee_id = item['values'][0]
                
                self.cursor.execute('DELETE FROM pegawai WHERE id=?', (employee_id,))
                self.conn.commit()
                
                self.status_var.set(f"🗑️ Pegawai {employee_name} berhasil dihapus")
                self.show_notification(f"Data pegawai '{employee_name}' berhasil dihapus!", "success")
                self.clear_fields()
                self.load_data()
                
            except sqlite3.Error as e:
                self.show_notification(f"Gagal menghapus pegawai: {e}", "error")
                self.status_var.set("❌ Gagal menghapus pegawai")
    
    def load_data(self):
        """Load semua data pegawai ke treeview"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            # Urutkan berdasarkan ID, bukan nama
            self.cursor.execute('SELECT id, nama, alamat, posisi, tahun_masuk FROM pegawai ORDER BY id')
            rows = self.cursor.fetchall()
            
            for row in rows:
                self.tree.insert('', tk.END, values=row)
            
            self.status_var.set(f"📊 Menampilkan {len(rows)} data pegawai")
            
        except sqlite3.Error as e:
            self.show_notification(f"Gagal memuat data: {e}", "error")
            self.status_var.set("❌ Gagal memuat data")
    
    def search_employee(self, event=None):
        """Pencarian pegawai berdasarkan nama dengan highlight"""
        search_term = self.search_var.get().strip()
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            if search_term:
                self.cursor.execute('''
                    SELECT id, nama, alamat, posisi, tahun_masuk FROM pegawai 
                    WHERE nama LIKE ? OR alamat LIKE ? OR posisi LIKE ?
                    ORDER BY id
                ''', (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
            else:
                # Jika tidak ada search term, tampilkan semua data urut berdasarkan ID
                self.cursor.execute('SELECT id, nama, alamat, posisi, tahun_masuk FROM pegawai ORDER BY id')
            
            rows = self.cursor.fetchall()
            
            for row in rows:
                self.tree.insert('', tk.END, values=row)
            
            if search_term:
                self.status_var.set(f"🔍 Ditemukan {len(rows)} pegawai untuk '{search_term}'")
            else:
                self.status_var.set(f"📊 Menampilkan {len(rows)} data pegawai")
            
        except sqlite3.Error as e:
            self.show_notification(f"Gagal mencari data: {e}", "error")
            self.status_var.set("❌ Gagal mencari data")
    
    def on_item_select(self, event):
        """Handle double click pada item treeview"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            values = item['values']
            
            self.selected_id = values[0]
            self.nama_var.set(values[1])
            self.alamat_var.set(values[2])
            self.posisi_var.set(values[3])
            self.tahun_var.set(values[4])
            
            self.status_var.set(f"✏️ Siap edit data pegawai: {values[1]}")
            self.show_notification(f"Data pegawai '{values[1]}' siap untuk diedit", "info")
    
    def on_single_click(self, event):
        """Handle single click untuk highlight"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            values = item['values']
            self.status_var.set(f"📋 Terpilih: {values[1]} - {values[3]}")
    
    def clear_fields(self):
        """Clear semua input fields dengan animasi"""
        self.nama_var.set('')
        self.alamat_var.set('')
        self.posisi_var.set('')
        self.tahun_var.set('')
        self.selected_id = None
        self.status_var.set("🧹 Form berhasil dibersihkan")
        
        # Clear selection di treeview
        for item in self.tree.selection():
            self.tree.selection_remove(item)
    
    def validate_input(self):
        """Validasi input form dengan pesan yang lebih user-friendly"""
        # Validasi nama
        if not self.nama_var.get().strip():
            self.show_notification("Nama lengkap wajib diisi!", "warning")
            self.nama_entry.focus()
            return False
        
        if len(self.nama_var.get().strip()) < 3:
            self.show_notification("Nama minimal 3 karakter!", "warning")
            self.nama_entry.focus()
            return False
        
        # Validasi alamat
        if not self.alamat_var.get().strip():
            self.show_notification("Alamat wajib diisi!", "warning")
            self.alamat_entry.focus()
            return False
        
        # Validasi posisi
        if not self.posisi_var.get().strip():
            self.show_notification("Posisi/Jabatan wajib diisi!", "warning")
            self.posisi_entry.focus()
            return False
        
        # Validasi tahun masuk
        try:
            tahun = int(self.tahun_var.get().strip())
            current_year = datetime.now().year
            if tahun < 1950 or tahun > current_year:
                self.show_notification(f"Tahun masuk harus antara 1950 - {current_year}!", "warning")
                self.tahun_entry.focus()
                return False
        except ValueError:
            self.show_notification("Tahun masuk harus berupa angka yang valid!", "warning")
            self.tahun_entry.focus()
            return False
        
        return True
    
    def __del__(self):
        """Destructor untuk menutup koneksi database"""
        if hasattr(self, 'conn'):
            self.conn.close()

def main():
    # Set DPI awareness untuk Windows (opsional)
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass
    
    root = tk.Tk()
    
    # Set icon aplikasi (jika ada file icon)
    try:
        root.iconbitmap('icon.ico')  # Ganti dengan path icon Anda
    except:
        pass
    
    app = EmployeeManagement(root)
    
    # Handle window close dengan konfirmasi
    def on_closing():
        result = messagebox.askyesno(
            "🚪 Keluar Aplikasi", 
            "Yakin ingin menutup aplikasi?\n\nSemua data sudah tersimpan di database.",
            icon='question'
        )
        if result:
            if hasattr(app, 'conn'):
                app.conn.close()
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Tampilkan pesan selamat datang
    root.after(1000, lambda: app.show_notification(
        "Selamat datang di Sistem Management Pegawai Modern! 🎉", "info"))
    
    # Center window di layar
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()

if __name__ == "__main__":
    main()