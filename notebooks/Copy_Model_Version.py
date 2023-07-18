# Databricks notebook source
# MAGIC %md ## Copy Registered Model Version
# MAGIC
# MAGIC **Overview**
# MAGIC * Creates a new model version from another model version. 
# MAGIC * Copies source version's metadata (description, tags and aliases) to target version.
# MAGIC * Option to overwrite description or add a new alias.
# MAGIC
# MAGIC **Widgets**
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

print("src_model_name:", src_model_name)
print("src_model_version:", src_model_version)
print("dst_model_name:", src_model_name)
print("alias:", alias)
print("description:", description)

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

dst_version = create_model_version(dst_client, 
    dst_model_name, 
    src_version.source, 
    src_version.run_id
)
dst_version

# COMMAND ----------

# MAGIC %md #### Set model version metadata

# COMMAND ----------

if description:
    dst_client.update_model_version(dst_model_name, dst_version.version, description)

# COMMAND ----------

for k,v in src_version.tags.items():
    print(f"Setting tag: key='{k}' value='{v}'")
    dst_client.set_model_version_tag(dst_version.name, dst_version.version, k, v)

# COMMAND ----------

for alias in aliases:
    print(f"Setting alias '{alias}'")
    dst_client.set_registered_model_alias(dst_model_name, alias, dst_version.version)

# COMMAND ----------

# MAGIC %md #### Display new model version

# COMMAND ----------

dst_version = dst_client.get_model_version(dst_model_name, dst_version.version)
dump_obj(dst_version)

# COMMAND ----------

display_model_version_uri(dst_model_name, dst_version.version)