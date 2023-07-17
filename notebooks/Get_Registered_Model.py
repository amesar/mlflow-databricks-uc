# Databricks notebook source
# MAGIC %md ## Get Registered Model
# MAGIC
# MAGIC Get registered model and its versions.
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

# MAGIC %md #### Get registered model

# COMMAND ----------

model = client.get_registered_model(model_name)
dump_obj(model, "Registered Model")

# COMMAND ----------

# MAGIC %md #### Get model versions

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
