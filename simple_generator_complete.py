# simple_generator_complete.py
import os
import sys
from pathlib import Path

def generate_complete_deploy_sh(project_path=".", output_file="deploy.sh"):
    """生成完整部署腳本（包含所有文件）"""
    
    project_path = Path(project_path)
    
    # 掃描目錄結構和文件
    dirs_to_create = set()
    init_dirs = set()
    files_to_create = {}
    
    # 總是包含根目錄
    dirs_to_create.add(".")
    
    for root, dirs, files in os.walk(project_path):
        # 過濾系統目錄
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'venv', 'env']]
        
        current_path = Path(root)
        
        for dir_name in dirs:
            full_path = current_path / dir_name
            try:
                rel_path = str(full_path.relative_to(project_path))
                dirs_to_create.add(rel_path)
            except ValueError:
                continue
            
        # 檢查 __init__.py 來確定 Python 包
        if "__init__.py" in files:
            try:
                rel_path = str(current_path.relative_to(project_path))
                if rel_path != ".":
                    init_dirs.add(rel_path)
            except ValueError:
                continue
        
        # 讀取所有文件內容（不再忽略 .env 和 .gitignore）
        for file in files:
            if file in ['.DS_Store', 'deploy.sh']:  # 只忽略系統文件和部署腳本本身
                continue
                
            file_path = current_path / file
            try:
                rel_path = str(file_path.relative_to(project_path))
                
                # 讀取文件內容
                try:
                    # 嘗試多種編碼
                    encodings = ['utf-8', 'gbk', 'cp950', 'latin-1']
                    content = None
                    for encoding in encodings:
                        try:
                            with open(file_path, 'r', encoding=encoding) as f:
                                content = f.read()
                            break
                        except UnicodeDecodeError:
                            continue
                    
                    if content is None:
                        # 如果是二進制文件，創建佔位符
                        content = f"# Binary file: {file}\n# This is a binary file that cannot be included in the deploy script.\n# Please replace this file manually after deployment."
                    
                    files_to_create[rel_path] = content
                    
                except Exception as e:
                    print(f"讀取文件 {file_path} 時出錯: {e}")
                    files_to_create[rel_path] = f"# Error reading file: {e}"
                    
            except Exception as e:
                print(f"處理文件 {file_path} 時出錯: {e}")
    
    # 生成 deploy.sh 內容
    script = [
        "#!/bin/bash",
        "",
        "# 自動生成的部署腳本",
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
    
    # 添加目錄創建命令
    script.append("log_info \"創建項目目錄結構...\"")
    for directory in sorted(dirs_to_create):
        if directory != ".":
            script.append(f"mkdir -p \"{directory}\"")
    
    # 添加 __init__.py 文件
    if init_dirs:
        script.append("")
        script.append("log_info \"創建 Python 包初始化文件...\"")
        for init_dir in sorted(init_dirs):
            script.append(f"touch \"{init_dir}/__init__.py\"")
    
    # 添加所有其他文件
    if files_to_create:
        script.append("")
        script.append("log_info \"創建項目文件...\"")
        
        for file_path, content in sorted(files_to_create.items()):
            script.append("")
            script.append(f"log_info \"創建文件: {file_path}\"")
            script.append(f"cat > \"{file_path}\" << 'EOF'")
            script.append(content)
            script.append("EOF")
    
    # 添加安裝命令
    script.append("")
    script.append("log_info \"安裝 Python 依賴...\"")
    script.append("if command -v pip3 &> /dev/null; then")
    script.append("    pip3 install -r requirements.txt")
    script.append("elif command -v pip &> /dev/null; then")
    script.append("    pip install -r requirements.txt")
    script.append("else")
    script.append("    log_error \"未找到 pip 或 pip3，請手動安裝 Python 依賴\"")
    script.append("fi")
    
    # 部署完成
    script.append("")
    script.append("log_success \"項目部署完成！\"")
    script.append("log_info \"最終項目結構:\"")
    script.append("find . -type d | sort")
    script.append("")
    script.append("log_info \"重要配置文件:\"")
    script.append("ls -la .env .gitignore requirements.txt 2>/dev/null || true")
    
    # 寫入文件
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("\n".join(script))
        print(f"成功生成: {output_file}")
        print(f"包含 {len(dirs_to_create)} 個目錄, {len(init_dirs)} 個 __init__.py, {len(files_to_create)} 個文件")
        
        # 顯示重要文件
        important_files = [f for f in files_to_create.keys() if f in ['.env', '.gitignore', 'requirements.txt']]
        if important_files:
            print("包含的重要配置文件:")
            for important_file in important_files:
                print(f"  - {important_file}")
                
    except Exception as e:
        print(f"寫入文件失敗: {e}")

if __name__ == "__main__":
    project_path = sys.argv[1] if len(sys.argv) > 1 else "."
    output_file = sys.argv[2] if len(sys.argv) > 2 else "deploy.sh"
    
    generate_complete_deploy_sh(project_path, output_file)
