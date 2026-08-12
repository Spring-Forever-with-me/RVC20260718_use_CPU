import os
import sys
import subprocess
import os
os.environ['PYTHONUTF8'] = '1'
os.environ['LANG'] = 'en_US.UTF-8'
os.system("chcp 65001")
# 1. 获取脚本所在目录（假设本 Python 脚本与批处理在同一位置，或者您可手动指定）
script_dir = os.path.dirname(os.path.abspath(__file__))

# 2. 切换到该目录（等同于 cd /d）
os.chdir(script_dir)
print(f"[DEBUG] 当前工作目录: {os.getcwd()}")

# 3. 准备环境变量
env = os.environ.copy()

# 添加 runtime 到 PATH 开头
runtime_path = os.path.join(script_dir, 'runtime')
env['PATH'] = runtime_path + os.pathsep + env.get('PATH', '')
print(f"[DEBUG] PATH = {env['PATH']}")

# 设置 GRADIO_ANALYTICS_ENABLED
env['GRADIO_ANALYTICS_ENABLED'] = 'False'
print(f"[DEBUG] GRADIO_ANALYTICS_ENABLED = {env['GRADIO_ANALYTICS_ENABLED']}")

# 设置 NO_PROXY
old_no_proxy = env.get('NO_PROXY', '')
env['NO_PROXY'] = f'localhost,127.0.0.1,::1,{old_no_proxy}' if old_no_proxy else 'localhost,127.0.0.1,::1'
print(f"[DEBUG] NO_PROXY = {env['NO_PROXY']}")

# 4. 构造要执行的命令
python_exe = os.path.join(runtime_path, 'python.exe')
cmd = [
    python_exe,
    '-I',
    'webui.py',
    '--pycmd', 'runtime\\python.exe',   # 注意路径风格（反斜杠可保留）
    '--port', '7897',
    '--dml'
]
print(f"[DEBUG] 即将执行: {' '.join(cmd)}")

# 5. 方式一（推荐）：使用 subprocess.run，可以传递自定义环境
print("[DEBUG] 使用 subprocess.run 启动...")
result = subprocess.run(cmd, env=env)  # 您也可以添加 capture_output=True 来捕获输出

# 6. 方式二（如果您坚持要用 os.system）：先注入环境变量到 os.environ，然后调用
# 注意：这种方式会修改当前 Python 进程的环境，且无法捕获子进程输出
# 如果需要，可以取消注释以下代码：
# os.environ.update(env)   # 但 env 已包含所有原有环境，可直接赋值给 os.environ
# os.system(' '.join(cmd))   # 但命令可能含有空格，建议用 subprocess 更安全

# 最后，如需暂停（模拟 pause）
input("按任意键退出...")