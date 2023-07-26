# Databricks notebook source
# MAGIC %md # MLflow Databricks Unity Catalog Notebooks
# MAGIC
# MAGIC Tools for Databricks Unity Catalog Model Registry.
# MAGIC
# MAGIC #### Overview
# MAGIC
# MAGIC * Migrate models from Workspace Model Registry to Unity Catalog Model Registry.
# MAGIC * Copy and create model versions. 
# MAGIC   * Copy a workspace model version to a UC model version.
# MAGIC   * Copy a UC model version to another UC model version, e.g. promote model from "staging" to "prod" catalog.
# MAGIC   * Copy a model version from an MLflow run.
# MAGIC * Tools to display and manipulate Unity Catalog models.
# MAGIC * For the most part, notebooks accept workspace model names besides UC model names.
# MAGIC
# MAGIC #### Notebooks
# MAGIC
# MAGIC ##### Create Model Version notebooks
# MAGIC * [Create_Model_Version_from_Version]($Create_Model_Version_from_Version) - Create a model version from another model version. 
# MAGIC   * Copy a version in its entirety (model and version metadata) to another version.
# MAGIC * [Create_Model_Version_from_Run]($Create_Model_Version_from_Run) - Create a new model version from a run. 
# MAGIC   * This is the standard way to register a new model version.
# MAGIC
# MAGIC ##### Other notebooks
# MAGIC * [Get_Registered_Model]($Get_Registered_Model) - Get registered model and its versions.
# MAGIC * [Get_Model_Version]($Get_Model_Version) - Get model version, its run and MLflow model.
# MAGIC * [Get_Model_Permissions]($Get_Model_Permissions) - Get permissions of a registered model
# MAGIC * [List_Registered_Models]($List_Registered_Models) - List registered models.
# MAGIC * [Set_Tag]($Set_Tag) - Set tag of registered model or model version.
# MAGIC * [Common]($Common) - Common utilities.
# MAGIC * [Experimental notebooks]($experimental/_README).
# MAGIC
# MAGIC Last updated: 2023-07-25
