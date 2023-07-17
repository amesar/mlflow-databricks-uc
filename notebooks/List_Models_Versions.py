# Databricks notebook source
# MAGIC %md ## List Model Versions
# MAGIC
# MAGIC Search for version within one registered model.
# MAGIC
# MAGIC Widgets:
# MAGIC * `Model name` - example: my_catalog.ml_models.sklearn_wine

# COMMAND ----------

# MAGIC %md #### Setup

# COMMAND ----------

# MAGIC %run ./Common

# COMMAND ----------

dbutils.widgets.text("Model name", "")
model_name = dbutils.widgets.get("Model name")
print("model_name:", model_name)

# COMMAND ----------

# MAGIC %md #### Search for model versions

# COMMAND ----------

filter = f"name = '{model_name}'"
versions = client.search_model_versions(filter)
len(versions)

# COMMAND ----------

# MAGIC %md #### Display model versions

# COMMAND ----------

versions = sorted(versions, key=lambda v: v.name)

# COMMAND ----------

for v in versions:
    print(v.version)

# COMMAND ----------

for v in versions:
    dump_obj(v, "Model Version")
