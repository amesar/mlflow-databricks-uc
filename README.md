# MLflow Databricks Unity Catalog tools

Tools for Databricks Unity Catalog Model Registry.

#### Overview

* Migrate models from Workspace Model Registry to Unity Catalog Model Registry.
* Copy and create model versions. 
  * Copy a workspace model version to a UC model version.
  * Copy a UC model version to another UC model version, e.g. promote model from "staging" to "prod" catalog.
  * Create a model version from an MLflow run.
* Tools to display and manipulate Unity Catalog models.
* For the most part, notebooks accept workspace model names besides UC model names.

#### Note
* This `README.md` is meant to be used __outside__ a workspace (links are public github links). 
* If you are __inside__ a workspace, use [notebooks/_README.py](notebooks/_README.py) in order for workspace links to work.

#### Databricks Notebooks

[README](notebooks/_README.py) - README for notebooks 

##### Create Model Version notebooks
* [Copy_Model_Version ](notebooks/Copy_Model_Version .py) - Creates a model version from another model version. 
  * Copy a version in its entirety (model and version metadata) to another version.
* [Create_Model_Version](notebooks/Create_Model_Version.py) - Create a new model version from a run. 
  * This is the canonical way to register a new model (version) from a run's MLflow model.

##### Other Notebooks
* [Get_Registered_Model](notebooks/Get_Registered_Model.py) - Get registered model and its versions.
* [Get_Model_Version](notebooks/Get_Model_Version.py) - Get model version, its run and MLflow model.
* [Get_Model_Permissions](notebooks/Get_Model_Permissions.py) - Get permissions of a registered model
* [List_Registered_Models](notebooks/List_Registered_Models.py) - List registered models.
* [Set_Tag](notebooks/Set_Tag.py) - Set tag of registered model or model version.
* [Experimental notebooks](experimental/_README.py).

##### Test Notebooks
* [Test notebooks](tests).

#### Databricks Documentation

* Manage model lifecycle in Unity Catalog - [AWS](https://docs.databricks.com/machine-learning/manage-model-lifecycle/index.html) - [Azure](https://learn.microsoft.com/en-us/azure/databricks/machine-learning/manage-model-lifecycle/)
* Upgrade ML workflows and models to Unity Catalog - [AWS](https://docs.databricks.com/machine-learning/manage-model-lifecycle/upgrade-to-uc/index.html) - [Azure](https://learn.microsoft.com/en-us/azure/databricks/machine-learning/manage-model-lifecycle/upgrade-to-uc/)
* Upgrade ML workflows to target models in Unity Catalog - [AWS](https://docs.databricks.com/machine-learning/manage-model-lifecycle/upgrade-to-uc/upgrade-workflows.html) - [Azure](https://learn.microsoft.com/en-us/azure/databricks/machine-learning/manage-model-lifecycle/upgrade-to-uc/upgrade-workflows)

Last updated: 2023-07-26