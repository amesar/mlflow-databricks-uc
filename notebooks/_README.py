# Databricks notebook source
# MAGIC %md # MLflow Databricks Unity Catalog Notebooks
# MAGIC
# MAGIC #### Overview
# MAGIC
# MAGIC Tools for the Databricks Unity Catalog Model Registry:
# MAGIC * Migrate models from Workspace Model Registry to Unity Catalog Model Registry.
# MAGIC * Display and manipulate Unity Catalog models.
# MAGIC * Most of these notebooks will accept either UC or non-UC models especially for model copying. 
# MAGIC   * For example, you can either copy a UC or non-UC model version to a new UC or non-UC model version.
# MAGIC
# MAGIC #### Notebooks
# MAGIC
# MAGIC ##### Create Model Version notebooks
# MAGIC * [Create_Model_Version_from_Version]($Create_Model_Version_from_Version) - Create a model version from another model version. Copy a version in its entirety (model and version metadata) to another version.
# MAGIC * [Create_Model_Version_from_Run]($Create_Model_Version_from_Run) - Create a new model version from a run. This is the canonical way to register a new model (version) from a run's MLflow model.
# MAGIC * [Create_Model_Version_from_Version_Advanced]($Create_Model_Version_from_Version_Advanced)
# MAGIC * [Create_Model_Version_from_URI]($Create_Model_Version_from_URI) - Create a model version from a model URI. Can be any model URI `models:/my-model/1`, `runs:/123` or other.
# MAGIC
# MAGIC ##### Other notebooks
# MAGIC * [Get_Registered_Model]($Get_Registered_Model) - Get registered model and its versions.
# MAGIC * [Get_Model_Version]($Get_Model_Version) - Get model version, its run and MLflow model.
# MAGIC * [Get_Model_Permissions]($Get_Model_Permissions) - Get permissions of a registered model
# MAGIC * [List_Registered_Models]($List_Registered_Models) - List registered models.
# MAGIC * [Set_Tag]($Set_Tag) - Set tag of registered model or model version.
# MAGIC * [Common]($Common) - Common utilities.
# MAGIC
# MAGIC Last updated: 2023-07-25
