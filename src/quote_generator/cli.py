# -*- coding: utf-8 -*-
"""命令行入口：``quote-gen`` / ``python -m quote_generator``。

子命令：
    quote-gen parse    <SCT文件或目录> [-o out.json]
    quote-gen build    <config.json> [-o out.xlsx]
    quote-gen selftest
    quote-gen --version
"""
import argparse
import json
import os
import sys
import tempfile

from . import __version__
from .builder import build
from .parser import parse_file, parse_folder

DEMO_CONFIG = {
    "output": "demo.xlsx",
    "rows": [
        {
            "name": "示例存储阵列 A1",
            "config": "本次共2节点，以下为单节点配置：\n机箱：示例机箱(2U,双控,12*3.5英寸)\n"
                      "电源：2*800W 交流电源\n内存：8*32GB DDR5 5600MHz\n硬盘：8*8TB 7.2K SATA(3.5\")",
            "qty": 1,
            "unit": "套",
            "price": 105000.0,
            "note": "合成样例，仅供演示",
        }
    ],
}


def cmd_parse(args):
    if os.path.isdir(args.target):
        results = parse_folder(args.target)
    else:
        parsed = parse_file(args.target)
        results = [] if parsed is None else [parsed]

    if not results:
        print("未找到 SCT 报价书（工作表「项目配置报价」不存在）", file=sys.stderr)
        return 2

    payload = results[0] if len(results) == 1 else results
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(text)
        print("saved:", args.output)
    else:
        print(text)
    return 0


def cmd_build(args):
    with open(args.config, "r", encoding="utf-8") as fh:
        cfg = json.load(fh)
    if args.output:
        cfg["output"] = args.output
    out, total = build(cfg)
    print("OK ->", out)
    print("合计 %.2f" % total)
    return 0


def cmd_selftest(_args):
    with tempfile.TemporaryDirectory() as tmp:
        cfg = dict(DEMO_CONFIG, output=os.path.join(tmp, "demo.xlsx"))
        out, total = build(cfg)
        if not os.path.exists(out) or os.path.getsize(out) == 0:
            print("selftest 失败：输出文件为空", file=sys.stderr)
            return 1
        if abs(total - 105000.0) > 1e-6:
            print("selftest 失败：合计不对 %.2f" % total, file=sys.stderr)
            return 1
    print("selftest OK（模板可读、可写出、合计 %.2f）" % 105000.0)
    return 0


def _use_utf8_console():
    """Windows 控制台默认 cp1252，打印中文会 UnicodeEncodeError，统一改成 UTF-8。"""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):  # 老版本 Python 或被重定向的流
            pass


def main(argv=None):
    _use_utf8_console()
    parser = argparse.ArgumentParser(
        prog="quote-gen", description="华为 SCT 报价书解析与报价单生成")
    parser.add_argument("--version", action="version", version="%(prog)s " + __version__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("parse", help="解析 SCT 导出文件为 JSON")
    p.add_argument("target", help="SCT 文件或目录")
    p.add_argument("-o", "--output", help="输出 JSON 路径（默认打印到标准输出）")
    p.set_defaults(func=cmd_parse)

    b = sub.add_parser("build", help="按 JSON 配置生成报价单")
    b.add_argument("config", help="quote_config.json 路径")
    b.add_argument("-o", "--output", help="输出 xlsx 路径")
    b.set_defaults(func=cmd_build)

    st = sub.add_parser("selftest", help="自检：模板可读、能写文件、合计正确")
    st.set_defaults(func=cmd_selftest)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
