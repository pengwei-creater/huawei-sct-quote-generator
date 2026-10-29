# -*- coding: utf-8 -*-
"""华为 SCT 报价书 → 客户报价单。

模块划分：
- :mod:`quote_generator.parser` 解析 SCT 导出的 ``客户化报价书_内部价格.xlsx``
- :mod:`quote_generator.builder` 按模板生成报价单 ``.xlsx``
"""

__version__ = "1.0.0"

from .builder import build  # noqa: F401
from .parser import parse_file, parse_folder  # noqa: F401

__all__ = ["build", "parse_file", "parse_folder", "__version__"]
