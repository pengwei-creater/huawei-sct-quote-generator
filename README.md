# SCT 报价单生成器

把华为 SCT（Sales Configuration Tool）导出的 `客户化报价书_内部价格.xlsx` 自动整理成
面向客户的 Excel 报价单：**解析 BOM → 按规则归类定价 → 输出统一格式 → 校验合计**。

[![CI](https://github.com/pengwei-creater/huawei-sct-quote-generator/actions/workflows/ci.yml/badge.svg)](https://github.com/pengwei-creater/huawei-sct-quote-generator/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)

> **免责声明**：本项目是个人开源的第三方工具，与华为技术有限公司**无隶属关系**，未获其背书。
> 「华为」「SCT」「OceanStor」「FusionCube」「Atlas」等为其各自权利人的商标，此处仅作描述性使用。
> 仓库内**不含任何真实客户数据、真实价格或华为内部资料**：示例文件由脚本合成，价格纯属虚构。
> 工具输出仅做格式整理，实际报价请以 SCT 原文与正式商务流程为准。

---

## 它解决什么问题

SCT 导出的内部报价书长这样：几百行 BOM、物料编码、`partType` 标记、三行合计，
直接发给客户既不好看也泄露内部编码。手工整理一份 5 行报价单要半小时，还容易算错。

这个工具把这件事变成三条命令，并且内置了一套已经踩过坑的书写规范
（配置详情怎么分行、服务怎么打包、行高怎么算、金额格式怎么设）。

## 特性

- **结构化解析**：从 `项目配置报价` 表抽出父产品、BOM 子项、设备/服务/项目三档合计。
- **规则化生成**：模板固定表头、列宽、字体（等线）、金额格式，行高按内容自动计算，长配置不截断。
- **合计自洽**：报价单合计 = `Σ 单价×数量`，可直接与 SCT `projectTotalPrice` 对账。
- **零硬编码路径**：模板随包分发，装到哪都能跑。
- **可测试**：内置合成样例与端到端测试，CI 覆盖 Windows / Linux。

## 安装

```bash
pip install -e .
# 或直接跑源码
pip install openpyxl
```

要求 Python 3.8+ 与 `openpyxl>=3.0`。

### 作为 DeepSeek Harness 技能使用

仓库根目录的 `SKILL.md` 是技能入口。复制到技能目录即可：

| 级别 | 路径 |
|---|---|
| 用户级 | Windows `%USERPROFILE%\.agents\skills\quote-generator`；macOS/Linux `~/.agents/skills/quote-generator` |
| 项目级 | `<项目根>/.agents/skills/quote-generator` |

## 快速开始

```bash
# 0) 生成合成样例（仓库不自带真实 SCT）
python examples/make_sample.py

# 1) 解析 → JSON
quote-gen parse examples/sample_sct.xlsx -o sct.json

# 2) 照着 examples/quote_config.example.json 写你自己的配置

# 3) 生成报价单
quote-gen build examples/quote_config.example.json -o 示例报价单.xlsx

# 4) 自检（模板可读、能写文件、合计正确）
quote-gen selftest
```

`python -m quote_generator ...` 与 `quote-gen ...` 等价。

## 配置格式

```json
{
  "output": "某项目报价单20260101.xlsx",
  "rows": [
    {
      "name": "OceanStor Pacific 9520",
      "config": "本次共3节点，以下为单节点配置：\n机箱：...\nCPU：...\n硬盘：...",
      "qty": 1,
      "unit": "套",
      "price": 4629389.36,
      "note": "含软件165TiB"
    }
  ],
  "total_label": "合计",
  "declarations": ["其他声明：", "1.报价仅供参考，具体价格以下单时为准。"]
}
```

| 字段 | 必填 | 说明 |
|---|---|---|
| `output` | 是 | 输出路径（可被 `-o` 覆盖） |
| `rows[].name` | 是 | 设备名称 |
| `rows[].config` | 是 | 配置详情，`\n` 分行，一行一项 |
| `rows[].qty` / `unit` | 否 | 默认 `1` / `台` |
| `rows[].price` | 是 | 成交单价；总价列由公式 `=F*D` 生成 |
| `rows[].note` | 否 | 备注，如容量、RAID 方式 |
| `declarations` | 否 | 底部声明，缺省为「仅供参考 / 含税 / CNY」三条 |

## 规则速查

- 配置详情写法、定价与打包规则、格式规范 → [docs/rules.md](docs/rules.md)
- 各产品线（Dorado / Pacific / 5xxx / Atlas / FusionCube / OceanProtect / 数通）模板 → [docs/products.md](docs/products.md)

三条最容易踩的坑：

1. **服务默认打包进设备价**，只有无设备归属的纯服务才单列；打包不得改变合计。
2. **网口速率看光模块不看网卡**（SFP+=10G，SFP28=25G）。
3. **硬盘合并一行**，容量升序、SSD 在前 HDD 在后。

## 开发

```bash
pip install -e ".[dev]"
python -m quote_generator selftest
pytest -q
```

目录结构：

```
src/quote_generator/   解析器、生成器、CLI、模板
examples/              合成样例与其生成脚本、配置示例
docs/                  规则手册、产品模板
tests/                 端到端测试
SKILL.md               技能入口（DeepSeek Harness）
```

## 贡献

见 [CONTRIBUTING.md](CONTRIBUTING.md)。**请勿提交任何真实 SCT 文件、客户名称、真实价格或内部编码。**

## 许可

[MIT](LICENSE) © 2026 pengwei-creater
