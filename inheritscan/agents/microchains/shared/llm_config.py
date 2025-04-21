from myagents.microchains.shared.stateless_tinyllama import StatelessOllamaLLM


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
