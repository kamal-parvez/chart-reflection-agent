from .providers import generate_text

def build_prompt(instruction: str, schema_text: str, out_path: str) -> str:
    prompt = f"""
Return your answer strictly in this format, nothing else:

<execute_python>
# valid python code here
</execute_python>

The code must create a matplotlib chart from a DataFrame named `df` with these columns:
{schema_text}

User instruction: {instruction}

Requirements:
1. Assume `df` is already loaded — do not read any file.
2. Use matplotlib only.
3. Add a clear title, axis labels, and a legend if needed.
4. Save the figure to '{out_path}' with dpi=300.
5. Do not call plt.show().
6. Call plt.close() at the end.
7. Include every import statement the code needs.
"""
    return prompt.strip()


def generate_chart_code(model: str, instruction: str, schema_text: str, out_path: str) -> str:
    prompt = build_prompt(instruction, schema_text, out_path)
    return generate_text(model, prompt)
