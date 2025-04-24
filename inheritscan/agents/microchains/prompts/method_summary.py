from langchain.prompts import PromptTemplate

method_summary_prompt_english = PromptTemplate(
    input_variables=["input_chunk"],
    template="""
You are an experienced software engineer.

Please provide a concise, high-level summary of the purpose 
and intent of the following class method, based on the provided 
aggregated summaries of its code chunks.
- First, give a one-sentence summary of what the method does using no more than 50 words.
- Then, list bullet points explaining the purpose and key responsibilities of the method
- avoiding implementation details unless essential for understanding.
- Focus on what the method achieves, not how it works.

Follow the forma:
Summary:
[the one-sentence summary]

Bulletin points:
[the bulletin-points]

Here are the aggregated and sorted summaries for the code chunks:

Aggregated Chunk Summaries:
{aggregated_chunk_summaries}
""",
)


