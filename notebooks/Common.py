# Databricks notebook source
# Common utilities

# COMMAND ----------

import mlflow
from mlflow.utils import databricks_utils
_host_name = databricks_utils.get_browser_hostname()
print(f"MLflow version: {mlflow.__version__}")
print(f"Databricks runtime: {databricks_utils.get_databricks_runtime()}")

# COMMAND ----------

def mk_dbfs_path(path):
    return path.replace("/dbfs","dbfs:")

def mk_local_path(path):
    return path.replace("dbfs:","/dbfs")

# COMMAND ----------

def assert_widget(value, name):
    if len(value.rstrip())==0:
        raise Exception(f"ERROR: '{name}' widget is required")

# COMMAND ----------

def dump_obj(obj, title="Object"):
    print(f"{title}:")
    if obj:
        for k,v in obj.__dict__.items():
            print(f"  {k[1:]}: {v}")

def dump_dct(dct, title="Dict"):
    print(f"{title}:")
    if  dct:
        for k,v in dct.items():
            print(f"  {k}: {v}")

def dump_keys(dct, title="Dict"):
    print(f"{title}:")
    if dct:
        for k in dct.keys():
            print(f"  {k}")

def dump_json(dct, sort_keys=None):
    import json
    print(json.dumps(dct, sort_keys=sort_keys, indent=2))

# COMMAND ----------

import yaml
from mlflow.utils.file_utils import TempDir
from mlflow.artifacts import download_artifacts

def get_MLmodel_artifact(model_uri, artifact_path="MLmodel"):
    with TempDir() as tmp:
        artifact_uri = f"{model_uri}/{artifact_path}"
        local_path = download_artifacts(artifact_uri=artifact_uri, dst_path=tmp.path())
        with open(local_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

# COMMAND ----------

from mlflow.exceptions import RestException

def create_model_version(client,  model_name, source_uri, run_id=None):
    try:
       client.create_registered_model(model_name)
    except RestException as e:
       client.get_registered_model(model_name)
    return client.create_model_version(model_name, source_uri, run_id=run_id)

# COMMAND ----------

# Client code

# COMMAND ----------

_non_uc_client = mlflow.MlflowClient(registry_uri="databricks")
_uc_client = mlflow.MlflowClient(registry_uri="databricks-uc")
client = _non_uc_client

# COMMAND ----------

def is_unity_catalog(model_name):
    return "." in model_name
    
def _get_client(model_name):
    return _uc_client if is_unity_catalog(model_name) else _non_uc_client

# COMMAND ----------

def get_client_uc(use_uc):
    client = _uc_client if use_uc else _non_uc_client
    mlflow.set_registry_uri(client._registry_uri)
    print("client.registry_uri:    ", client._registry_uri)
    print("mlflow.get_registry_uri:", mlflow.get_registry_uri())
    return client

# COMMAND ----------

def get_client(model_name):
    client = _get_client(model_name)
    mlflow.set_registry_uri(client._registry_uri)
    print("client.registry_uri:    ", client._registry_uri)
    print("mlflow.get_registry_uri:", mlflow.get_registry_uri())
    return client

# COMMAND ----------

def get_clients(src_model_name, dst_model_name):
    src_client = _get_client(src_model_name)
    dst_client = _get_client(dst_model_name)
    print("src_client.registry_uri:", src_client._registry_uri)
    print("dst_client.registry_uri:", dst_client._registry_uri)
    return src_client, dst_client

# COMMAND ----------

def display_registered_model_uri(model_name):
    if _host_name: # if not running as job
        if is_unity_catalog(model_name): # is unity catalog model
            model_name = model_name.replace(".","/")
            uri = f"https://{_host_name}/explore/data/models/{model_name}"
        else:
            uri = f"https://{_host_name}/#mlflow/models/{model_name}"
        displayHTML(f'<b>Registered Model UI:</b> <a href="{uri}">{uri}</a>')

# COMMAND ----------

def display_model_version_uri(model_name, version):
    if _host_name: # if not running as job
        if is_unity_catalog(model_name): # is unity catalog model
            model_name = model_name.replace(".","/")
            uri = f"https://{_host_name}/explore/data/models/{model_name}/version/{version}"
        else:
            uri = f"https://{_host_name}/#mlflow/models/{model_name}/versions/{version}"
        displayHTML(f'<b>Model Version UI:</b> <a href="{uri}">{uri}</a>')

# COMMAND ----------

def display_error(msg):
    if _host_name: # if not running as job
        displayHTML(f'<i><b><font color="red" size=+0 >{msg}</font></b></i>')
    else:
        print(msg)

def display_bold(msg):
    if _host_name: # if not running as job
        displayHTML(f'<i><b><font size=+0 >{msg}</font></b></i>')
    else:
        print(msg)

# COMMAND ----------

# Experimental
# Should work but fails.

# MlflowException: Model version creation failed for model name: Sklearn_Wine_test version: 52 with status: FAILED_REGISTRATION and message: Failed registration. The given source path `dbfs:/databricks/mlflow-registry/3a5e115117914dd0bf09b85c4a4e48ad/models/sklearn-model` does not exist.

def _register_with_version_download_uri(client, model_name, model_version):
    artifact_uri = client.get_model_version_download_uri(model_name, model_version) 
    return mlflow.register_model(artifact_uri, dst_model_name)

# COMMAND ----------

# Experimental
"""
Since we can't register using the value of model_version_download_uri (see above)
jump through some hoops by:
  1. Download the model to DBFS /tmp directory
  2. Use this temp directory to register the model

Caveats:
  1. run_id will be not be set obviously
  2. version "source" field will be invalid as it refers to temporary directory
"""

_tmp_download_dir = "/dbfs/tmp"

def register_with_version_download_uri(client, model_name, model_version):
    from distutils.dir_util import copy_tree
    import tempfile
    artifact_uri = client.get_model_version_download_uri(model_name, model_version) 
    with tempfile.TemporaryDirectory(dir=_tmp_download_dir) as tmp_dir:
        local_dir = download_artifacts(artifact_uri=artifact_uri, dst_path=tmp_dir)
        copy_tree(local_dir, mk_local_path(tmp_dir))
        print(f"Registering model '{dst_model_name}' again from version download URI '{artifact_uri}'")
        return mlflow.register_model(mk_dbfs_path(tmp_dir), dst_model_name)
