from transformers import pipeline


class TextGenerator:
    def __init__(self):
        self.generator = pipeline(
            "text2text-generation",
            model="google/flan-t5-small"
        )

    def generate(self, prompt: str) -> str:
        output: list[dict] = self.generator(  # type: ignore
            prompt,
            max_new_tokens=150
        )
        return str(output[0]["generated_text"])