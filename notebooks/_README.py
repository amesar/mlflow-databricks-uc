# Databricks notebook source
# MAGIC %md # MLflow Databricks Unity Catalog Notebooks
# MAGIC
# MAGIC Notebooks for the new Databricks Unity Catalog (UC) Model Registry feature.
# MAGIC
# MAGIC #### Overview
# MAGIC * Notebooks to migrate models from Workspace Model Registry to Unity Catalog Model Registry.
# MAGIC * Notebooks to copy and create model versions. 
# MAGIC   * Copy a workspace registry model version to a UC model version.
# MAGIC   * Copy a UC model version to another UC model version, e.g. promote model from "staging" to "prod" catalog.
# MAGIC   * Create a model version from an MLflow run.
# MAGIC * Tools to display and manipulate Unity Catalog models.
# MAGIC * For the most part, notebooks accept workspace model names as well UC model names.
# MAGIC
# MAGIC #### Notebooks
# MAGIC
# MAGIC ##### Copy/Create Model Version notebooks
# MAGIC * [Copy_Model_Version]($Copy_Model_Version) - Copy one model version to another. 
# MAGIC   * Copy a version in its entirety (model and version metadata) to another version.
# MAGIC * [Create_Model_Version]($Create_Model_Version) - Create a new model version from a run. 
# MAGIC   * This is the standard way to register a brand new model version from scratch.
# MAGIC
# MAGIC ##### MLflow Management Notebooks
# MAGIC * [Get_Registered_Model]($Get_Registered_Model) - Get registered model and its versions.
# MAGIC * [Get_Model_Version]($Get_Model_Version) - Get model version, its run and MLflow model.
# MAGIC * [Get_Model_Permissions]($Get_Model_Permissions) - Get permissions of a registered model
# MAGIC * [List_Registered_Models]($List_Registered_Models) - List registered models.
# MAGIC * [Set_Tag]($Set_Tag) - Set tag of registered model or model version.
# MAGIC
# MAGIC ##### Other Notebooks
# MAGIC * [Common]($Common) - Common utilities notebook.
# MAGIC * [Experimental notebooks]($experimental/_README).
# MAGIC
# MAGIC ##### Test notebooks
# MAGIC * [Test notebooks]($tests/_README).
# MAGIC
# MAGIC #### Git Repo
# MAGIC * https://github.com/amesar/mlflow-databricks-uc
# MAGIC
# MAGIC Last updated: 2023-10-02
