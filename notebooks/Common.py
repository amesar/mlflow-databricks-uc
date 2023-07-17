# Databricks notebook source
# Common utilities

# COMMAND ----------

import mlflow
non_uc_client = mlflow.MlflowClient(registry_uri="databricks")
uc_client = mlflow.MlflowClient(registry_uri="databricks-uc")
client = non_uc_client

# COMMAND ----------

def show_clients():
    print("mlflow.get_registry_uri:", mlflow.get_registry_uri())
    print("non_uc_client:", non_uc_client._registry_uri)
    print("uc_client:    ", uc_client._registry_uri)
    print("client:       ", client._registry_uri)
show_clients()

# COMMAND ----------

def use_unity_catalog(use_uc):
    global client
    client = uc_client if use_uc else non_uc_client
    print("New client:", client._registry_uri)
