# -*- coding: utf-8 -*-
"""报价单生成器：把一份 JSON 配置写成格式统一的 Excel 报价单。

配置结构::

    {
      "output": "输出文件名.xlsx",
      "rows": [
        {
          "name": "OceanStor Pacific 9520",
          "config": "本次共3节点，以下为单节点配置：\\n机箱：...\\nCPU：...",
          "qty": 1,
          "unit": "套",
          "price": 4629389.36,
          "note": "含软件165TiB"
        }
      ],
      "total_label": "合计",
      "declarations": ["其他声明：", "1.报价仅供参考，具体价格以下单时为准。"]
    }

模板固定为包内的 ``templates/quote_template.xlsx``，表头、列宽、字体都已在模板里定义，
本模块只负责填数据、算行高、加合计与声明区。
"""
import json
import os
import shutil

from openpyxl import load_workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

HERE = os.path.dirname(os.path.abspath(__file__))

# 包内模板优先；开发态回退到仓库根目录的 templates/
_TEMPLATE_CANDIDATES = [
    os.path.join(HERE, "templates", "quote_template.xlsx"),
    os.path.join(HERE, "..", "..", "templates", "quote_template.xlsx"),
]

FONT = "等线"
MONEY_FORMAT = "0.00_);[Red](0.00)"
HEADERS = ["序号", "设备名称", "配置详情", "数量", "单位", "单价", "总价", "备注"]
DEFAULT_DECLARATIONS = [
    "其他声明：",
    "1.报价仅供参考，具体价格以下单时为准。",
    "2.本报价为含税价。",
    "3.本报价单货币币种: CNY; 货币单位: 元。",
]

__all__ = ["build", "template_path", "DEFAULT_DECLARATIONS"]


def template_path():
    """返回可用的模板路径，找不到时抛 ``FileNotFoundError``。"""
    for path in _TEMPLATE_CANDIDATES:
        if os.path.exists(path):
            return os.path.abspath(path)
    raise FileNotFoundError(
        "找不到 quote_template.xlsx，尝试过：" + "；".join(_TEMPLATE_CANDIDATES)
    )


def _visual_lines(text):
    """按列宽估算换行后的实际行数（中日韩字符按 2 个字符宽计）。"""
    total = 0
    for line in str(text).split("\n"):
        width = sum(2 if ord(ch) > 127 else 1 for ch in line)
        total += max(1, -(-width // 76))
    return total


def build(cfg, template=None):
    """按 ``cfg`` 生成报价单，返回 ``(输出路径, 合计金额)``。"""
    out = cfg["output"]
    src = template or template_path()
    shutil.copy2(src, out)

    wb = load_workbook(out)
    ws = wb[wb.sheetnames[0]]

    for merged in list(ws.merged_cells.ranges):
        ws.unmerge_cells(str(merged))

    thin = Border(
        left=Side(style="thin"),
        right=Side(style="thin"),
        top=Side(style="thin"),
        bottom=Side(style="thin"),
    )
    white = PatternFill("solid", fgColor="FFFFFFFF")
    center = Alignment(horizontal="center", vertical="center", wrap_text=True)
    vwrap = Alignment(vertical="center", wrap_text=True)
    vleft = Alignment(horizontal="left", vertical="center")

    rows = cfg["rows"]
    last_data_row = 1 + len(rows)

    # 清空模板里第 2 行起的残留
    for r in range(2, 16):
        for c in range(1, 9):
            cell = ws.cell(row=r, column=c)
            cell.value = None
            cell.border = Border()
            cell.fill = PatternFill()
            cell.font = Font(name=FONT)
            cell.number_format = "General"

    header_fill = PatternFill("solid", fgColor="FF76453B")
    header_font = Font(name=FONT, size=12, bold=True, color="FFFFFFFF")
    for i, h in enumerate(HEADERS, 1):
        cell = ws.cell(row=1, column=i, value=h)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center
        cell.border = thin
        cell.number_format = MONEY_FORMAT if i in (6, 7) else "General"

    for idx, row in enumerate(rows, 1):
        r = idx + 1
        config = row["config"]
        height = max(30, round(_visual_lines(config) * 15.75 + 6, 2))

        values = [
            idx,
            row["name"],
            config,
            row.get("qty", 1),
            row.get("unit", "台"),
            row.get("price", 0),
            "=F%d*D%d" % (r, r),
            row.get("note", ""),
        ]
        for c, v in enumerate(values, 1):
            cell = ws.cell(row=r, column=c, value=v)
            cell.font = Font(name=FONT, size=12)
            cell.fill = white
            cell.border = thin
            cell.number_format = MONEY_FORMAT if c in (6, 7) else "General"
            cell.alignment = vwrap if c in (3, 8) else center
        ws.row_dimensions[r].height = height

    # 合计行
    total_row = last_data_row + 1
    ws.merge_cells("A%d:F%d" % (total_row, total_row))
    ws["A%d" % total_row] = cfg.get("total_label", "合计")
    ws["A%d" % total_row].font = Font(name=FONT, size=12)
    ws["A%d" % total_row].alignment = Alignment(horizontal="right", vertical="center")
    ws["A%d" % total_row].border = thin
    for ci in range(2, 8):
        ws.cell(row=total_row, column=ci).border = thin
    total_cell = ws.cell(row=total_row, column=7, value="=SUM(G2:G%d)" % last_data_row)
    total_cell.font = Font(name=FONT, size=12)
    total_cell.number_format = MONEY_FORMAT
    total_cell.alignment = center
    ws.cell(row=total_row, column=8).border = thin
    ws.row_dimensions[total_row].height = 24

    # 声明区
    declarations = cfg.get("declarations") or DEFAULT_DECLARATIONS
    decl_font = Font(name=FONT, size=9, bold=True)
    for i, text in enumerate(declarations):
        rr = total_row + 1 + i
        ws.merge_cells("A%d:G%d" % (rr, rr))
        ws["A%d" % rr] = text
        ws["A%d" % rr].font = decl_font
        ws["A%d" % rr].alignment = vleft

    # 删掉声明区之后模板残留的空行
    decl_end = total_row + len(declarations)
    if ws.max_row > decl_end:
        ws.delete_rows(decl_end + 1, ws.max_row - decl_end)

    wb.save(out)

    total = sum((row.get("price", 0) or 0) * (row.get("qty", 1) or 1) for row in rows)
    return out, total


def build_from_file(cfg_path, output=None):
    """从 JSON 文件生成报价单；``output`` 优先于配置里的 ``output``。"""
    with open(cfg_path, "r", encoding="utf-8") as fh:
        cfg = json.load(fh)
    if output:
        cfg["output"] = output
    return build(cfg)
