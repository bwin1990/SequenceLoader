import logging
from datetime import datetime
from pathlib import Path

class Logger:
    def __init__(self):
        # 创建logs目录
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # 生成日志文件名（使用时间戳）
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = log_dir / f"operation_{timestamp}.log"
        
        # 配置日志
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def log_operation(self, source_file, target_file, line_count, status):
        """记录操作日志"""
        self.logger.info(f"源文件: {source_file}")
        self.logger.info(f"目标文件: {target_file}")
        self.logger.info(f"源文件行数: {line_count}")
        self.logger.info(f"操作状态: {status}")
        self.logger.info("-" * 50) 