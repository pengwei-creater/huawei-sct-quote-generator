---
name: quote-generator
description: 根据华为SCT导出文件自动生成报价单。支持IT存储/OceanStor、超融合FusionCube、AI服务器Atlas、数通网络设备等产品的报价单生成。从SCT解析产品信息、BOM配置、价格，输出格式化报价单。
---

# SCT 报价单生成器（技能入口）

> 仓库结构：
> - `src/quote_generator/` — 解析器（SCT→JSON）、生成器（JSON→xlsx）、CLI
> - `src/quote_generator/templates/quote_template.xlsx` — 报价单模板（勿改）
> - `scripts/sct_parser.py`、`scripts/quote.py` — 免安装包装脚本
> - `docs/rules.md` — 规则手册；`docs/products.md` — 各产品线模板
> - `examples/make_sample.py` — 合成样例生成脚本（仓库不含任何真实 SCT）
>
> 环境：Python 3.8+ 与 `openpyxl`。

## 零、工作流（脚本优先）

```bash
pip install openpyxl

# 1) 解析 SCT -> JSON
python scripts/sct_parser.py "<SCT文件或目录>" -o sct.json

# 2) 按规则整理报价行，写入 quote_config.json（结构见 examples/quote_config.example.json）

# 3) 生成报价单
python scripts/quote.py quote_config.json -o "<输出目录>/<产品名>报价单<YYYYMMDD>.xlsx"

# 4) 校验：脚本打印的合计 必须等于 SCT 的 projectTotalPrice
```

- 不要手写 xlsx 样式，一律走生成器，保证格式一致。
- `rows[].config` 用 `\n` 分行，一行一个配置项；多个产品 = 多个 row；合计由脚本自动生成。

## 一、SCT 文件结构

工作表：`封面`、`免责声明`、`项目配置报价`（只有最后一张含数据）。

| 列 | 含义 |
|---|---|
| A | 标记：`partType.1`=硬件、`partType.0`=服务/软件、`partnumber.*`=物料码、`*TotalPrice`=合计行 |
| C | 序号（非空即父产品） |
| D | 描述 |
| E | 总数 |
| F | 成交单价 |
| G | 成交总价 |

## 二、定价规则

- 设备单价取父产品 F 列，总价取 G 列。
- **随设备服务默认打包**（工程应用支持、安装、规划设计与实施、灾备场景化实施、SSD 寿命保障）：
  `设备单价 = SCT设备单价 + (Σ归属服务金额 / 设备数量)`，不单独列行。
- 只有无设备归属的纯服务（业务迁移、独立运维）才单列。
- 打包/拆分**不得改变合计**，合计必须等于 `projectTotalPrice`。
- 实施服务单列：仅在用户明确要求时使用，价格取该父产品成交价。

## 三、书写规范（要点）

- 每项一行，行首不留空格；CPU、缓存、网口从机箱剥离。
- 硬盘合并一行：容量升序、SSD 在前 HDD 在后、`、` 分隔。
- 数量写在型号前（`8*1Gb ETH`）。
- 网口速率依光模块判定：SFP+=10G，SFP28=25G。
- 电源用「功率+类型」，不写物料编码；禁止内部代号与处理痕迹。
- 软件写许可名称与 CPU 数；服务与维保合并成一行。
- 字体等线、金额 `0.00_);[Red](0.00)`、其余「常规」，行高由脚本按内容计算。

完整规则见 [docs/rules.md](docs/rules.md)，产品模板见 [docs/products.md](docs/products.md)。

## 四、交付前自检

1. 合计 == SCT `projectTotalPrice`（脚本已打印）。
2. 每个产品独立成行，服务归属正确（无重复计价、无遗漏）。
3. 配置详情无截断：打开生成的 xlsx 检查长行是否换行完整。
4. 文件名 `{产品名}报价单{YYYYMMDD}.xlsx`，输出到 SCT 同目录或用户指定目录。
5. 备注写在备注列，不放内部说明。
