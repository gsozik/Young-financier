import json
from openai import OpenAI


class MetricsLLMInterpreter:
    def __init__(self, api_key: str, model: str = "gpt-4.1-mini"):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def interpret(self, metrics: dict) -> str:
        response = self.client.responses.create(
            model=self.model,
            input=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": self._build_prompt(metrics)
                        }
                    ]
                }
            ]
        )
        return response.output_text.strip()

    def _build_prompt(self, metrics: dict) -> str:
        return f"""
Ты финансовый аналитик.

Ниже дан словарь финансовых метрик компании:
{json.dumps(metrics, ensure_ascii=False, indent=2)}

Задача:
- кратко проанализируй эти метрики на русском языке;
- напиши 5-6 предложений;
- укажи, какие показатели выглядят сильными;
- укажи, какие показатели выглядят слабыми или аномальными;
- если есть невероятные или подозрительные значения, прямо скажи, что их нужно проверить вручную;
- отдельно укажи, на что стоит обратить внимание инвестору.

Правила:
- не возвращай JSON;
- не переписывай все метрики подряд;
- не пиши слишком длинно;
- не выдумывай отсутствующие данные;
- если метрика равна null, просто не опирайся на нее;
- если показатель выглядит экономически странно, назови его подозрительным;
- ответ должен быть деловым и понятным.
"""