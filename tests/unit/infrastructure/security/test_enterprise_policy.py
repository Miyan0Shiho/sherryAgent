import os
import tempfile
import toml
from sherry_agent.infrastructure.security.enterprise_policy import EnterprisePolicy
from sherry_agent.infrastructure.security.base import PermissionRequest, RiskLevel


def test_enterprise_policy_with_deny_list():
    """测试企业策略的拒绝列表功能"""
    # 创建临时策略文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.toml', delete=False) as f:
        policy = {
            'enterprise_policy': {
                'global': {
                    'enforce': True
                },
                'deny_list': {
                    'commands': ['rm -rf *', 'sudo *'],
                    'paths': ['/etc/*', '~/.ssh/*'],
                    'operations': ['delete', 'format']
                }
            }
        }
        toml.dump(policy, f)
        policy_path = f.name
    
    try:
        # 初始化企业策略检查器
        checker = EnterprisePolicy(policy_path=policy_path)
        
        # 测试拒绝的命令
        request1 = PermissionRequest(
            tool_name='shell',
            operation='rm -rf /tmp/*',
            risk_level=RiskLevel.HIGH
        )
        result1 = checker.check(request1)
        assert result1.decision.value == 'deny'
        assert '企业策略拒绝' in result1.reason
        
        # 测试拒绝的路径
        request2 = PermissionRequest(
            tool_name='file',
            operation='read',
            target_path='/etc/passwd',
            risk_level=RiskLevel.MEDIUM
        )
        result2 = checker.check(request2)
        assert result2.decision.value == 'deny'
        assert '企业策略拒绝' in result2.reason
        
        # 测试拒绝的操作类型
        request3 = PermissionRequest(
            tool_name='file',
            operation='delete',
            target_path='/tmp/test.txt',
            risk_level=RiskLevel.MEDIUM
        )
        result3 = checker.check(request3)
        assert result3.decision.value == 'deny'
        assert '企业策略拒绝' in result3.reason
        
        # 测试允许的操作
        request4 = PermissionRequest(
            tool_name='shell',
            operation='ls -la',
            risk_level=RiskLevel.LOW
        )
        result4 = checker.check(request4)
        assert result4.decision.value == 'allow'
        
    finally:
        # 清理临时文件
        if os.path.exists(policy_path):
            os.unlink(policy_path)


def test_enterprise_policy_with_allow_list():
    """测试企业策略的允许列表功能"""
    # 创建临时策略文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.toml', delete=False) as f:
        policy = {
            'enterprise_policy': {
                'global': {
                    'enforce': True
                },
                'allow_list': {
                    'commands': ['git *', 'npm *'],
                    'paths': ['~/projects/*', '/tmp/*'],
                    'operations': ['read', 'write']
                }
            }
        }
        toml.dump(policy, f)
        policy_path = f.name
    
    try:
        # 初始化企业策略检查器
        checker = EnterprisePolicy(policy_path=policy_path)
        
        # 测试允许的命令
        request1 = PermissionRequest(
            tool_name='shell',
            operation='git status',
            risk_level=RiskLevel.LOW
        )
        result1 = checker.check(request1)
        assert result1.decision.value == 'allow'
        assert '企业策略允许' in result1.reason
        
        # 测试允许的路径
        request2 = PermissionRequest(
            tool_name='file',
            operation='write',
            target_path='/tmp/test.txt',
            risk_level=RiskLevel.MEDIUM
        )
        result2 = checker.check(request2)
        assert result2.decision.value == 'allow'
        assert '企业策略允许' in result2.reason
        
        # 测试允许的操作类型
        request3 = PermissionRequest(
            tool_name='file',
            operation='read',
            target_path='/tmp/test.txt',
            risk_level=RiskLevel.LOW
        )
        result3 = checker.check(request3)
        assert result3.decision.value == 'allow'
        assert '企业策略允许' in result3.reason
        
    finally:
        # 清理临时文件
        if os.path.exists(policy_path):
            os.unlink(policy_path)


def test_enterprise_policy_not_enforced():
    """测试企业策略未启用的情况"""
    # 创建临时策略文件（未启用）
    with tempfile.NamedTemporaryFile(mode='w', suffix='.toml', delete=False) as f:
        policy = {
            'enterprise_policy': {
                'global': {
                    'enforce': False
                },
                'deny_list': {
                    'commands': ['rm -rf *']
                }
            }
        }
        toml.dump(policy, f)
        policy_path = f.name
    
    try:
        # 初始化企业策略检查器
        checker = EnterprisePolicy(policy_path=policy_path)
        
        # 测试操作（应该通过，因为策略未启用）
        request = PermissionRequest(
            tool_name='shell',
            operation='rm -rf /tmp/*',
            risk_level=RiskLevel.HIGH
        )
        result = checker.check(request)
        assert result.decision.value == 'allow'
        assert '无企业策略或未启用，继续检查' in result.reason
        
    finally:
        # 清理临时文件
        if os.path.exists(policy_path):
            os.unlink(policy_path)


def test_enterprise_policy_no_policy():
    """测试无企业策略文件的情况"""
    # 使用不存在的策略文件路径
    checker = EnterprisePolicy(policy_path='/nonexistent/path/enterprise_policy.toml')
    
    # 测试操作
    request = PermissionRequest(
        tool_name='shell',
        operation='ls -la',
        risk_level=RiskLevel.LOW
    )
    result = checker.check(request)
    assert result.decision.value == 'allow'
    assert '无企业策略或未启用，继续检查' in result.reason
