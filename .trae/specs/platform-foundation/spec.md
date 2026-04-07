# SherryAgent - Platform Foundation Spec

## Overview
- **Summary**: 定义平台底座，包括任务模型、事件模型、状态机、权限、审计、配置和存储基础。
- **Purpose**: 为后续所有运行链路提供统一对象、统一边界和统一治理口径。

## Goals
- 固定 Task / Run / Evidence / Decision / Cost Record 数据对象
- 固定统一状态机、风险分级、预算档位
- 固定配置分层与权限审计口径

## Non-Goals
- 本阶段不恢复任何运行时代码
- 不深入某条具体业务链路的实现细节

## Acceptance Criteria
- 文档中不存在“实现者自行决定”的核心对象字段
- 状态机、幂等、审计、配置分层都有明确文字约束

