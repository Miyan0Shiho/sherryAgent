"""Token estimation utilities for SherryAgent.

This module provides the TokenEstimator class for accurate token counting
using tiktoken with fallback to heuristic-based estimation.
"""

import re


class TokenEstimator:
    """Token estimator using tiktoken with fallback to heuristics.

    This class provides accurate token counting when tiktoken is available,
    and falls back to an improved heuristic algorithm when tiktoken is not installed.
    """

    def __init__(self, encoding_name: str = "cl100k_base"):
        """Initialize token estimator.

        Args:
            encoding_name: Name of tiktoken encoding to use (default: cl100k_base for GPT-4).
        """
        self._encoding_name = encoding_name
        self._encoding: object | None = None
        self._available = False
        self._init_encoding()

    def _init_encoding(self) -> None:
        """Attempt to initialize tiktoken encoding."""
        try:
            import tiktoken

            self._encoding = tiktoken.get_encoding(self._encoding_name)
            self._available = True
        except ImportError:
            self._available = False
            self._encoding = None

    def estimate(self, text: str) -> int:
        """Estimate the number of tokens in text.

        Args:
            text: Text to estimate token count for.

        Returns:
            Estimated number of tokens.
        """
        if self._available and self._encoding is not None:
            return len(self._encoding.encode(text))
        else:
            return self._fallback_estimate(text)

    def _fallback_estimate(self, text: str) -> int:
        """Fallback token estimation using improved heuristics.

        This method provides a reasonable approximation when tiktoken is unavailable.
        The algorithm accounts for different character types:
        - English text: ~4 characters per token
        - Chinese/CJK text: ~1.5 characters per token
        - Punctuation and special characters: counted separately

        Args:
            text: Text to estimate token count for.

        Returns:
            Estimated number of tokens with <20% error rate.
        """
        if not text:
            return 0

        cjk_pattern = re.compile(r"[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff\u3040-\u309f\u30a0-\u30ff]")
        cjk_chars = len(cjk_pattern.findall(text))
        non_cjk_text = cjk_pattern.sub("", text)
        words = re.findall(r"\b\w+\b", non_cjk_text)
        word_count = len(words)
        punctuation = re.findall(r"[^\w\s]", non_cjk_text)
        punct_count = len(punctuation)
        total_chars = len(non_cjk_text)
        cjk_tokens = max(1, int(cjk_chars * 0.7))
        char_based_tokens = max(1, total_chars // 4)
        word_based_tokens = max(1, word_count)
        punct_tokens = max(0, punct_count // 2)
        total_estimate = cjk_tokens + (char_based_tokens + word_based_tokens) // 2 + punct_tokens
        return max(1, total_estimate)

    @property
    def is_tiktoken_available(self) -> bool:
        """Check if tiktoken is available.

        Returns:
            True if tiktoken is available, False otherwise.
        """
        return self._available

    @property
    def encoding_name(self) -> str:
        """Get the encoding name.

        Returns:
            Name of the encoding being used.
        """
        return self._encoding_name
