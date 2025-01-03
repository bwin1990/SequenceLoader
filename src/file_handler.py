import yaml
from pathlib import Path

class FileHandler:
    def __init__(self, config_path):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
    
    def get_target_file(self, source_file_path):
        """根据源文件行数确定目标文件"""
        line_count = sum(1 for _ in open(source_file_path))
        
        for target, info in self.config['target_files'].items():
            min_lines, max_lines = info['line_range']
            if min_lines <= line_count <= max_lines:
                return info['path']
        return None
    
    def copy_content(self, source_path, target_path):
        """清空目标文件并复制内容"""
        with open(target_path, 'w') as f:
            f.write('')  # 清空文件
            
        with open(source_path, 'r') as source:
            content = source.read()
            with open(target_path, 'w') as target:
                target.write(content) 