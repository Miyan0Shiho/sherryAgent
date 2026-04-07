# 天气查询
version: 1.0.0
description: 查询指定城市的天气信息

## Dependencies
- requests

## Triggers
- keyword: "天气"
- keyword: "temperature"

## Entry Point
weather_tool.py:WeatherTool

## Environment Variables
API_KEY=your_api_key
