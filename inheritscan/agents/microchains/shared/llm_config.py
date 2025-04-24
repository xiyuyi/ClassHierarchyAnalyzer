from inheritscan.agents.microchains.shared.stateless_tinyllama import StatelessOllamaLLM
from inheritscan.agents.microchains.shared.together_ai import TogetherQwenCoder


def get_tinyllm150():
    return StatelessOllamaLLM(
        model="mistral",
        num_predict=150,
        temperature=0.0,
        top_p=1.0,
        top_k=0,
        stop=["Explanation complete.", "\n\n"],
    )


def get_tinyllm100():
    return StatelessOllamaLLM(
        model="mistral",
        num_predict=100,
        temperature=0.0,
        top_p=1.0,
        top_k=0,
        stop=["Explanation complete.", "\n\n"],
    )

def get_qwen_coder_instruct500():
    return TogetherQwenCoder(
        model="Qwen/Qwen2.5-Coder-32B-Instruct",
        max_tokens=500,
        temperature=0,
        top_p=0.95,
        min_p=0.05,
        top_k=40,
        repetition_penalty=1.1,
        presence_penalty=0,
        frequency_penalty=0,
        seed=42
    )

def get_qwen_coder_instruct2000():
    return TogetherQwenCoder(
        model="Qwen/Qwen2.5-Coder-32B-Instruct",
        max_tokens=2000,
        temperature=0,
        top_p=0.95,
        min_p=0.05,
        top_k=100,
        repetition_penalty=1.1,
        presence_penalty=0,
        frequency_penalty=0,
        seed=42
    )

