import os
import tempfile
import toml
from sherry_agent.infrastructure.security.user_rules import UserConfigRules
from sherry_agent.infrastructure.security.base import PermissionRequest, RiskLevel


def test_user_config_rules_with_deny_list():
    """测试用户配置规则的拒绝列表功能"""
    # 创建临时配置文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.toml', delete=False) as f:
        config = {
            'permissions': {
                'deny_list': {
                    'commands': ['rm -rf *', 'sudo *'],
                    'paths': ['/etc/*', '~/.ssh/*']
                }
            }
        }
        toml.dump(config, f)
        config_path = f.name
    
    try:
        # 初始化用户配置规则检查器
        checker = UserConfigRules(config_path=config_path)
        
        # 测试拒绝的命令
        request1 = PermissionRequest(
            tool_name='shell',
            operation='rm -rf /tmp/*',
            risk_level=RiskLevel.HIGH
        )
        result1 = checker.check(request1)
        assert result1.decision.value == 'deny'
        assert '用户配置规则拒绝' in result1.reason
        
        # 测试拒绝的路径
        request2 = PermissionRequest(
            tool_name='file',
            operation='read',
            target_path='/etc/passwd',
            risk_level=RiskLevel.MEDIUM
        )
        result2 = checker.check(request2)
        assert result2.decision.value == 'deny'
        assert '用户配置规则拒绝' in result2.reason
        
        # 测试允许的操作
        request3 = PermissionRequest(
            tool_name='shell',
            operation='ls -la',
            risk_level=RiskLevel.LOW
        )
        result3 = checker.check(request3)
        assert result3.decision.value == 'allow'
        
    finally:
        # 清理临时文件
        if os.path.exists(config_path):
            os.unlink(config_path)


def test_user_config_rules_with_allow_list():
    """测试用户配置规则的允许列表功能"""
    # 创建临时配置文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.toml', delete=False) as f:
        config = {
            'permissions': {
                'allow_list': {
                    'commands': ['git *', 'npm *'],
                    'paths': ['~/projects/*', '/tmp/*']
                }
            }
        }
        toml.dump(config, f)
        config_path = f.name
    
    try:
        # 初始化用户配置规则检查器
        checker = UserConfigRules(config_path=config_path)
        
        # 测试允许的命令
        request1 = PermissionRequest(
            tool_name='shell',
            operation='git status',
            risk_level=RiskLevel.LOW
        )
        result1 = checker.check(request1)
        assert result1.decision.value == 'allow'
        assert '用户配置规则允许' in result1.reason
        
        # 测试允许的路径
        request2 = PermissionRequest(
            tool_name='file',
            operation='write',
            target_path='/tmp/test.txt',
            risk_level=RiskLevel.MEDIUM
        )
        result2 = checker.check(request2)
        assert result2.decision.value == 'allow'
        assert '用户配置规则允许' in result2.reason
        
    finally:
        # 清理临时文件
        if os.path.exists(config_path):
            os.unlink(config_path)


def test_user_config_rules_no_config():
    """测试无配置文件的情况"""
    # 使用不存在的配置文件路径
    checker = UserConfigRules(config_path='/nonexistent/path/config.toml')
    
    # 测试操作
    request = PermissionRequest(
        tool_name='shell',
        operation='ls -la',
        risk_level=RiskLevel.LOW
    )
    result = checker.check(request)
    assert result.decision.value == 'allow'
    assert '无用户配置规则匹配，继续检查' in result.reason
