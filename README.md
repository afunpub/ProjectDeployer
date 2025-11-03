# ProjectDeployer
🚀 Automatically generate deployment scripts from project structure - 從項目結構自動生成部署腳本的工具
項目結構分析與部署腳本生成器
這是一個強大的 Python 工具，可以自動分析項目目錄結構並生成完整的部署腳本 (deploy.sh)，幫助您在新環境中快速重建項目。

🚀 功能特色
核心功能
自動目錄結構分析 - 掃描項目目錄，識別所有文件夾和文件

智能文件處理 - 支持文本文件和二進制文件的處理

多編碼支持 - 自動檢測文件編碼 (UTF-8, GBK, CP950, Latin-1 等)

依賴管理 - 自動檢測並生成 requirements.txt

彩色日誌輸出 - 美觀的彩色終端輸出，提升用戶體驗

配置文件支持

✅ .env - 環境變數配置文件

✅ .gitignore - Git 忽略規則文件

✅ requirements.txt - Python 依賴管理

✅ Python 包初始化 - 自動創建 __init__.py

智能過濾
自動過濾系統文件 (.DS_Store, __pycache__, .git 等)

可選跳過二進制文件以避免腳本過大

保留重要的項目配置文件

📦 安裝與使用
快速開始
```bash
# 使用完整版本
python structure_analyzer.py -d /path/to/your/project -o deploy.sh
```
```
# 使用簡化版本
python simple_generator_complete.py /path/to/your/project deploy.sh
```
完整版本參數說明
```bash
# 基本用法 - 分析當前目錄
python structure_analyzer.py

# 指定項目目錄和輸出文件
python structure_analyzer.py -d /path/to/project -o my_deploy.sh

# 跳過二進制文件（推薦）
python structure_analyzer.py -d /path/to/project -o deploy.sh --skip-binary

# 幫助信息
python structure_analyzer.py --help
```
參數說明：

-d, --directory - 要分析的項目目錄路徑（默認：當前目錄）

-o, --output - 生成的部署腳本文件名（默認：deploy.sh）

--skip-binary - 跳過二進制文件，避免部署腳本過大

簡化版本用法
```bash
# 分析當前目錄
python simple_generator_complete.py

# 指定項目目錄
python simple_generator_complete.py /path/to/project

# 指定項目目錄和輸出文件
python simple_generator_complete.py /path/to/project custom_deploy.sh
🛠️ 生成的部署腳本功能
生成的 deploy.sh 包含以下功能：
```
彩色日誌系統
```bash
log_info "信息消息"      # 藍色
log_success "成功消息"   # 綠色  
log_warning "警告消息"   # 黃色
log_error "錯誤消息"     # 紅色
```
自動化部署流程
創建目錄結構 - 重建完整的項目文件夾層級
初始化 Python 包 - 自動創建 __init__.py 文件
生成項目文件 - 還原所有源代碼和配置文件
安裝依賴 - 自動檢測並使用 pip 或 pip3
驗證部署 - 顯示最終項目結構和重要文件

錯誤處理
遇到錯誤自動退出 (set -e)
智能命令檢測（自動選擇 pip 或 pip3）
二進制文件警告和手動替換提示

📁 文件說明
主要文件
structure_analyzer.py - 完整功能版本，支持命令行參數和高級配置
simple_generator_complete.py - 簡化版本，快速易用

🎯 使用場景
適合使用完整版本
🏢 企業項目 - 需要精細控制的生產環境

🔧 複雜配置 - 包含二進制文件或特殊編碼的項目

📦 自動化流程 - 集成到 CI/CD 流水線中

適合使用簡化版本
🚀 快速原型 - 開發階段的快速部署

📚 學習項目 - 教育和小型項目

⏱️ 簡單需求 - 只需要基本功能的場景

🔧 高級用法
自定義忽略規則
修改代碼中的 ignore_dirs 和 ignore_files 來適應您的項目需求：

```python
self.ignore_dirs = {'.git', '__pycache__', '.idea', 'node_modules'}
self.ignore_files = {'.DS_Store', 'deploy.sh'}  # 只忽略真正的系統文件
```
處理二進制文件
對於包含二進制文件的項目：

```bash
# 第一次生成時跳過二進制文件
python structure_analyzer.py --skip-binary

# 然後手動替換標記的二進制文件
```
📝 輸出示例
生成過程輸出
```text
分析目錄: /path/to/project
找到 15 個目錄, 8 個 __init__.py, 47 個文件
包含的重要配置文件:
  - .env
  - .gitignore
  - requirements.txt
成功生成部署腳本: deploy.sh
```
部署腳本執行效果
```bash
$ chmod +x deploy.sh
$ ./deploy.sh
[INFO] 開始部署項目...
[INFO] 創建項目目錄結構...
[INFO] 創建 Python 包初始化文件...
[INFO] 創建項目文件...
[INFO] 生成依賴文件...
[INFO] 安裝 Python 依賴...
[SUCCESS] 項目部署完成！
[INFO] 項目結構:
.
./app
./app/api
./app/core
...
[SUCCESS] 可以開始使用項目了！
```
⚠️ 注意事項
二進制文件 - 對於二進制文件（圖片、模型等），建議使用 --skip-binary 參數，然後手動替換
文件權限 - 生成的腳本會自動設置執行權限，但在 Windows 上可能需要手動設置
編碼問題 - 如果遇到特殊編碼文件，工具會自動嘗試多種解碼方式
大文件處理 - 對於非常大的文本文件，建議手動處理以避免腳本過大

🐛 故障排除
常見問題
Q: 遇到編碼錯誤怎麼辦？
A: 工具會自動嘗試多種編碼，如果仍然失敗，會創建空文件並顯示警告。

Q: 部署腳本太大怎麼辦？
A: 使用 --skip-binary 參數跳過二進制文件，或手動處理大文本文件。

Q: 如何在 Windows 上運行？
A: 需要使用 Git Bash、WSL 或 Cygwin 等支持 bash 的環境。

Q: 依賴安裝失敗？
A: 檢查 Python 環境和網絡連接，腳本會自動檢測 pip 或 pip3。

📄 許可證
此工具為開源項目，可自由使用和修改。

開始使用：

```bash
# 嘗試分析您的第一個項目！
python structure_analyzer.py -d /path/to/your/project -o deploy.sh --skip-binary
```
