from openai import OpenAI


class AuditQuestionsAnalyzer:
    def __init__(self, api_key: str, model: str = "gpt-4.1-mini"):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def analyze(self, pdf_path: str) -> str:
        file_id = self._upload_file(pdf_path)
        return self._request_analysis(file_id)

    def _upload_file(self, pdf_path: str) -> str:
        with open(pdf_path, "rb") as f:
            uploaded = self.client.files.create(
                file=f,
                purpose="user_data"
            )
        return uploaded.id

    def _request_analysis(self, file_id: str) -> str:
        response = self.client.responses.create(
            model=self.model,
            input=[
                {
                    "role": "user",
                    "content": [
                        {"type": "input_file", "file_id": file_id},
                        {"type": "input_text", "text": self._build_prompt()}
                    ]
                }
            ]
        )
        return response.output_text.strip()

    def _build_prompt(self) -> str:
        return """
Найди в PDF раздел аудиторского заключения под названием:
- "Ключевые вопросы аудита"
- "Ключевой вопрос аудита"

Если раздел найден, верни только краткую выжимку на русском языке в 5-6 предложениях.
Выжимка должна быть понятна финансовому аналитику и должна коротко объяснять:
- какие темы аудитор считает наиболее важными,
- на какие статьи отчетности стоит обратить внимание,
- где есть риск оценочных суждений, неопределенности или возможных искажений.

Правила:
- Не возвращай JSON.
- Не цитируй большие куски текста.
- Не пересказывай весь документ.
- Пиши кратко, делово и по существу.
- Если раздел не найден, верни одну фразу:
  "Раздел 'Ключевые вопросы аудита' в документе не найден."
"""