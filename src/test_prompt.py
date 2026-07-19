from src.text_generator import TextGenerator

generator = TextGenerator()

context = """ Core components:
-Self-Atention: allows each token to attend to all others tokens
-Positional Encoding: injects position information
"""


prompt = """Use the following context to answer the question.
If the answer is not the context , say I don't know! Do not make up an answer

context = {context}

Question:
what is the capital of France?


Answer:
"""

print(generator.generate(prompt))


