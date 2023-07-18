# Databricks notebook source
# MAGIC %md ## Create Model Version from URI
# MAGIC
# MAGIC **Overview**
# MAGIC * Creates a new model version from model URI. 
# MAGIC * Copies source version's metadata (description, tags and aliases) to target version.
# MAGIC * Option to overwrite description or add a new alias.
# MAGIC
# MAGIC **Widgets**
# MAGIC * `2. Source Model URI` - the model to register. Examples:
# MAGIC   * Runs URI: `runs:/76031d22c5464dd99431e426b939e800/model`
# MAGIC   * Models URI: `models:/andre_catalog.ml_models2.sklearn_wine_best/1`
# MAGIC * `1. Source model name` - example: `andre_catalog.ml_models.sklearn_wine`
# MAGIC * `2. Source model version` 
# MAGIC * `3. New model name` 
# MAGIC * `4. Alias` - alias to append to source version aliases
# MAGIC * `5. Description` - replace source version description if specified

# COMMAND ----------

# MAGIC %md #### Setup

# COMMAND ----------

# MAGIC %run ./Common

# COMMAND ----------

dbutils.widgets.text("1. Source model URI", "")
src_model_uri = dbutils.widgets.get("1. Source model URI")

dbutils.widgets.text("2. New model name", "")
dst_model_name = dbutils.widgets.get("2. New model name")

dbutils.widgets.text("3. Alias", "")
alias = dbutils.widgets.get("3. Alias")

dbutils.widgets.text("4. Description", "")
description = dbutils.widgets.get("4. Description")

print("src_model_uri:", src_model_uri)
print("dst_model_name:", dst_model_name)
print("alias:", alias)
print("description:", description)

# COMMAND ----------

assert_widget(src_model_uri, "1. Source model URI")
assert_widget(dst_model_name, "2. New model name")

# COMMAND ----------

dst_client = get_client(dst_model_name)

# COMMAND ----------

# MAGIC %md #### Register model - create new model version

# COMMAND ----------

dst_version = mlflow.register_model(
    model_uri = src_model_uri, 
    name = dst_model_name
)
dst_version

# COMMAND ----------

# MAGIC %md #### Set model version metadata

# COMMAND ----------

if description:
    dst_client.update_model_version(dst_model_name, dst_version.version, description)

# COMMAND ----------

if alias:
    print(f"Setting alias '{alias}'")
    dst_client.set_registered_model_alias(dst_model_name, alias, dst_version.version)

# COMMAND ----------

# MAGIC %md #### Display new model version

# COMMAND ----------

dst_version = dst_client.get_model_version(dst_model_name, dst_version.version)
dump_obj(dst_version)

# COMMAND ----------

display_model_version_uri(dst_model_name, dst_version.version)
