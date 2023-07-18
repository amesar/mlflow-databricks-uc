# Databricks notebook source
# MAGIC %md # MLflow Databricks Unity Catalog Notebooks
# MAGIC
# MAGIC #### Overview
# MAGIC
# MAGIC Tools for the Databricks Unity Catalog Model Registry:
# MAGIC * Migrate models from Workspace Model Registry to Unity Catalog Model Registry.
# MAGIC * Display and manipulate Unity Catalog models.
# MAGIC * Most of these notebooks will accept either UC or non-UC models especially for model copying. 
# MAGIC   * For example, you can copy a UC or non-UC model version to a target UC or non-UC model version.
# MAGIC
# MAGIC #### Notebooks
# MAGIC * [Register_Model]($Register_Model) - Register a new model version from a run.
# MAGIC * [Copy_Model_Version]($Copy_Model_Version) - Creates a new model version from another model version.
# MAGIC * [Get_Registered_Model]($Get_Registered_Model) - Get registered model and its versions.
# MAGIC * [Get_Model_Version]($Get_Model_Version) - Get model version, its run and MLflow model.
# MAGIC * [Get_Model_Permissions]($Get_Model_Permissions) - Get permissions of a registered model
# MAGIC * [List_Registered_Models]($List_Registered_Models) - List registered models.
# MAGIC * [Set_Tag]($Set_Tag) - Set tag of registered model or model version.
# MAGIC * [Common]($Common) - Common utilities.
# MAGIC
# MAGIC Last updated: 2023-07-18
