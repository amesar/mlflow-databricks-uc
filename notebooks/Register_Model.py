# Databricks notebook source
# MAGIC %md ## Register Model
# MAGIC
# MAGIC Register a new model version from a run model.
# MAGIC
# MAGIC Widgets:
# MAGIC * `1. Source Run ID` - example: `76031d22c5464dd99431e426b939e800`
# MAGIC * `2. Source Model Artifact` - example: `model`
# MAGIC * `3. Model name` - example: `andre_catalog.ml_models.sklearn_wine`
# MAGIC * `4. Alias`
# MAGIC * `5. Description`

# COMMAND ----------

# MAGIC %md #### Setup

# COMMAND ----------

# MAGIC %run ./Common

# COMMAND ----------

dbutils.widgets.text("1. Source Run ID", "")
run_id = dbutils.widgets.get("1. Source Run ID")

dbutils.widgets.text("2. Source Model Artifact", "model")
model_artifact = dbutils.widgets.get("2. Source Model Artifact")

dbutils.widgets.text("3. Model name", "")
model_name = dbutils.widgets.get("3. Model name")

dbutils.widgets.text("4. Alias", "")
alias = dbutils.widgets.get("4. Alias")

dbutils.widgets.text("5. Description", "")
description = dbutils.widgets.get("5. Description")

print("run_id:", run_id)
print("model_artifact:", model_artifact)
print("model_name:", model_name)
print("alias:", alias)
print("description:", description)

# COMMAND ----------

assert_widget(run_id, "1. Run ID")
assert_widget(model_name, "3. Model name")

# COMMAND ----------

# MAGIC %md #### Register model - create new model version

# COMMAND ----------

path = f"/{model_artifact}" if model_artifact else ""
model_uri = f"runs:/{run_id}{path}"
model_uri

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
