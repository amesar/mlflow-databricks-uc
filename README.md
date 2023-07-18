# MLflow Databricks Unity Catalog tools

#### Overview

Tools for Databricks Unity Catalog Model Registry:
* Migrate models from Workspace Model Registry to Unity Catalog Model Registry.
* Display and manipulate Unity Catalog models.
* Most of these notebooks will accept either UC or non-UC models especially for model copying. 
  * For example, you can copy a UC or non-UC model version to a target UC or non-UC model version.

#### Note
* This `README.md` is meant to be used outside a workspace. 
* If you are inside a workspace, use [notebooks/_README.py](notebooks/_README.py) in order for workspace links to work.

#### Databricks Notebooks
*  [README](notebooks/_README.py)
* [Register_Model](notebooks/Register_Model.py) - Register a new model - create new model version.
* [Copy_Model_Version](notebooks/Copy_Model_Version) - Creates a new model version from another model version.
* [Get_Registered_Model](notebooks/Get_Registered_Model.py) - Get registered model and its versions.
* [Get_Model_Version](notebooks/Get_Model_Version.py) - Get model version, its run and MLflow model.
* [Get_Model_Permissions](notebooks/Get_Model_Permissions.py) - Get permissions of a registered model
* [List_Registered_Models](notebooks/List_Registered_Models.py) - List registered models.
* [Set_Tag](notebooks/Set_Tag.py) - Set tag of registered model or model version.

#### Databricks Documentation

* Manage model lifecycle in Unity Catalog - [AWS](https://docs.databricks.com/machine-learning/manage-model-lifecycle/index.html) - [Azure](https://learn.microsoft.com/en-us/azure/databricks/machine-learning/manage-model-lifecycle/)
* Upgrade ML workflows and models to Unity Catalog - [AWS](https://docs.databricks.com/machine-learning/manage-model-lifecycle/upgrade-to-uc/index.html) - [Azure](https://learn.microsoft.com/en-us/azure/databricks/machine-learning/manage-model-lifecycle/upgrade-to-uc/)
* Upgrade ML workflows to target models in Unity Catalog - [AWS](https://docs.databricks.com/machine-learning/manage-model-lifecycle/upgrade-to-uc/upgrade-workflows.html) - [Azure](https://learn.microsoft.com/en-us/azure/databricks/machine-learning/manage-model-lifecycle/upgrade-to-uc/upgrade-workflows)

Last updated: 2023-07-18