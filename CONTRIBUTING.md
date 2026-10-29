# 贡献指南

感谢愿意一起改进这个工具。下面几件事请先看一眼。

## 绝对不能提交的内容

- **真实 SCT 导出文件**（`*客户化报价书_内部价格.xlsx`）以及任何客户名称、项目名、客户编码。
- **真实成交价、折扣、成本**，包括截图和 PDF。
- 华为内部系统地址、账号、内部物料编码表。

需要举例时，用 `examples/make_sample.py` 生成合成数据，或自己编一套明显虚构的数据。

## 开发环境

```bash
git clone https://github.com/pengwei-creater/huawei-sct-quote-generator.git
cd huawei-sct-quote-generator
python -m venv .venv
# Windows: .venv\Scripts\activate ；macOS/Linux: source .venv/bin/activate
pip install -e ".[dev]"
```

## 提交前自检

```bash
python -m quote_generator selftest
pytest -q
```

两条都要通过。若改了模板或生成逻辑，请附一个「改动前后」的 xlsx 截图差异说明。

## 代码约定

- 只依赖标准库 + `openpyxl`，不引入重量级依赖。
- 路径一律相对定位，不写死 `C:\`、`D:\` 或用户名。
- 中文注释与文档用「，」「。」全角标点；代码标识符用英文。
- 新增产品模板写进 `docs/products.md`，并在 `docs/rules.md` 补对应归类规则。

## 提交信息

用一句话说清改了什么，例如：

```
fix: 长配置行行高少算一行导致截断
docs: 补充 OceanProtect 模板
feat: 支持统一倍率定价
```

## 提 PR

1. Fork 并新建分支（`fix/...`、`feat/...`）。
2. 一个 PR 只做一件事，别混格式化与功能改动。
3. 描述里写清：动机、改法、验证方式（命令与结果）。
