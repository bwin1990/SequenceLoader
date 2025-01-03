import sys
from pathlib import Path
from tkinter import messagebox
from file_handler import FileHandler
from gui import GUI
from logger import Logger

class DNAFileProcessor:
    def __init__(self):
        self.gui = GUI()
        self.logger = Logger()
        
        # 加载配置文件
        config_path = Path("config/config.yaml")
        if not config_path.exists():
            self.show_error("配置文件不存在！")
            sys.exit(1)
            
        self.file_handler = FileHandler(config_path)
        
        # 设置文件选择回调
        self.gui.set_file_selected_callback(self.handle_selected_file)
    
    def handle_selected_file(self, file_path):
        """处理选中的文件"""
        try:
            # 更新状态
            self.gui.update_status(f"正在处理文件: {file_path}")
            
            # 获取目标文件
            target_file = self.file_handler.get_target_file(file_path)
            
            if not target_file:
                self.show_error("无法找到匹配的目标文件！")
                self.gui.update_status("处理失败：无匹配目标文件")
                return
                
            # 获取行数（用于日志）
            line_count = sum(1 for _ in open(file_path))
            
            # 确认操作
            if not self.gui.confirm_operation(file_path, target_file):
                self.gui.update_status("操作已取消")
                return
                
            # 执行复制
            self.file_handler.copy_content(file_path, target_file)
            
            # 记录日志
            self.logger.log_operation(
                file_path, 
                target_file,
                line_count,
                "成功"
            )
            
            # 显示成功消息
            self.show_success("文件处理完成！")
            self.gui.update_status("处理完成")
            
        except Exception as e:
            self.show_error(f"处理过程中出错：{str(e)}")
            self.logger.log_operation(
                file_path,
                target_file if 'target_file' in locals() else "未知",
                line_count if 'line_count' in locals() else 0,
                f"失败: {str(e)}"
            )
            self.gui.update_status("处理失败")

    def show_error(self, message):
        """显示错误消息"""
        messagebox.showerror("错误", message)
        
    def show_success(self, message):
        """显示成功消息"""
        messagebox.showinfo("成功", message)
        
    def run(self):
        """运行程序"""
        self.gui.run()

def main():
    app = DNAFileProcessor()
    app.run()
    
if __name__ == "__main__":
    main() 