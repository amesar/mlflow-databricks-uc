# Databricks notebook source
# MAGIC %md ## Get Model Version
# MAGIC
# MAGIC Get a model version, its run and MLflow model.
# MAGIC
# MAGIC Widgets:
# MAGIC * `Model name` - example: my_catalog.ml_models.sklearn_wine
# MAGIC * `Model version`

# COMMAND ----------

# MAGIC %md #### Setup

# COMMAND ----------

# MAGIC %run ./Common

# COMMAND ----------

dbutils.widgets.text("Model name", "")
model_name = dbutils.widgets.get("Model name")

dbutils.widgets.text("Model version", "")
model_version = dbutils.widgets.get("Model version")

print("model_name:", model_name)
print("model_version:", model_version)

# COMMAND ----------

assert_widget(model_name, "Model name")
assert_widget(model_version, "Model version")

# COMMAND ----------

client = get_client(model_name)

# COMMAND ----------

# MAGIC %md #### Get model version

# COMMAND ----------

version = client.get_model_version(model_name, model_version)
dump_obj(version, "Model Version")

# COMMAND ----------

# MAGIC %md #### Get run

# COMMAND ----------

run = client.get_run(version.run_id)
dump_obj(run.info, "Run Info")

# COMMAND ----------

# MAGIC %md #### Get MLflow model metdata - `MLmodel` artifact aka `ModelInfo`
# MAGIC
# MAGIC Two ways:
# MAGIC 1. Get `MLmodel` artifact - more human-readable result
# MAGIC 2. Call `mlflow.models.get_model_info()` - less human-readable result

# COMMAND ----------

# MAGIC %md ##### 1. Get `MLmodel` artifact - more human-readable result

# COMMAND ----------

mlmodel = get_MLmodel_artifact(version.source)

# COMMAND ----------

dump_keys(mlmodel, "MLModel")

# COMMAND ----------

mlmodel

# COMMAND ----------

# MAGIC %md ##### 2. Call `mlflow.models.get_model_info()` - less human-readable result

# COMMAND ----------

model_uri = f"models:/{model_name}/{model_version}"
model_uri

# COMMAND ----------

model_info = mlflow.models.get_model_info(model_uri)
model_info

# COMMAND ----------

dump_keys(model_info.__dict__, "ModelInfo")

# COMMAND ----------

dump_obj(model_info)
