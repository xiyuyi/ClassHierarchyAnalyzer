from langchain.prompts import PromptTemplate

class_summary_prompt_english = PromptTemplate(
    input_variables=["input_chunk"],
    template="""
You are an experienced software engineer.

Please provide a concise, high-level summary of the purpose
and intent of the following Python Class, based on the provided
aggregated summaries of its Methods.
- First, give a one-sentence summary of what the Class does using no more than 50 words.
- Then, list bullet points explaining the purpose and key responsibilities of the class
- avoiding implementation details unless essential for understanding.
- Focus on what the class achieves, not how it works.

Follow the forma:
Summary:
[the one-sentence summary]

Bulletin points:
[the bulletin-points]

Here are the aggregated and sorted summaries for the methods:

Aggregated Method Summaries:
{aggregated_method_summaries}
""",
)


class_summary_prompt_english_1_paragraph = PromptTemplate(
    input_variables=["input_chunk"],
    template="""
You are an experienced software engineer.

Please provide a concise, high-level 1 paragraph. summary of the purpose
and intent of the following Python Class, based on the provided
aggregated summaries of its Methods.
- First, give a one-paragraph summary of what the Class does using no more than 50 words.
- avoiding implementation details unless essential for understanding.
- Focus on what the class achieves, not how it works.

The output should just be one paragraph of plain text.

Here are the aggregated and sorted summaries for the methods:

Aggregated Method Summaries:
{aggregated_method_summaries}
""",
)
