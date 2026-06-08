# 🗃️ Retrieval-Augmented SQL (RA-SQL)

[![Accuracy](https://img.shields.io/badge/SQL%20Accuracy-94.1%25-green)](.) [![Databases](https://img.shields.io/badge/Databases-BigQuery%7CPostgres%7CMySQL-blue)](.) [![Spider](https://img.shields.io/badge/Spider%20Benchmark-Top%205%25-orange)](.)

> **Natural language to SQL** with RAG-enhanced few-shot learning. Handles complex joins, CTEs, window functions and subqueries. **94.1% accuracy** on enterprise schemas with 500+ tables.

## 🏆 Results
- **94.1% execution accuracy** on complex enterprise schemas
- **Top 5%** on Spider NL2SQL benchmark
- Handles schemas with **500+ tables** and complex relationships
- **Auto-correction**: retries with error feedback until valid SQL

## 🔄 Pipeline
```
Natural Language → Schema RAG (find relevant tables/columns)
               → Few-shot Examples RAG (similar past queries)
               → SQL Generation (Gemini 1.5 Pro)
               → Validation (dry-run on DB)
               → Auto-correction if invalid
               → Execute + Format results
```
