# medical-dialog

一个可在 Claude Code 中安装复用的中文医患对话总结 Skill。它提取对话中的患者情况、医生提出的治疗策略、药物信息及注意事项，并按需读取配套的医保示例手册。

## 功能

- 忠于原始对话：未提及的诊断、药物剂量、频次和疗程不自行补全。
- 仅在对话明确涉及医保、报销等内容时读取手册并增加对应提醒。
- 资料或条件不足时保留“未提及”或“暂时无法确定”。
- 用户要求保存时，调用 Python 脚本将总结写入本地 TXT。

**配套《医疗报销手册.md》中的地区、金额和比例均为虚构演示数据，有效期字段也是教学设定（2025 年）。它用于演示条件触发、资料读取与信息核对，不代表真实医保政策。**

## 环境

- 已配置可用模型的 Claude Code。
- 导出 TXT 时需要 Python 3.8+，只使用标准库，无需安装第三方 Python 包。
- 只使用对话总结时无需运行 Python。Skill 的效果取决于模型、工具权限及实际读取的资料。

## 安装

将本仓库完整放入 Claude Code 的 `skills/medical-dialog/` 目录，确保 `SKILL.md` 直接位于该文件夹中。

Windows PowerShell（目标目录尚不存在时）：

```powershell
git clone https://github.com/HMU-ChaoWang/medical-dialog.git "$env:USERPROFILE\.claude\skills\medical-dialog"
```

macOS / Linux：

```bash
git clone https://github.com/HMU-ChaoWang/medical-dialog.git ~/.claude/skills/medical-dialog
```

也可以在 GitHub 点击 **Code → Download ZIP**，解压后将文件夹重命名为 `medical-dialog`，放入用户目录的 `.claude/skills/`。仅供当前项目使用时，放入项目的 `.claude/skills/medical-dialog/`。已有同名 Skill 时先备份自己的修改，再决定如何更新。

安装后的结构：

```text
medical-dialog/
├── SKILL.md
├── 医疗报销手册.md
├── scripts/
│   └── save_skill_output.py
├── examples/
├── README.md
└── LICENSE
```

## 使用

打开 Claude Code 的新会话，输入 `/medical-dialog`，或明确要求使用该 Skill，然后提供对话，例如：

```text
请使用 medical-dialog 总结以下模拟对话，只提取已明确提供的信息：
患者：我咳嗽三天了，晚上比较严重。
医生：先注意休息、多喝水。如果持续发热，请复诊。
```

预期包含“患者主要情况”“治疗策略”“药物信息”“注意事项”；由于原始对话未涉及医保，不读取医保手册、不主动增加医保内容。可对照 [教学输出示例](examples/summary-example.txt)。该示例为人工编写的格式参考。

医保分支的模拟输入见 [dialog-with-insurance.txt](examples/dialog-with-insurance.txt)。使用该分支时应读取手册、核对适用条件、注明具体章节，并明确输出仅适用于虚构教学场景；信息不足时不猜测。

如需保存，可以追加：

```text
请将总结保存到本机当前工作区的 outputs/medical-dialog/，完成后回读并告诉我文件位置。
```

默认输出目录相对于运行脚本时的当前工作目录。Agent 应在用户指定的工作区运行脚本，并将资源路径相对于 Skill 安装目录解析。

## 单独验证导出脚本

从仓库根目录执行：

```bash
python scripts/save_skill_output.py --input examples/summary-example.txt --output-dir outputs/demo
```

也支持 `--content "要保存的文本"` 或标准输入。没有 `--output-dir` 时默认写入当前目录的 `outputs/medical-dialog/`。每次生成独立文件，避免覆盖已有结果；成功时返回 JSON，包含 `success` 和实际绝对路径。脚本不会分析对话或请求模型 API。

## 检查建议

| 输入情境 | 应观察的行为 |
|---|---|
| 普通对话 | 只提取原文；无医保提醒 |
| 提到药物但未提供剂量 | 剂量、频次或疗程对应字段写“未提及” |
| 只问治疗费用 | 不仅凭费用问题自动触发医保分支 |
| 明确问医保但缺少地区、日期或参保信息 | 读取手册，保留待确认条件，不直接给报销承诺 |
| 要求导出 TXT | 真正运行保存脚本、检查文件并回读 |

仓库已验证导出脚本和基本 Skill 格式；对话总结及医保条件分支仍需使用者在实际 Agent 会话中检查。

## 许可与资料

自创 Skill 指令、脚本、示例与虚构手册采用 [MIT License](LICENSE)，Copyright (c) 2026 HMU-ChaoWang。可下载、修改和再分发，保留许可及版权声明。

此仓库不含真实患者对话。若自行加入第三方资料，请核对其许可并保留出处；添加的资料不自动获得本仓库的 MIT 授权。实际临床判断或医保办理应由具备权限的专业人员及当地经办机构处理。
