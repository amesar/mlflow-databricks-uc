# Databricks notebook source
# MAGIC %md ## List Registered Models
# MAGIC

# COMMAND ----------

# MAGIC %run ./Common

# COMMAND ----------

use_unity_catalog(True)

# COMMAND ----------

models = client.search_registered_models()
len(models)

# COMMAND ----------

for model in models:
    print(model.name)
