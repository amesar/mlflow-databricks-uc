# Databricks notebook source
# MAGIC %md ## Create Model Version from another Model Version - Advanced
# MAGIC
# MAGIC **Overview**
# MAGIC * Creates a new model version from another model version. 
# MAGIC * Option to use as the source model either: 
# MAGIC   * Version's run MLflow model 
# MAGIC   * Version's registry MLflow model 
# MAGIC * Copies source version's metadata (description, tags and aliases) to new version.
# MAGIC * Option to overwrite description or add a new alias.
# MAGIC
# MAGIC **Widgets**
# MAGIC * `1. Source model name` - example: `andre_catalog.ml_models.sklearn_wine`
# MAGIC * `2. Source model version` 
# MAGIC * `3. New model name` 
# MAGIC * `4. Alias` - alias to append to source version aliases
# MAGIC * `5. Description` - replace source version description if specified
# MAGIC * `6. Copy MLflow model from` - source of MLflow model to copy:
# MAGIC   * `Run` - create model version from source version's run MLflow model
# MAGIC   * `Registry` - create model version from source version's registry MLflow model
# MAGIC   * `If Run fails then try Registry` - If `Run` method fails (deleted run or corrupted model), fall back to copying from the registry model.

# COMMAND ----------

# MAGIC %md 
# MAGIC
# MAGIC #### Discussion on widget "`6. Copy MLflow model from`"
# MAGIC   
# MAGIC **Run** 
# MAGIC
# MAGIC * Copies MLflow model from the source version run model artifact. 
# MAGIC * This corresponds to the standard way of creating a new model version   directly from the run ("register model").
# MAGIC * The process creates a "well-formed" model version with correct lineage to the run. The fields (`version.source` and `version.run_id` correctly point to their run values.
# MAGIC * The run's MLflow model is copied to the model registry's storage area which is DBFS for the workspace registry but a UC location for UC registry.
# MAGIC * A model version therefore points to two MLflow models:
# MAGIC    * "Run model" - in run's workspace DBFS. This is the model source of truth for the Model Version UI where the `Source Run` link points to.
# MAGIC    * "Registry model" - in registry's storage location. This is the source of truth when you retrieve a model for scoring from the registry with `models:/mymodel/12`.
# MAGIC * This create process can fail for two reasons:
# MAGIC    * The run has been deleted (hard-deleted) 
# MAGIC    * The MLflow model artifact has been corrupted. Either the native model is corrupeted (e.g. model.pkl) or the MLModel file is invalid. 
# MAGIC * There is no referential integrity constraint between the model version and its originating run. You can delete a run that is being used by a (production) model version without warning. Or you can overwrite the run MLflow model so now it differs from the registry MLflow model.
# MAGIC  
# MAGIC  __Registry__
# MAGIC  * Copy the MLflow model from the source model version's "registry run". 
# MAGIC * This method guarantees that the canonical registry model will be copied.
# MAGIC * But it will not be "well-formed" since the `version.source` and `version.run_id` fields will not be empty.
# MAGIC
# MAGIC __If Run fails then try Registry__
# MAGIC * If the standard `Run` create method fails, fall back to trying the `Registry` method.

# COMMAND ----------

# MAGIC %md #### Setup

# COMMAND ----------

# MAGIC %run ./Common

# COMMAND ----------

RUN = "Run"
REGISTRY = "Registry"
RUN_THEN_REGISTRY = "If Run fails then try Registry"

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

dbutils.widgets.dropdown("6. Copy MLflow model from", RUN, [RUN, REGISTRY, RUN_THEN_REGISTRY])
copy_model_from = dbutils.widgets.get("6. Copy MLflow model from")

print("src_model_name:", src_model_name)
print("src_model_version:", src_model_version)
print("dst_model_name:", src_model_name)
print("alias:", alias)
print("description:", description)
print("copy_model_from:", copy_model_from)

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
dump_obj(src_version, "Source Model Version")

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

# MAGIC %md **If run does not exist**
# MAGIC
# MAGIC error_code: INTERNAL_ERROR
# MAGIC
# MAGIC MlflowException: Model version creation failed for model name: Sklearn_Wine_test version: 16 with status: FAILED_REGISTRATION and message: Failed registration. The given source path `dbfs:/databricks/mlflow-tracking/e090757fcb8f49cb9822f65f2fe7ed91/3c0b2decc41c4dc0becd3d60bc814a4d/artifacts/model` does not exist.

# COMMAND ----------

if copy_model_from == REGISTRY:
    display_bold(f"Creating model version from source registry MLflow model without run")
    dst_version = register_with_version_download_uri(src_client, src_model_name, src_model_version)
else:
    try:
        dst_version = create_model_version(dst_client, 
            dst_model_name, 
            src_version.source, 
            src_version.run_id
        )
        display_bold("Created model version from registry model without run")
    except mlflow.MlflowException as e: # Run doesn't exist. error_code: INTERNAL_ERROR
        if copy_model_from == RUN_THEN_REGISTRY:
            display_error(f"WARNING: Run '{src_version.run_id}' does not exist. error_code: {e.error_code}\n") 
            display_bold(f"Creating model version from source registry MLflow model without run")
            dst_version = register_with_version_download_uri(src_client, src_model_name, src_model_version)
        else:
            display_error(f"ERROR: Run '{src_version.run_id}' does not exist. error_code: {e.error_code}\n") 
            raise e
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
dump_obj(dst_version, "New Model Version")

# COMMAND ----------

if not dst_version.run_id:
    display_error(f"WARNING: New model version {dst_version.version} does not have a run_id")

# COMMAND ----------

display_model_version_uri(dst_model_name, dst_version.version)
