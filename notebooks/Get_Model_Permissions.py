# Databricks notebook source
# MAGIC %md ## Get Model Permissions
# MAGIC
# MAGIC Get registered model permissions. 
# MAGIC
# MAGIC Since open-source MLflow does not have registered model permissions we need to use a Databricks Unity Catalog API.
# MAGIC
# MAGIC **Widgets**
# MAGIC * `Model name` - example: my_catalog.ml_models.sklearn_wine
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %md #### Registered Model Permissions API Documentation
# MAGIC
# MAGIC **UC Registered Model Permissions API**
# MAGIC
# MAGIC See more invocation examples: [Unity Catalog Registered Model Permissions](https://databricks.atlassian.net/wiki/spaces/UN/pages/1280411724/MLflow+FAQ#Unity-Catalog-Registered-Model-Permissions) Databricks wiki page.
# MAGIC
# MAGIC REST API
# MAGIC * [2.1/unity-catalog/permissions](https://docs.databricks.com/api/workspace/grants/get) 
# MAGIC * [2.1/unity-catalog/effective-permissions](https://docs.databricks.com/api/workspace/grants/geteffective)
# MAGIC
# MAGIC Python SDK
# MAGIC * [GrantsAPI.get](https://databricks-sdk-py.readthedocs.io/en/latest/workspace/grants.html#GrantsAPI.get) 
# MAGIC * [GrantsAPI.get_effective](https://databricks-sdk-py.readthedocs.io/en/latest/workspace/grants.html#GrantsAPI.get_effective) 
# MAGIC
# MAGIC **Non-UC Registered Model Permissions API**
# MAGIC * [permissions/registered-models/{model_id}/permissionLevels](https://docs.databricks.com/api/workspace/permissions/getpermissionlevels)
# MAGIC * [permissions/registered-models/{model_id}](https://docs.databricks.com/api/workspace/permissions/get)
# MAGIC * [databricks/registered-models/get](https://docs.databricks.com/api/workspace/modelregistry/getmodel) - need returned `model_id` to call above two methods

# COMMAND ----------

# MAGIC %md #### SDK Setup
# MAGIC
# MAGIC Until DBR comes with SDK 0.1.12 bu default, you need to manually install it 0.1.12 order to use WorkspaceClient() with a no-arg constructor.

# COMMAND ----------

# MAGIC %pip install -U databricks-sdk==0.1.12

# COMMAND ----------

dbutils.library.restartPython()

# COMMAND ----------

from databricks import sdk
sdk.version.__version__

# COMMAND ----------

# MAGIC %md #### Setup widget

# COMMAND ----------

# MAGIC %run ./Common

# COMMAND ----------

dbutils.widgets.text("Model name", "")
model_name = dbutils.widgets.get("Model name")

# COMMAND ----------

assert_widget(model_name, "Model name")

# COMMAND ----------

# MAGIC %md #### Create SDK client

# COMMAND ----------

from databricks.sdk import WorkspaceClient
sdk_client = WorkspaceClient()
sdk_client

# COMMAND ----------

# MAGIC %md #### Get model permissions
# MAGIC
# MAGIC Note there is no `Catalog.SecurableType.MODEL`, so we use `Catalog.SecurableType.FUNCTION`.

# COMMAND ----------


from databricks.sdk.service import catalog

perms = sdk_client.grants.get(catalog.SecurableType.FUNCTION, model_name)
perms

# COMMAND ----------

# MAGIC %md #### Get model effective permissions

# COMMAND ----------

grants = sdk_client.grants.get_effective(catalog.SecurableType.FUNCTION, model_name)
grants

# COMMAND ----------

import json
jperms = json.dumps(grants.as_dict(),indent=2)
print(jperms)
