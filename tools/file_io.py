import os

def read_text(path, errors="strict", newline=None):
    """
    安全读取文本文件，自动检测编码（优先 UTF-8），并提供宽松 fallback。
    """
    # 优先尝试的编码列表（按推荐顺序）
    encodings_to_try = [
        "utf-8-sig",               # 处理 UTF-8 with BOM
        "utf-8",                   # 标准 UTF-8
        None,                      # 系统默认（Windows 常为 GBK，Linux 常为 UTF-8）
        "gbk",                     # 常见中文编码
        "gb2312",                  # 兼容 GBK
    ]
    # 去重，避免重复尝试
    seen = set()
    unique_encodings = []
    for enc in encodings_to_try:
        if enc not in seen:
            seen.add(enc)
            unique_encodings.append(enc)

    last_error = None
    for encoding in unique_encodings:
        try:
            kwargs = {"errors": "strict", "newline": newline}
            if encoding is not None:
                kwargs["encoding"] = encoding
            with open(path, "r", **kwargs) as f:
                return f.read()
        except UnicodeDecodeError as e:
            last_error = e
            # 可选：打印调试信息
            # print(f"尝试编码 {encoding or '系统默认'} 失败: {e}")
            continue

    # 所有严格尝试都失败，若 errors 不是 'strict'，则用宽容模式再试一次
    if errors != "strict":
        # 使用最后一种编码（gbk 或系统默认）并应用 errors 模式
        fallback_encoding = "gbk"  # 或系统默认，但这里用 gbk 更常见
        try:
            with open(path, "r", encoding=fallback_encoding, errors=errors, newline=newline) as f:
                return f.read()
        except UnicodeDecodeError as e:
            last_error = e

    # 如果仍然失败，或 errors 为 strict，抛出异常
    raise last_error or UnicodeDecodeError("无法解码文件，尝试所有常见编码均失败")