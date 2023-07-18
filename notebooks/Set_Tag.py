# Databricks notebook source
# MAGIC %md ## Set tag of registered model or model version
# MAGIC
# MAGIC Sets a tag for either a registered model or model version.
# MAGIC
# MAGIC **Widgets**
# MAGIC * `1. Registered Model` - required.
# MAGIC * `2. Model Version` - if set model version tag is set. If not set, registeree model tag is set.
# MAGIC * `3. Tag key`
# MAGIC * `3. Tag value`

# COMMAND ----------

# MAGIC %run ./Common

# COMMAND ----------

dbutils.widgets.text("1. Registered Model", "")
model_name = dbutils.widgets.get("1. Registered Model")

dbutils.widgets.text("2. Model Version", "")
model_version = dbutils.widgets.get("2. Model Version")

dbutils.widgets.text("3. Tag key", "")
tag_key = dbutils.widgets.get("3. Tag key")

dbutils.widgets.text("4. Tag value", "")
tag_value = dbutils.widgets.get("4. Tag value")

print("model_name:", model_name)
print("model_version:", model_version)
print("tag_key:", tag_key)
print("tag_value:", tag_value)

# COMMAND ----------

assert_widget(model_name, "Missing '1. Registered Model' widget")
assert_widget(tag_key, "Missing '3. Tag key")

# COMMAND ----------

    display_registered_model_uri(model_name)

# COMMAND ----------

if model_version:
    display_model_version_uri(model_name, model_version)

# COMMAND ----------

client = get_client(model_name)

# COMMAND ----------

if model_version:
    client.set_model_version_tag(model_name, model_version, tag_key, tag_value)
    vr = client.get_model_version(model_name, model_version)
    print(vr.tags)

# COMMAND ----------

if not model_version:
    client.set_registered_model_tag(model_name, tag_key, tag_value)
    model = client.get_registered_model(model_name)
    print(model.tags)
