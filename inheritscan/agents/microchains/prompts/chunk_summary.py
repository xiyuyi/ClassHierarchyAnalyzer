from langchain.prompts import PromptTemplate

chunk_summary_prompt_korean = PromptTemplate(
    input_variables=["input_chunk"],
    template="""
당신은 숙련된 소프트웨어 엔지니어입니다.  
다음 Python 코드 조각이 무엇을 하고 왜 존재하는지를 중심으로, 고수준에서 요약해 주세요.  
간결하고 개발자 중심의 스타일을 사용하고, 중요하지 않은 저수준 구현 세부사항은 생략하세요.
한국어로 대답해 주세요.

코드 조각:
```python
{input_chunk}
""",
)

chunk_summary_prompt_english = PromptTemplate(
    input_variables=["input_chunk"],
    template="""
You are an experienced software engineer.

- Summarize the following Python code chunk at low-level, give short, concise and punctual 
bulletin points of what it does at low level without too much details.
- Contain details to the level of this chunk such that it would make sense with other chunks 
with the same level of details, I will use it for summarizaiton later.
- If you see multiple lines can be explained and summarized together, summarize them together.
- Use a concise, dev-oriented style. 
- Please reply in English.

Code chunk:
```python
{input_chunk}
```
""",
)


chunk_summary_prompt_chinese = PromptTemplate(
    input_variables=["input_chunk"],
    template="""
你是一位经验丰富的软件工程师。
请从高层次的角度总结以下 Python 代码片段的作用以及它为何存在。
请使用简洁、以开发者为导向的风格，忽略不重要的底层实现细节。
请用中文作答。

代码片段：
```python
{input_chunk}
""",
)
