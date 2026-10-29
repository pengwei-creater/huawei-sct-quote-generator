# Changelog

格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [1.0.0] - 2026-10-29

首个公开版本。

### Added

- SCT 解析器：从 `项目配置报价` 表抽出父产品、BOM 子项与设备/服务/项目三档合计。
- 报价单生成器：固定表头、列宽、等线字体、金额格式，行高按内容自动计算（长配置不截断）。
- CLI：`quote-gen parse|build|selftest`，同时支持 `python -m quote_generator`。
- 兼容包装脚本 `scripts/sct_parser.py`、`scripts/quote.py`（免安装直接跑）。
- 规则手册与各产品线配置模板（Dorado / Pacific / 5xxx / Atlas / FusionCube / OceanProtect / 数通）。
- 合成样例生成脚本与端到端测试，CI 覆盖 Windows 与 Linux。
- `SKILL.md` 技能入口，可在 DeepSeek Harness 中直接使用。
