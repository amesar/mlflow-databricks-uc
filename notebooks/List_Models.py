# Databricks notebook source
# MAGIC %md ## List Registered Models
# MAGIC
# MAGIC Widgets:
# MAGIC * `Model name` - filter by - "startswith"

# COMMAND ----------

# MAGIC %md #### Setup

# COMMAND ----------

# MAGIC %run ./Common

# COMMAND ----------

dbutils.widgets.text("Model name", "")
model_name = dbutils.widgets.get("Model name")
print("model_name:", model_name)

# COMMAND ----------

# MAGIC %md #### Search for registered models

# COMMAND ----------

models = client.search_registered_models()
len(models)

# COMMAND ----------

# MAGIC %md #### Search with filter - non-UC only
# MAGIC
# MAGIC MlflowException: Argument 'filter_string' is unsupported for models in the Unity Catalog. See the user guide for more information

# COMMAND ----------

# filter = f"name like '{model_name}%'" 
# models = client.search_registered_models(filter_string=filter)
# len(models)

# COMMAND ----------

# MAGIC %md #### UC-specific client-side filter

# COMMAND ----------

if model_name:
    models = [ m for m in models if m.name.startswith(model_name)]
len(models)

# COMMAND ----------

# MAGIC %md #### Display models

# COMMAND ----------

models = sorted(models, key=lambda m: map.name)

# COMMAND ----------

for m in models:
    print(m.name)

# COMMAND ----------

for m in models:
    dump_obj(m,"Model")
