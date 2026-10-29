# -*- coding: utf-8 -*-
"""兼容旧用法的包装脚本：``python scripts/quote.py <config.json> [-o out.xlsx]``。

逻辑全在 ``src/quote_generator/builder.py``。
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))

from quote_generator.builder import build_from_file  # noqa: E402


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cfg_path = sys.argv[1]
    out = sys.argv[sys.argv.index("-o") + 1] if "-o" in sys.argv else None
    target, total = build_from_file(cfg_path, out)
    print("OK ->", target)
    print("合计 %.2f" % total)


if __name__ == "__main__":
    main()
