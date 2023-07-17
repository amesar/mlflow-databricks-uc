# Databricks notebook source
# MAGIC %md ## Register Model
# MAGIC
# MAGIC Register a model version from either a run (`runs:` URI) or an existing model version (`models:` URI).
# MAGIC
# MAGIC If you use a models URI, the new model version will not point to a Run ID, and therefore you will not be able to navigate to the run from model version UI page.
# MAGIC
# MAGIC Widgets:
# MAGIC * `1. Model name` - example: my_catalog.ml_models.sklearn_wine
# MAGIC * `2. Source Model URI` - the model to register. Examples:
# MAGIC   * Runs URI: `runs:/76031d22c5464dd99431e426b939e800/model`
# MAGIC   * Models URI: `models:/andre_catalog.ml_models2.sklearn_wine_best/1`
# MAGIC * `3. Alias`
# MAGIC * `4. Description`

# COMMAND ----------

# MAGIC %md #### Setup

# COMMAND ----------

# MAGIC %run ./Common

# COMMAND ----------

dbutils.widgets.text("1. Model name", "")
model_name = dbutils.widgets.get("1. Model name")

dbutils.widgets.text("2. Source Model URI", "")
model_uri = dbutils.widgets.get("2. Source Model URI")

dbutils.widgets.text("3. Alias", "")
alias = dbutils.widgets.get("3. Alias")

dbutils.widgets.text("4. Description", "")
description = dbutils.widgets.get("4. Description")

print("model_name:", model_name)
print("model_uri:", model_uri)
print("alias:", alias)
print("description:", description)

# COMMAND ----------

assert_widget(model_name, "1. Model name")
assert_widget(model_uri, "2. Source Model URI")

# COMMAND ----------

# MAGIC %md #### Register model - create new model version

# COMMAND ----------

version = mlflow.register_model(model_uri=model_uri, name=model_name)
version

# COMMAND ----------

if description:
    client.update_model_version(model_name, version.version, description)

# COMMAND ----------

if alias:
    client.set_registered_model_alias(model_name, alias, version.version)

# COMMAND ----------

# MAGIC %md #### Display new model version

# COMMAND ----------

version = client.get_model_version(model_name, version.version)
dump_obj(version)
