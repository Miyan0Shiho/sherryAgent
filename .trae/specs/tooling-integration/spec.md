# SherryAgent - Tooling Integration Spec

## Overview
- **Summary**: 定义工具协议、MCP/CLI/API 接入、隔离、重试、幂等和外部依赖治理。
- **Purpose**: 保证工具使用既可扩展又可审计，不因集成复杂度破坏平台稳定性。

## Goals
- 固定工具调用最小契约
- 固定本地工具、远程工具、外部 API 的接入边界
- 固定幂等、超时、重试、隔离的治理要求

## Non-Goals
- 不编写具体工具实现

## Acceptance Criteria
- 工具接入和执行风险有统一口径
- MCP/CLI/API 接入方式不会把策略和执行混杂

