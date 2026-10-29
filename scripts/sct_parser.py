# -*- coding: utf-8 -*-
"""兼容旧用法的包装脚本：``python scripts/sct_parser.py <SCT文件或目录> [-o out.json]``。

逻辑全在 ``src/quote_generator/parser.py``，这里只是把 ``src`` 加进 ``sys.path``，
让不安装包、直接 clone 仓库的人也能跑。
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))

from quote_generator.parser import parse_file, parse_folder  # noqa: E402


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    target = sys.argv[1]
    out = sys.argv[sys.argv.index("-o") + 1] if "-o" in sys.argv else None

    results = parse_folder(target) if os.path.isdir(target) else [parse_file(target)]
    results = [r for r in results if r]
    if not results:
        print("未找到 SCT 报价书（需包含工作表：项目配置报价）")
        sys.exit(2)

    payload = results[0] if len(results) == 1 else results
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    if out:
        with open(out, "w", encoding="utf-8") as fh:
            fh.write(text)
        print("saved:", out)
    else:
        print(text)


if __name__ == "__main__":
    main()
