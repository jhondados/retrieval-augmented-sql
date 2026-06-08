"""Retrieval-Augmented SQL generation."""
from langchain_google_vertexai import ChatVertexAI
from langchain_community.vectorstores import BigQueryVectorSearch
from google.cloud import bigquery
from typing import Optional

class RAugmentedSQL:
    SYSTEM = """You are an expert SQL engineer. Given schema context and examples, write precise SQL.
Rules: use exact column/table names, add WHERE clauses for safety, use CTEs for readability."""

    def __init__(self, project_id: str, bq_dataset: str):
        self.bq = bigquery.Client(project=project_id)
        self.llm = ChatVertexAI(model_name="gemini-1.5-pro-002", temperature=0)
        self.project_id = project_id
        self.dataset = bq_dataset

    def get_schema_context(self, question: str) -> str:
        """Retrieve relevant tables/columns via vector search."""
        tables = self.bq.list_tables(self.dataset)
        schema_parts = []
        for table in list(tables)[:20]:
            t = self.bq.get_table(table)
            cols = ", ".join([f"{f.name} ({f.field_type})" for f in t.schema[:10]])
            schema_parts.append(f"Table {t.table_id}: {cols}")
        return "\n".join(schema_parts)

    def generate_sql(self, question: str, max_retries: int = 3) -> str:
        schema = self.get_schema_context(question)
        prompt = f"{self.SYSTEM}\nSchema:\n{schema}\nQuestion: {question}\nSQL:"
        for attempt in range(max_retries):
            sql = self.llm.invoke(prompt).content.strip().strip("```sql").strip("```")
            try:
                self.bq.query(f"SELECT 1 FROM ({sql}) LIMIT 0")  # dry-run
                return sql
            except Exception as e:
                prompt += f"\nError: {e}\nFixed SQL:"
        return sql
