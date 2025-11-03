import os
import argparse
import shutil
from pathlib import Path

class StructureAnalyzer:
    def __init__(self, root_dir="."):
        self.root_dir = Path(root_dir)
        self.ignore_dirs = {'.git', '__pycache__', '.idea', 'node_modules', 'venv', 'env', '.vscode'}
        self.ignore_files = {'.DS_Store', 'deploy.sh'}  # 只忽略系統文件和部署腳本本身
        
    def analyze_structure(self):
        """分析目錄結構並返回需要創建的目錄和文件"""
        directories = set()
        init_files = set()
        all_files = {}  # 儲存文件路徑和內容
        
        # 總是包含根目錄
        directories.add(".")
        
        for root, dirs, files in os.walk(self.root_dir):
            # 過濾忽略的目錄
            dirs[:] = [d for d in dirs if d not in self.ignore_dirs]
            
            current_path = Path(root)
            
            # 處理相對路徑
            try:
                relative_path = current_path.relative_to(self.root_dir)
            except ValueError:
                continue
            
            # 收集目錄
            directories.add(str(relative_path))
            
            # 收集文件
            for file in files:
                if file in self.ignore_files:
                    continue
                    
                file_path = current_path / file
                
                try:
                    relative_file_path = file_path.relative_to(self.root_dir)
                except ValueError:
                    continue
                
                if file == "__init__.py":
                    init_files.add(str(relative_file_path.parent))
                else:
                    # 讀取文件內容
                    try:
                        # 嘗試多種編碼讀取文件
                        encodings = ['utf-8', 'gbk', 'big5', 'cp950', 'latin-1']
                        content = None
                        for encoding in encodings:
                            try:
                                with open(file_path, 'r', encoding=encoding) as f:
                                    content = f.read()
                                break
                            except UnicodeDecodeError:
                                continue
                        
                        # 如果是二進制文件，標記為二進制
                        if content is None:
                            with open(file_path, 'rb') as f:
                                content = f.read()
                            all_files[str(relative_file_path)] = {'content': content, 'binary': True}
                        else:
                            all_files[str(relative_file_path)] = {'content': content, 'binary': False}
                            
                    except Exception as e:
                        print(f"讀取文件 {file_path} 時出錯: {e}")
                        # 創建空文件作為備份
                        all_files[str(relative_file_path)] = {'content': '', 'binary': False}
        
        return sorted(directories), sorted(init_files), all_files
    
    def detect_requirements(self):
        """檢測項目依賴並生成 requirements.txt 內容"""
        requirements_content = []
        
        # 檢查常見的依賴文件
        req_files = ['requirements.txt', 'pyproject.toml', 'setup.py']
        for req_file in req_files:
            req_path = self.root_dir / req_file
            if req_path.exists():
                print(f"檢測到依賴文件: {req_file}")
                try:
                    if req_file == 'requirements.txt':
                        encodings = ['utf-8', 'gbk', 'big5', 'cp950', 'latin-1']
                        for encoding in encodings:
                            try:
                                with open(req_path, 'r', encoding=encoding) as f:
                                    content = f.read().strip()
                                    if content:
                                        requirements_content = content.split('\n')
                                        print(f"成功讀取 requirements.txt (編碼: {encoding})")
                                        break
                            except UnicodeDecodeError:
                                continue
                    break
                except Exception as e:
                    print(f"讀取 {req_file} 時出錯: {e}")
                    break
        
        # 如果沒有找到依賴文件或讀取失敗，使用預設內容
        if not requirements_content:
            print("使用預設依賴配置")
            requirements_content = [
                "# Core Web Framework",
                "fastapi==0.104.1",
                "uvicorn[standard]==0.24.0",
                "python-multipart==0.0.6",
                "",
                "# AI and Machine Learning", 
                "openai==1.3.0",
                "torch==2.1.0",
                "torchaudio==2.1.0", 
                "torchvision==0.16.0",
                "",
                "# Video Processing",
                "moviepy==1.0.3",
                "pydub==0.25.1",
                "",
                "# Utilities",
                "python-dotenv==1.0.0",
                "pydantic==2.4.2",
                "requests==2.31.0"
            ]
        
        return requirements_content

