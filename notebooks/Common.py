# Databricks notebook source
# ==== Common utilities

# COMMAND ----------

import mlflow
from mlflow.exceptions import MlflowException, RestException
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

def dump_obj(obj, title=None):
    title = title or type(obj).__name__
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

def dump_dict_as_json(dct, sort_keys=None):
    import json
    print(json.dumps(dct, sort_keys=sort_keys, indent=2))

def dict_as_json(dct, sort_keys=None):
    import json
    return json.dumps(dct, sort_keys=sort_keys, indent=2)

# COMMAND ----------

# Create a model version from a run


# COMMAND ----------

def create_model_version(client,  model_name, source_uri, run_id=None):
    try:
       client.create_registered_model(model_name)
    except RestException as e:
       client.get_registered_model(model_name)
    return client.create_model_version(model_name, source_uri, run_id=run_id)

# COMMAND ----------

# === Get appropriate client 

# COMMAND ----------

_non_uc_client = mlflow.MlflowClient(registry_uri="databricks")
_uc_client = mlflow.MlflowClient(registry_uri="databricks-uc")

# COMMAND ----------

def is_unity_catalog(name):
    return len(name.split(".")) == 3
    
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

# ==== Display functions

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

# ==== Convert to dict

# COMMAND ----------

import copy
def registered_model_to_dict(model):
    dct = copy.deepcopy(model.__dict__)
    if model.latest_versions is not None:
        dct["_latest_versions"] = [ vr.__dict__ for vr in model.latest_versions ]
    dct.pop("_latest_version",None)
    return dct

# COMMAND ----------

# ==== Copy Model Version

# COMMAND ----------

def _copy_model_version(src_version, dst_model_name, src_client, dst_client, use_download_uri=False):
    try:
        dst_client.create_registered_model(dst_model_name)
    except MlflowException as e:
        if e.error_code != "RESOURCE_ALREADY_EXISTS":
            print(f"ERROR: error_code: {e.error_code}")
            raise 
        
    if use_download_uri:
        src_uri = src_client.get_model_version_download_uri(src_version.name, src_version.version)
    else:
        src_uri = f"models:/{src_version.name}/{src_version.version}"
    print(f"Creating new version for model '{dst_model_name}' from '{src_uri}' with run_id '{src_version.run_id}'")
    
    try:
        return dst_client.create_model_version(source=src_uri, name=dst_model_name, run_id=src_version.run_id)
    except MlflowException as e:
        print(f"ERROR: error_code: {e.error_code}")
        raise 

# COMMAND ----------

def copy_model_version(src_version, dst_model_name, src_client, dst_client):
    """
    Create model version from the source version's registry MLflow model.
    """
    src_is_uc = is_unity_catalog(src_version.name)
    dst_is_uc = is_unity_catalog(dst_model_name)
    ori_registry_uri = mlflow.get_registry_uri()
    mlflow.set_registry_uri(dst_client._registry_uri) # NOTE: If not set, fails for UC to UC copy

    # UC to UC
    if src_is_uc and dst_is_uc:
        vr= _copy_model_version(src_version, dst_model_name, src_client, dst_client)

    # non-UC to UC
    elif not src_is_uc and dst_is_uc:
        vr = _copy_model_version(src_version, dst_model_name, src_client, dst_client, use_download_uri=True)
   
    # non-UC to non-UC - fails
    else:
        print(f"WARNING: Creating version from run MLflow model instead of registry MLflow model due to non-UC to non-UC bug.")
        vr = create_model_version(dst_client, dst_model_name, src_version.source, src_version.run_id)
    
    mlflow.set_registry_uri(ori_registry_uri)
    return vr

# COMMAND ----------

# Get model version utils

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

# == Source model lineage

# COMMAND ----------

current_user = dbutils.notebook.entry_point.getDbutils().notebook().getContext().tags().get("user").get()

# COMMAND ----------

TAG_LINEAGE_BASE = "_mlflow_lineage.source_model_version"
TAG_SOURCE_MODEL_NAME = f"{TAG_LINEAGE_BASE}.name"
TAG_SOURCE_MODEL_VERSION = f"{TAG_LINEAGE_BASE}.version"
TAG_SOURCE_MODEL_COPY_USER = f"{TAG_LINEAGE_BASE}.user"
TAG_SOURCE_MODEL_COPY_TIME = f"{TAG_LINEAGE_BASE}.copy_time"
TAG_SOURCE_MODEL_COPY_TIME_NICE = f"{TAG_LINEAGE_BASE}.copy_time_nice"

# COMMAND ----------

import time
TS_FORMAT = "%Y-%m-%d %H:%M:%S"
utc_now_seconds = time.time()
utc_now_millis = round(utc_now_seconds*1000)
utc_now_nice = time.strftime(TS_FORMAT, time.gmtime(utc_now_seconds))
#utc_now_seconds, utc_now_nice

# COMMAND ----------

def copy_model_version_lineage(dst_client, src_version, dst_version):
    dst_client.set_model_version_tag(dst_version.name, dst_version.version, 
        TAG_SOURCE_MODEL_NAME, src_version.name)
    dst_client.set_model_version_tag(dst_version.name, dst_version.version, 
        TAG_SOURCE_MODEL_VERSION, src_version.version)
    dst_client.set_model_version_tag(dst_version.name, dst_version.version, 
        TAG_SOURCE_MODEL_COPY_USER, current_user)
    dst_client.set_model_version_tag(dst_version.name, dst_version.version, 
        TAG_SOURCE_MODEL_COPY_TIME, utc_now_millis)
    dst_client.set_model_version_tag(dst_version.name, dst_version.version, 
        TAG_SOURCE_MODEL_COPY_TIME_NICE, utc_now_nice)

# COMMAND ----------


