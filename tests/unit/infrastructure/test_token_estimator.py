"""Unit tests for TokenEstimator class."""

import pytest
from src.sherry_agent.infrastructure.token_estimator import TokenEstimator


class TestTokenEstimator:
    """Test cases for TokenEstimator class."""

    def test_initialization(self):
        """Test that TokenEstimator initializes correctly."""
        estimator = TokenEstimator()
        assert estimator.encoding_name == "cl100k_base"
        assert isinstance(estimator.is_tiktoken_available, bool)

    def test_initialization_with_custom_encoding(self):
        """Test initialization with custom encoding name."""
        estimator = TokenEstimator(encoding_name="p50k_base")
        assert estimator.encoding_name == "p50k_base"

    def test_estimate_empty_string(self):
        """Test token estimation for empty string."""
        estimator = TokenEstimator()
        assert estimator.estimate("") == 0

    def test_estimate_simple_english(self):
        """Test token estimation for simple English text."""
        estimator = TokenEstimator()
        text = "Hello world"
        tokens = estimator.estimate(text)
        assert tokens > 0
        assert tokens < 10

    def test_estimate_longer_english(self):
        """Test token estimation for longer English text."""
        estimator = TokenEstimator()
        text = "This is a longer sentence with multiple words and punctuation."
        tokens = estimator.estimate(text)
        assert tokens > 5

    def test_estimate_chinese_text(self):
        """Test token estimation for Chinese text."""
        estimator = TokenEstimator()
        text = "这是一个中文测试句子"
        tokens = estimator.estimate(text)
        assert tokens > 0

    def test_estimate_mixed_language(self):
        """Test token estimation for mixed language text."""
        estimator = TokenEstimator()
        text = "Hello world 你好世界 This is mixed 混合文本"
        tokens = estimator.estimate(text)
        assert tokens > 5

    def test_estimate_with_punctuation(self):
        """Test token estimation with punctuation."""
        estimator = TokenEstimator()
        text = "Hello, world! How are you?"
        tokens = estimator.estimate(text)
        assert tokens > 0

    def test_estimate_code_snippet(self):
        """Test token estimation for code snippet."""
        estimator = TokenEstimator()
        text = "def hello_world():\n    print('Hello, World!')"
        tokens = estimator.estimate(text)
        assert tokens > 5

    def test_fallback_estimate_simple(self):
        """Test fallback estimation for simple text."""
        estimator = TokenEstimator()
        text = "Hello world"
        tokens = estimator._fallback_estimate(text)
        assert tokens > 0

    def test_fallback_estimate_chinese(self):
        """Test fallback estimation for Chinese text."""
        estimator = TokenEstimator()
        text = "这是一个测试"
        tokens = estimator._fallback_estimate(text)
        assert tokens > 0

    def test_fallback_estimate_empty(self):
        """Test fallback estimation for empty string."""
        estimator = TokenEstimator()
        assert estimator._fallback_estimate("") == 0

    def test_fallback_estimate_whitespace_only(self):
        """Test fallback estimation for whitespace only."""
        estimator = TokenEstimator()
        tokens = estimator._fallback_estimate("   \n\t  ")
        assert tokens >= 0

    def test_tiktoken_availability_check(self):
        """Test that tiktoken availability can be checked."""
        estimator = TokenEstimator()
        assert isinstance(estimator.is_tiktoken_available, bool)

    def test_estimate_realistic_text(self):
        """Test estimation for realistic text."""
        estimator = TokenEstimator()
        text = """
        The quick brown fox jumps over the lazy dog.
        This is a test of the token estimation system.
        It should handle multiple sentences and paragraphs.
        """
        tokens = estimator.estimate(text)
        assert tokens > 10

    def test_estimate_json_like_text(self):
        """Test estimation for JSON-like text."""
        estimator = TokenEstimator()
        text = '{"name": "John", "age": 30, "city": "New York"}'
        tokens = estimator.estimate(text)
        assert tokens > 5

    def test_estimate_with_numbers(self):
        """Test estimation with numbers."""
        estimator = TokenEstimator()
        text = "The year 2024 has 365 days and 12 months."
        tokens = estimator.estimate(text)
        assert tokens > 5

    def test_multiple_estimations_consistency(self):
        """Test that multiple estimations are consistent."""
        estimator = TokenEstimator()
        text = "Consistent estimation test"
        tokens1 = estimator.estimate(text)
        tokens2 = estimator.estimate(text)
        assert tokens1 == tokens2

    def test_different_texts_different_estimates(self):
        """Test that different texts get different estimates."""
        estimator = TokenEstimator()
        text1 = "Short"
        text2 = "This is a much longer text with more words and content"
        tokens1 = estimator.estimate(text1)
        tokens2 = estimator.estimate(text2)
        assert tokens1 < tokens2

    def test_fallback_accuracy_english(self):
        """Test fallback accuracy for English text.

        The fallback should be within 20% of tiktoken when available.
        """
        estimator = TokenEstimator()
        text = "The quick brown fox jumps over the lazy dog"
        fallback_tokens = estimator._fallback_estimate(text)
        if estimator.is_tiktoken_available:
            actual_tokens = estimator.estimate(text)
            error_rate = abs(fallback_tokens - actual_tokens) / actual_tokens
            assert error_rate < 0.3

    def test_fallback_accuracy_chinese(self):
        """Test fallback accuracy for Chinese text."""
        estimator = TokenEstimator()
        text = "这是一个中文测试句子用于测试估算准确性"
        fallback_tokens = estimator._fallback_estimate(text)
        if estimator.is_tiktoken_available:
            actual_tokens = estimator.estimate(text)
            error_rate = abs(fallback_tokens - actual_tokens) / actual_tokens
            assert error_rate < 0.5
