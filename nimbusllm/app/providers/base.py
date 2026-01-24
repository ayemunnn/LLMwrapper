from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

class BaseLLMProvider(ABC):
    @abstractmethod
    async def generate(
        self,
        messages: List[Dict[str, str]],
        model: str,
        temperature: float,
        max_tokens: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Must return dict with:
          - text: str
          - usage: {input_tokens:int, output_tokens:int} (optional)
          - raw: any (optional)
        """
        raise NotImplementedError