def generate_deploy_script(directories, init_files, all_files, requirements_content, output_file="deploy.sh"):
    """生成部署腳本"""
    
    script_content = [
        "#!/bin/bash",
        "",
        "# 自動生成的部署腳本",
        "# 創建項目目錄結構和文件...",
        "",
        "set -e  # 遇到錯誤時退出",
        "",
        "# ==================== 顏色定義 ====================",
        "RED='\\033[0;31m'",
        "GREEN='\\033[0;32m'", 
        "YELLOW='\\033[1;33m'",
        "BLUE='\\033[0;34m'",
        "NC='\\033[0m' # No Color",
        "",
        "# ==================== 工具函數 ====================",
        "log_info() {",
        "    echo -e \"${BLUE}[INFO]${NC} $1\"",
        "}",
        "",
        "log_success() {",
        "    echo -e \"${GREEN}[SUCCESS]${NC} $1\"",
        "}",
        "",
        "log_warning() {",
        "    echo -e \"${YELLOW}[WARNING]${NC} $1\"", 
        "}",
        "",
        "log_error() {",
        "    echo -e \"${RED}[ERROR]${NC} $1\"",
        "}",
        "",
        "# ==================== 部署開始 ====================",
        "log_info \"開始部署項目...\"",
        ""
    ]
    
    # 創建目錄 (過濾當前目錄 ".")
    script_content.append("log_info \"創建項目目錄結構...\"")
    for directory in directories:
        if directory != ".":
            script_content.append(f"mkdir -p \"{directory}\"")
    
    # 創建 __init__.py 文件
    if init_files:
        script_content.append("")
        script_content.append("log_info \"創建 Python 包初始化文件...\"")
        for init_dir in init_files:
            if init_dir != ".":  # 避免在根目錄創建 __init__.py
                script_content.append(f"touch \"{init_dir}/__init__.py\"")
    
    # 生成所有其他文件
    if all_files:
        script_content.append("")
        script_content.append("log_info \"創建項目文件...\"")
        
        binary_files = []
        for file_path, file_info in sorted(all_files.items()):
            script_content.append("")
            
            if file_info.get('binary', False):
                # 二進制文件 - 在 Windows 環境下跳過或創建空文件
                binary_files.append(file_path)
                script_content.append(f"log_warning \"跳過二進制文件: {file_path}\"")
                script_content.append(f"echo \"# Binary file: {file_path}\" > \"{file_path}\"")
                script_content.append(f"log_warning \"請手動替換二進制文件: {file_path}\"")
            else:
                # 文本文件使用 cat 和 here document
                script_content.append(f"log_info \"創建文件: {file_path}\"")
                script_content.append(f"cat > \"{file_path}\" << 'EOF'")
                script_content.append(file_info['content'])
                script_content.append("EOF")
        
        # 如果有二進制文件，顯示警告
        if binary_files:
            script_content.append("")
            script_content.append("log_warning \"以下二進制文件需要手動替換:\"")
            for bin_file in binary_files:
                script_content.append(f"log_warning \"  - {bin_file}\"")
    
    # 生成 requirements.txt (如果還沒有被包含在 all_files 中)
    if "requirements.txt" not in all_files:
        script_content.append("")
        script_content.append("log_info \"生成依賴文件...\"")
        script_content.append("cat > requirements.txt << 'EOF'")
        script_content.extend(requirements_content)
        script_content.append("EOF")
    
    # 添加安裝命令
    script_content.append("")
    script_content.append("log_info \"安裝 Python 依賴...\"")
    script_content.append("if command -v pip3 &> /dev/null; then")
    script_content.append("    pip3 install -r requirements.txt")
    script_content.append("elif command -v pip &> /dev/null; then")
    script_content.append("    pip install -r requirements.txt")
    script_content.append("else")
    script_content.append("    log_error \"未找到 pip 或 pip3，請手動安裝 Python 依賴\"")
    script_content.append("    exit 1")
    script_content.append("fi")
    
    # 部署完成
    script_content.append("")
    script_content.append("log_success \"項目部署完成！\"")
    script_content.append("log_info \"項目結構:\"")
    script_content.append("find . -type d | sort")
    script_content.append("")
    script_content.append("log_info \"重要配置文件:\"")
    script_content.append("ls -la .env .gitignore 2>/dev/null || true")
    script_content.append("")
    script_content.append("log_success \"可以開始使用項目了！\"")
    
    # 寫入文件
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(script_content))
        
        print(f"成功生成部署腳本: {output_file}")
        print(f"總共包含 {len(directories)} 個目錄, {len(init_files)} 個 __init__.py, {len(all_files)} 個文件")
        
        # 顯示包含的重要文件
        important_files = [f for f in all_files.keys() if f in ['.env', '.gitignore', 'requirements.txt']]
        if important_files:
            print("包含的重要配置文件:")
            for important_file in important_files:
                print(f"  - {important_file}")
                
    except Exception as e:
        print(f"寫入文件時出錯: {e}")

def main():
    parser = argparse.ArgumentParser(description='生成項目部署腳本')
    parser.add_argument('--directory', '-d', default='.', help='要分析的目錄路徑')
    parser.add_argument('--output', '-o', default='deploy.sh', help='輸出腳本文件名')
    parser.add_argument('--skip-binary', action='store_true', help='跳過二進制文件')
    
    args = parser.parse_args()
    
    print(f"分析目錄: {args.directory}")
    
    analyzer = StructureAnalyzer(args.directory)
    
    try:
        directories, init_files, all_files = analyzer.analyze_structure()
        requirements_content = analyzer.detect_requirements()
        
        if args.skip_binary:
            # 過濾掉二進制文件
            all_files = {k: v for k, v in all_files.items() if not v.get('binary', False)}
            print("已跳過二進制文件")
        
        generate_deploy_script(directories, init_files, all_files, requirements_content, args.output)
        
    except Exception as e:
        print(f"分析過程中出錯: {e}")
        print("請檢查目錄路徑是否正確")

if __name__ == "__main__":
    main()
