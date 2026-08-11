# AGENTS.md

本文件为本仓库的 Agent 协作约定。请优先使用中文与用户沟通。

## 仓库约定

- 这是 `drawio-skill` Agent Skill 仓库，核心内容位于 `skills/drawio-skill/`。
- `skills/drawio-skill/SKILL.md` 是技能主入口；修改能力、流程、约束或依赖前，先阅读并保持文档一致。
- 脚本按能力拆分在 `skills/drawio-skill/scripts/`，对应说明在 `references/`、`README.md` 和 `README_CN.md`。
- 回归测试位于仓库根目录 `tests/`，只使用标准库 `unittest`，不引入 pip 依赖；测试不会随 Skill 包发布。
- 运行完整测试：

```bash
rtk python3 -W error::ResourceWarning -m unittest discover -s tests -v
```

- 修改 Python 脚本时保持标准库优先；确需第三方依赖时，应遵循脚本现有约定并同步文档。
- 修改 `skills/drawio-skill/` 下内容时，注意 `sync-365-skills` 工作流会把该目录同步到 `Agents365-ai/365-skills`，不要写入只适用于本仓库根目录的内容。
- 涉及调用 draw.io CLI 的流程，必须遵守 `SKILL.md` 中的沙箱外执行规则，并在每次调用前申请提权。
- 除非用户明确要求，否则更新 AGENTS、Skill 或其他文档时不要滚动版本号，也不要同步修改 `CHANGELOG.md`、marketplace 等版本相关文件。

## 工作方式

- 先阅读相关文档和现有实现，再按仓库既有模式修改。
- 改动保持聚焦，不顺手重构无关代码。
- 不覆盖用户已有的未提交修改。
- 对本项目进行优化时，禁止硬编码架构，禁止耦合参考资料的实际内容，禁止写入参考图的内容文本。
- 完成修改后运行受影响测试，并在交付时说明验证结果。
