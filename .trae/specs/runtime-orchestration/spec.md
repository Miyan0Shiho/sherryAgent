# SherryAgent - Runtime Orchestration Spec

## Overview
- **Summary**: 定义 Planner、Execution Engine、Scheduler 与四条主链路的运行时组织方式。
- **Purpose**: 把交互式、后台、批量、发布治理四类工作负载统一到同一执行框架下。

## Goals
- 固定 4 条主链路的输入/输出契约
- 固定 mode、planner、executor、scheduler 的职责边界
- 固定超时、取消、重试、确认流的处理原则

## Non-Goals
- 不设计具体工具 API 细节

## Acceptance Criteria
- 4 条主链路都有明确流程、目标和降级策略
- Planner / Execution / Scheduler 边界没有重叠歧义

