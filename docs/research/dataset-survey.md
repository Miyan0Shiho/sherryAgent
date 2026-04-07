---
title: "主流开源 Agent 评估数据集调研"
status: approved
created: 2026-04-06
updated: 2026-04-06
author: "sherry-agent-team"
related: ["mvp-5-skill-ecosystem.md"]
---

# 主流开源 Agent 评估数据集调研

## 摘要

本文调研了当前主流的开源 Agent 评估数据集，包括 AgentBench、GAIA、ToolBench、WebArena 等，对比分析了各数据集的特点、难度分布、许可证、获取难度。针对 SherryAgent 的特性，推荐优先采用 GAIA 和 ToolBench 两个数据集。

## 数据集对比

| 数据集 | 特点 | 难度分布 | 许可证 | 获取难度 | 环境配置复杂度 | 适用场景 |
|--------|------|----------|--------|----------|----------------|----------|
| **AgentBench** | 综合基准，8 个环境（网页浏览、数学解题、具身决策等） | 中高 | MIT | 中 | 高（需要 Docker、任务服务器） | 通用 Agent 能力评估 |
| **GAIA** | 人类设计的 466 个问题，涵盖日常任务、科学、常识 | 从简单到困难 | Apache 2.0 | 低 | 低 | 通用 AI 助手评估 |
| **ToolBench** | 专注工具调用，1.6 万+ 真实 API | 中 | Apache 2.0 | 中 | 中 | 工具学习和调用能力 |
| **WebArena** | 专注网页导航任务 | 中 | MIT | 中 | 高 | Web Agent 评估 |

## 各数据集详细分析

### 1. AgentBench

**简介：** 由清华大学等机构联合推出的综合性 Agent 评估基准。

**特点：**
- 包含 8 个环境（5 个首创，3 个基于已有数据集）
- 覆盖网页浏览、数学解题、具身决策、操作系统操作等场景
- 测试推理、决策、工具使用等综合能力

**获取难度：** 中等
**环境配置复杂度：** 高（需要 Docker 镜像、任务服务器、任务分配器）
**GitHub：** https://github.com/THUDM/AgentBench

### 2. GAIA (General AI Assistants Benchmark)

**简介：** 由 Meta、HuggingFace、AutoGPT 联合推出的通用 AI 助手基准。

**特点：**
- 466 个人类设计和注释的问题
- 有时附带文件（图像、电子表格等）
- 涵盖日常个人任务、科学和常识
- 测试自主规划、多步骤推理、工具调用、上下文记忆、多模态处理

**获取难度：** 低（可直接通过 Hugging Face 下载）
**环境配置复杂度：** 低（不需要复杂环境）
**Hugging Face：** https://huggingface.co/datasets/gaia-benchmark/GAIA

**难度分布：**
- Level 1（简单）：单步推理，无需工具
- Level 2（中等）：多步推理，可能需要工具
- Level 3（困难）：复杂多步推理，需要多工具协作

### 3. ToolBench

**简介：** 由清华大学等机构推出的工具学习基准。

**特点：**
- 1.6 万+ 真实世界 API
- 支持单一工具和多工具配置
- 提供训练和评估脚本
- 包含微调模型 ToolLLaMA

**获取难度：** 中等
**环境配置复杂度：** 中等
**GitHub：** https://github.com/OpenBMB/ToolBench

### 4. WebArena

**简介：** 专注于网页导航和操作的 Agent 基准。

**特点：**
- 覆盖不同领域的通用网页导航
- 测试 Agent 在多种操作和环境下的泛化能力
- 需要模拟真实 Web 环境

**获取难度：** 中等
**环境配置复杂度：** 高

## 推荐方案

### 优先推荐：GAIA + ToolBench

#### 1. GAIA 优先采用理由：

✅ **获取难度低**：通过 Hugging Face 即可获取，无需复杂环境配置  
✅ **适用性广**：涵盖 SherryAgent 的所有核心能力（规划、推理、工具调用、记忆）  
✅ **难度分层**：从简单到困难，适合不同阶段的评估  
✅ **社区活跃**：有公开的排行榜，便于对比  
✅ **许可证友好**：Apache 2.0，可自由使用

#### 2. ToolBench 补充采用理由：

✅ **专注工具调用**：完美匹配 SherryAgent 的 Skill 插件系统  
✅ **API 丰富**：1.6 万+ 真实 API，覆盖各种场景  
✅ **提供脚本**：有现成的训练和评估脚本  
✅ **开源友好**：Apache 2.0 许可证

### 实施建议

1. **第一阶段：GAIA 基础评估**
   - 使用 GAIA Level 1-2 任务进行基础能力验证
   - 测试 Agent 的规划、推理、基础工具调用能力
   - 实现自动化评估脚本

2. **第二阶段：ToolBench 工具能力深度评估**
   - 使用 ToolBench 测试多工具协作能力
   - 验证 SherryAgent 的 Skill 插件系统
   - 对比工具调用效率和准确性

3. **长期：选择性集成 AgentBench/WebArena**
   - 如需更全面的评估，可考虑集成 AgentBench
   - 如需 Web 导航能力测试，可考虑 WebArena

## 参考链接

- AgentBench: https://github.com/THUDM/AgentBench
- GAIA: https://huggingface.co/datasets/gaia-benchmark/GAIA
- ToolBench: https://github.com/OpenBMB/ToolBench
