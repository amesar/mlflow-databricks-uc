# Databricks notebook source
# Common utilities

# COMMAND ----------

import mlflow
non_uc_client = mlflow.MlflowClient(registry_uri="databricks")
uc_client = mlflow.MlflowClient(registry_uri="databricks-uc")
client = non_uc_client

# COMMAND ----------

def show_clients():
    print("mlflow.registry_uri:", mlflow.get_registry_uri())
    print("non_uc_client:", non_uc_client._registry_uri)
    print("uc_client:    ", uc_client._registry_uri)
    print("client:       ", client._registry_uri)
show_clients()

# COMMAND ----------

def use_unity_catalog(use_uc):
    global client
    if use_uc:
        client = uc_client
        mlflow.set_registry_uri("databricks-uc")
    else:
        client = non_uc_client
        mlflow.set_registry_uri("databricks")
    print("New client.registry:    ", client._registry_uri)
    print("New mlflow.registry.uri:", mlflow.get_registry_uri())

# COMMAND ----------

use_unity_catalog(True)

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
