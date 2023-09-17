# Databricks notebook source
# MAGIC %md ## Copy a Model Version
# MAGIC
# MAGIC **Overview**
# MAGIC * Copy one model version to another. 
# MAGIC * Uses the version's registry MLflow model run and not the source version run MLflow model.
# MAGIC * Copies source version's metadata (description, tags and aliases) to target version.
# MAGIC
# MAGIC **Widgets**
# MAGIC * `1. Source model name` - example: `andre_catalog.ml_models.sklearn_wine`
# MAGIC * `2. Source model version` 
# MAGIC * `3. New model name` 
# MAGIC * `4. Set model version lineage` - Option to save the following source version tags:
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

dbutils.widgets.dropdown("4. Set model version lineage", "no", ["yes","no"])
set_model_version_lineage = dbutils.widgets.get("4. Set model version lineage") == "yes"

print("src_model_name:", src_model_name)
print("src_model_version:", src_model_version)
print("dst_model_name:", src_model_name)
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

# MAGIC %md #### Create new model version

# COMMAND ----------

dst_version = copy_model_version(src_version, dst_model_name, src_client, dst_client)
dump_obj(dst_version)

# COMMAND ----------

# MAGIC %md #### Set model version lineage tags

# COMMAND ----------

if set_model_version_lineage:
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
dbutils.notebook.exit(dict_as_json(result))
