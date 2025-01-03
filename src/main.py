import sys
from pathlib import Path
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
        
    def show_error(self, message):
        """显示错误消息"""
        self.gui.window.messagebox.showerror("错误", message)
        
    def show_success(self, message):
        """显示成功消息"""
        self.gui.window.messagebox.showinfo("成功", message)
        
    def process(self):
        """主处理流程"""
        # 1. 选择源文件
        source_file = self.gui.select_file()
        if not source_file:
            return
            
        # 2. 根据行数判断目标文件
        target_file = self.file_handler.get_target_file(source_file)
        if not target_file:
            self.show_error("无法找到匹配的目标文件！")
            return
            
        # 3. 确认操作
        if not self.gui.confirm_operation(source_file, target_file):
            return
            
        try:
            # 4. 执行复制
            self.file_handler.copy_content(source_file, target_file)
            
            # 5. 记录日志
            line_count = sum(1 for _ in open(source_file))
            self.logger.log_operation(
                source_file, 
                target_file,
                line_count,
                "成功"
            )
            
            # 6. 显示成功消息
            self.show_success("文件处理完成！")
            
        except Exception as e:
            self.show_error(f"处理过程中出错：{str(e)}")
            self.logger.log_operation(
                source_file,
                target_file,
                line_count,
                f"失败: {str(e)}"
            )

def main():
    app = DNAFileProcessor()
    app.gui.run()  # 运行GUI主循环
    
if __name__ == "__main__":
    main() 