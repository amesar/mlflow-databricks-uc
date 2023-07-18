# Databricks notebook source
# Common utilities

# COMMAND ----------

def assert_widget(value, name):
    if len(value.rstrip())==0:
        raise Exception(f"ERROR: '{name}' widget is required")

# COMMAND ----------

def dump_obj(obj, title="Object"):
    print(f"{title}:")
    for k,v in obj.__dict__.items():
        print(f"  {k[1:]}: {v}")

def dump_dct(dct, title="Dict"):
    print(f"{title}:")
    for k,v in dct.items():
        print(f"  {k}: {v}")

def dump_keys(dct, title="Dict"):
    print(f"{title}:")
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

import mlflow
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
    print("client.registry_uri:   ", client._registry_uri)
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

from mlflow.utils import databricks_utils
_host_name = databricks_utils.get_browser_hostname()
print("_host_name:", _host_name)

# COMMAND ----------

def display_registered_model_uri(model_name):
    if _host_name:
        if is_unity_catalog(model_name): # is unity catalog model
            model_name = model_name.replace(".","/")
            uri = f"https://{_host_name}/explore/data/models/{model_name}"
        else:
            uri = f"https://{_host_name}/#mlflow/models/{model_name}"
        displayHTML("""<b>Registered Model:</b> <a href="{}">{}</a>""".format(uri,uri))

# COMMAND ----------

def display_model_version_uri(model_name, version):
    if _host_name:
        if is_unity_catalog(model_name): # is unity catalog model
            model_name = model_name.replace(".","/")
            uri = f"https://{_host_name}/explore/data/models/{model_name}/version/{version}"
        else:
            uri = f"https://{_host_name}/#mlflow/models/{model_name}/versions/{version}"
        displayHTML("""<b>Model Version:</b> <a href="{}">{}</a>""".format(uri,uri))
