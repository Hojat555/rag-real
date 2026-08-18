from src.text_generator import TextGenerator

generator = TextGenerator()

prompt = """
Ask the question using only the provided context.

Write a clear and complete answer in 2 or 3 sentences.
Do not return an incomplete phrase.

Context:
Before Transformers, recuurent neural networks processed text step by step.
This caused limitations a Transformer to consider the entire input sequence
and identify relationships between different parts of the text.

Qusetion:
why can Transformers models process sequences more efficiently than recurrent neural networks?\

Complete Answer:
"""
answer = generator.generate(prompt)
print(answer)
