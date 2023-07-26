# Databricks notebook source
# MAGIC %md ## List Registered Models
# MAGIC
# MAGIC **Widgets**
# MAGIC * `1. Model name` 
# MAGIC   * UC: Since UC doesn't support `search_registered_models()`, we improvise:
# MAGIC     *  with filter by Python `startswith()`
# MAGIC   * non-UC: normal `search_registered_models()` filter
# MAGIC * `2. Unity Catalog`

# COMMAND ----------

# MAGIC %md #### Setup

# COMMAND ----------

# MAGIC %run ./Common

# COMMAND ----------

dbutils.widgets.text("1. Model name", "")
model_name = dbutils.widgets.get("1. Model name")

dbutils.widgets.dropdown("2. Unity Catalog", "yes", ["yes","no"])
use_uc = dbutils.widgets.get("2. Unity Catalog") == "yes"

print("model_name:", model_name)
print("use_uc:", use_uc)

# COMMAND ----------

client = get_client_uc(use_uc)

# COMMAND ----------

# MAGIC %md #### Search for registered models

# COMMAND ----------

models = client.search_registered_models()
len(models)

# COMMAND ----------

# MAGIC %md #### Search
# MAGIC
# MAGIC **UC**
# MAGIC
# MAGIC Does not support standard `filter_string` for search_registered_models().
# MAGIC
# MAGIC MlflowException: Argument 'filter_string' is unsupported for models in the Unity Catalog. See the user guide for more information
# MAGIC
# MAGIC **Non-UC**
# MAGIC
# MAGIC Search with standard `filter_string` argument for search_registered_models().

# COMMAND ----------

if model_name:
    if use_uc:
          models = [ m for m in models if m.name.startswith(model_name)]
    else:
        filter = f"name like '{model_name}%'" 
        models = client.search_registered_models(filter_string=filter)
    print(f"Found {len(models)} models")

# COMMAND ----------

# MAGIC %md #### Display models

# COMMAND ----------

models = sorted(models, key=lambda m: m.name)

# COMMAND ----------

for m in models:
    print(m.name)

# COMMAND ----------

for m in models:
    dump_obj(m)
