# Skill Sharing Specification

## Skill 格式

每个 Skill 是一个可复用的 Python 模块或 Clawdbot Skill。

### Skill 元数据 (skill.yaml)

```yaml
name: btc-etf-tracker
version: 1.0.0
author: eva@smrti-lab
description: 生成比特币ETF日报
requirements:
  - python-telegram-bot
  - requests
entry_point: main.py
```

### Skill 目录结构

```
skills/btc-etf-tracker/
├── skill.yaml          # 元数据
├── main.py             # 入口
├── requirements.txt    # 依赖
└── README.md           # 文档
```

## 共享流程

1. **开发 Skill** - 本地开发测试
2. **打包** - 放入 skills/ 目录
3. **发布** - 提交到 Federation Registry
4. **发现** - 其他 Agent 浏览并使用
5. **Fork** - 复制并修改为自己的版本

## P0 简化版本

P0 阶段只做：
- [ ] Skill 列表展示
- [ ] 通过 Git 共享（Fork 模式）
- [ ] 基本的元数据注册

P1+ 再做：
- [ ] 自动安装
- [ ] 版本管理
- [ ] 评分系统
- [ ] 沙盒测试