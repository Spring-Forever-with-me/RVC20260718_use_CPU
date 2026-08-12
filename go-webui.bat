@echo off
chcp 65001 >nul
set "SCRIPT_DIR=%~dp0"
set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"
cd /d "%SCRIPT_DIR%"
set "PATH=%SCRIPT_DIR%\runtime;%PATH%"
set "GRADIO_ANALYTICS_ENABLED=False"
set "NO_PROXY=localhost,127.0.0.1,::1,%NO_PROXY%"

:: ========== CPU推理模式配置 ==========
:: 全局强制Python使用UTF-8编码
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8

:: 强制关闭CUDA Graph（CPU模式不需要）
set RVC_CUDA_GRAPH=0

:: CPU推理性能优化
:: 设置OpenMP线程数（根据你的CPU核心数调整，一般设为物理核心数）
set OMP_NUM_THREADS=12
set MKL_NUM_THREADS=12
set OPENBLAS_NUM_THREADS=12
set VECLIB_MAXIMUM_THREADS=12
set NUMEXPR_NUM_THREADS=12

:: 禁用DML，强制使用CPU
set DIRECTML_DISABLE=1
echo "当前模式 | CPU推理"
start /affinity FFF runtime\python.exe -I webui.py --pycmd runtime\python.exe --port 7897
