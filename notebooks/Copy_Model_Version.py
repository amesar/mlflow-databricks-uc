# Databricks notebook source
# MAGIC %md ## Copy a Model Version
# MAGIC
# MAGIC **Overview**
# MAGIC * Copy one model version to another. 
# MAGIC * Uses the version's registry MLflow model run and not the source version run MLflow model.
# MAGIC * Copies source version's metadata (description, tags and aliases) to target version.
# MAGIC * Option to overwrite description or add a new alias.
# MAGIC
# MAGIC **Widgets**
# MAGIC * `1. Source model name` - example: `andre_catalog.ml_models.sklearn_wine`
# MAGIC * `2. Source model version` 
# MAGIC * `3. New model name` 
# MAGIC * `4. Alias` - alias to append to source version aliases
# MAGIC * `5. Description` - replace source version description if specified
# MAGIC * `6. Set model version lineage` - Save the following source version tags:
# MAGIC   * `_mlflow_lineage.source_model_version.name`
# MAGIC   * `_mlflow_lineage.source_model_version.version`
# MAGIC   * `_mlflow_lineage.source_model_version.copy_user`
# MAGIC   * `_mlflow_lineage.source_model_version.copy_time` - milliseconds of copy time
# MAGIC   * `_mlflow_lineage.source_model_version.copy_time_nice` - ibid but human-friendly

# COMMAND ----------

# MAGIC %md #### Setup

# COMMAND ----------

# MAGIC %run ./Common

# COMMAND ----------

dbutils.widgets.text("1. Source model name", "")
src_model_name = dbutils.widgets.get("1. Source model name")

dbutils.widgets.text("2. Source model version", "")
src_model_version = dbutils.widgets.get("2. Source model version")

dbutils.widgets.text("3. New model name", "")
dst_model_name = dbutils.widgets.get("3. New model name")

dbutils.widgets.text("4. Alias", "")
alias = dbutils.widgets.get("4. Alias")

dbutils.widgets.text("5. Description", "")
description = dbutils.widgets.get("5. Description")

dbutils.widgets.dropdown("6. Set model version lineage", "no", ["yes","no"])
set_model_version_lineage = dbutils.widgets.get("6. Set model version lineage") == "yes"

print("src_model_name:", src_model_name)
print("src_model_version:", src_model_version)
print("dst_model_name:", src_model_name)
print("alias:", alias)
print("description:", description)
print("set_model_version_lineage:", set_model_version_lineage)

# COMMAND ----------

assert_widget(src_model_name, "1. Source model name")
assert_widget(src_model_name, "2. Source model version")
assert_widget(dst_model_name, "3. New model name")

# COMMAND ----------

src_client, dst_client = get_clients(src_model_name, dst_model_name)

# COMMAND ----------

# MAGIC %md #### Get source model version

# COMMAND ----------

src_version = src_client.get_model_version(src_model_name, src_model_version)
dump_obj(src_version)

# COMMAND ----------

description = description or src_version.description
aliases = src_version.aliases
if alias:
    aliases.append(alias)
print("description:",description)
print("aliases:",aliases)

# COMMAND ----------

# MAGIC %md #### Register model - create new model version

# COMMAND ----------

dst_version = copy_model_version(src_version, dst_model_name, src_client, dst_client)
dump_obj(dst_version)

# COMMAND ----------

# MAGIC %md #### Set model version metadata

# COMMAND ----------

# MAGIC %md ##### Set model version description

# COMMAND ----------

if description:
    dst_client.update_model_version(dst_model_name, dst_version.version, description)

# COMMAND ----------

# MAGIC %md ##### Set model version tags

# COMMAND ----------

for k,v in src_version.tags.items():
    print(f"Setting tag: key='{k}' value='{v}'")
    dst_client.set_model_version_tag(dst_version.name, dst_version.version, k, v)

# COMMAND ----------

# MAGIC %md ##### Set model version aliases

# COMMAND ----------

for alias in aliases:
    print(f"Setting alias '{alias}'")
    dst_client.set_registered_model_alias(dst_model_name, alias, dst_version.version)

# COMMAND ----------

# MAGIC %md ##### Set model version lineage tags

# COMMAND ----------

if set_model_version_lineage: ##
    print(f"Setting source model lineage tags '{TAG_LINEAGE_BASE}.*'")
    copy_model_version_lineage(dst_client, src_version, dst_version)

# COMMAND ----------

# MAGIC %md #### Display new model version

# COMMAND ----------

dst_version = dst_client.get_model_version(dst_model_name, dst_version.version)
dump_obj(dst_version)

# COMMAND ----------

dump_dict_as_json(dst_version.tags)

# COMMAND ----------

display_model_version_uri(dst_model_name, dst_version.version)

# COMMAND ----------

# MAGIC %md ### Result

# COMMAND ----------

keys = [ "name", "version", "run_id", "description", "aliases", "tags" ]
def subset(obj, keys):
    return { k[1:]:v for k,v in obj.__dict__.items() if k[1:] in keys }
result = {
    "src_model_version":  subset(src_version, keys),
    "dst_model_version":  subset(dst_version, keys)
}
dump_dict_as_json(result)

# COMMAND ----------

dbutils.notebook.exit(dict_as_json(result))
