# Databricks notebook source
# MAGIC %md ## Get Registered Model
# MAGIC
# MAGIC Get registered model and its versions for either UC and non-UC models.
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

client = get_client(model_name)

# COMMAND ----------

# MAGIC %md #### Get registered model

# COMMAND ----------

model = client.get_registered_model(model_name)
dump_obj(model, "Registered Model")

# COMMAND ----------

# MAGIC %md #### Get latest model versions - only non-UC
# MAGIC Note: UC returns None for model.latest_versions not []

# COMMAND ----------

if model.latest_versions:
    for v in model.latest_versions:
        dump_obj(v, "Latest Model Version")

# COMMAND ----------

# MAGIC %md #### Get all model versions

# COMMAND ----------

filter = f"name = '{model_name}'"
versions = client.search_model_versions(filter)
len(versions)

# COMMAND ----------

versions = sorted(versions, key=lambda v: v.name)
len(versions)

# COMMAND ----------

for v in versions:
    dump_obj(v, "Model Version")
