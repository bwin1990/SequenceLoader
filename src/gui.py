import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import yaml
from pathlib import Path

class ConfigEditor(tk.Toplevel):
    def __init__(self, parent, config_path):
        super().__init__(parent)
        self.title("配置编辑器")
        self.config_path = config_path
        self.load_config()
        self.setup_ui()
        
    def load_config(self):
        """加载配置文件"""
        with open(self.config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
            
    def save_config(self):
        """保存配置文件"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                yaml.dump(self.config, f, allow_unicode=True)
            messagebox.showinfo("成功", "配置已保存")
        except Exception as e:
            messagebox.showerror("错误", f"保存配置失败：{str(e)}")
            
    def setup_ui(self):
        """设置UI界面"""
        # 创建notebook用于标签页
        notebook = ttk.Notebook(self)
        notebook.pack(padx=10, pady=10, fill='both', expand=True)
        
        # 目标文件设置页
        target_frame = ttk.Frame(notebook)
        notebook.add(target_frame, text="合成序列文件")
        
        # 创建目标文件编辑区
        row = 0
        self.target_entries = {}
        for target, info in self.config['target_files'].items():
            ttk.Label(target_frame, text=f"文件 {target}:").grid(row=row, column=0, padx=5, pady=5)
            
            # 路径设置
            path_frame = ttk.Frame(target_frame)
            path_frame.grid(row=row+1, column=0, columnspan=2, padx=5, pady=2)
            
            path_entry = ttk.Entry(path_frame, width=50)
            path_entry.insert(0, info['path'])
            path_entry.pack(side='left', padx=2)
            
            browse_btn = ttk.Button(path_frame, text="浏览",
                                  command=lambda e=path_entry: self.browse_path(e))
            browse_btn.pack(side='left', padx=2)
            
            # 行数范围设置
            range_frame = ttk.Frame(target_frame)
            range_frame.grid(row=row+2, column=0, columnspan=2, padx=5, pady=2)
            
            ttk.Label(range_frame, text="行数范围:").pack(side='left')
            min_entry = ttk.Entry(range_frame, width=10)
            min_entry.insert(0, str(info['line_range'][0]))
            min_entry.pack(side='left', padx=2)
            
            ttk.Label(range_frame, text="至").pack(side='left')
            max_entry = ttk.Entry(range_frame, width=10)
            max_entry.insert(0, str(info['line_range'][1]))
            max_entry.pack(side='left', padx=2)
            
            self.target_entries[target] = {
                'path': path_entry,
                'range': (min_entry, max_entry)
            }
            
            row += 3
            
        # 默认源目录设置页
        default_frame = ttk.Frame(notebook)
        notebook.add(default_frame, text="默认载入from")
        
        ttk.Label(default_frame, text="默认源文件目录:").pack(padx=5, pady=5)
        self.default_dir_entry = ttk.Entry(default_frame, width=50)
        self.default_dir_entry.insert(0, self.config['default_source_dir'])
        self.default_dir_entry.pack(padx=5, pady=2)
        
        browse_btn = ttk.Button(default_frame, text="浏览",
                              command=lambda: self.browse_directory(self.default_dir_entry))
        browse_btn.pack(pady=5)
        
        # 保存按钮
        save_btn = ttk.Button(self, text="保存配置", command=self.update_config)
        save_btn.pack(pady=10)
        
    def browse_path(self, entry):
        """浏览文件路径"""
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")]
        )
        if path:
            entry.delete(0, tk.END)
            entry.insert(0, path)
            
    def browse_directory(self, entry):
        """浏览文件夹"""
        directory = filedialog.askdirectory()
        if directory:
            entry.delete(0, tk.END)
            entry.insert(0, directory)
            
    def update_config(self):
        """更新配置"""
        try:
            # 更新目标文件配置
            for target, entries in self.target_entries.items():
                self.config['target_files'][target]['path'] = entries['path'].get()
                self.config['target_files'][target]['line_range'] = [
                    int(entries['range'][0].get()),
                    int(entries['range'][1].get())
                ]
            
            # 更新默认源目录
            self.config['default_source_dir'] = self.default_dir_entry.get()
            
            # 保存配置
            self.save_config()
            
        except ValueError as e:
            messagebox.showerror("错误", "行数范围必须是数字！")
        except Exception as e:
            messagebox.showerror("错误", f"更新配置失败：{str(e)}")

class GUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("DNA序列文件处理工具")
        self.setup_ui()
        
    def setup_ui(self):
        """设置主界面"""
        # 创建主框架
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill='both', expand=True)
        
        # 添加文件选择按钮
        select_btn = ttk.Button(main_frame, text="载入序列文件选择", command=self.select_file)
        select_btn.pack(pady=5)
        
        # 添加配置编辑按钮
        config_btn = ttk.Button(main_frame, text="编辑配置", command=self.open_config_editor)
        config_btn.pack(pady=5)
    
    def open_config_editor(self):
        """打开配置编辑器"""
        config_path = Path("config/config.yaml")
        if not config_path.exists():
            self.show_error("配置文件不存在！")
            return
        ConfigEditor(self.window, config_path)
    
    def select_file(self):
        """打开文件选择对话框"""
        file_path = filedialog.askopenfilename(
            title="选择序列文件",
            filetypes=[("Text files", "*.txt")]
        )
        return file_path
    
    def confirm_operation(self, source_file, target_file):
        """确认操作对话框"""
        return messagebox.askyesno(
            "确认操作",
            f"是否将文件 {source_file} 的内容复制到 {target_file}?"
        ) 
    
    def show_error(self, message):
        """显示错误消息"""
        messagebox.showerror("错误", message)
        
    def show_success(self, message):
        """显示成功消息"""
        messagebox.showinfo("成功", message)
        
    def run(self):
        """运行GUI主循环"""
        self.window.mainloop() 