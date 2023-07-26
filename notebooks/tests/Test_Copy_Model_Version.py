# Databricks notebook source
# MAGIC %md ## Test Copy_Model_Version
# MAGIC
# MAGIC **Legend**
# MAGIC * WS - workspace as in workspace model name: `Sklearn_Wine`
# MAGIC * UC - Unity Catalog as in UC model name: `my_catalog:mlmodels:sklearn_wine`
# MAGIC
# MAGIC **Note**
# MAGIC * Test data (model names and versions) is for e2-demo-west

# COMMAND ----------

# MAGIC %md #### Setup

# COMMAND ----------

from mlflow.utils import databricks_utils
import os

this_notebook = databricks_utils.get_notebook_path()
nb_dir = os.path.dirname(os.path.dirname(this_notebook))
nb_dir

# COMMAND ----------

nb = "Copy_Model_Version"
notebook = f"{nb_dir}/{nb}"
notebook

# COMMAND ----------

# MAGIC %md #### Initialize test data
# MAGIC
# MAGIC * Configure these values per your environment.
# MAGIC * TODO: Externalize with widgets

# COMMAND ----------

# e2-demo-west

uc_src_name = "andre_catalog.ml_models2.sklearn_wine_best"
uc_src_version = "1"
uc_dst_name = "andre_catalog.ml_models2.tmp"

ws_src_name = "Sklearn_Wine_best"
ws_src_version = "1"
ws_dst_name = "Sklearn_Wine_test"

ws_src_name_no_run = "andre_02a_Sklearn_Train_Predict"
ws_src_version_no_run = "11"

# COMMAND ----------

# MAGIC %md #### Test Harness

# COMMAND ----------

import json
def dump_dict(dct, sort_keys=None):
    print(json.dumps(dct, sort_keys=sort_keys, indent=2))

def dump_json(json_str):
    dct = json.loads(json_str)
    dump_dict(dct)

def to_json(dct):
    return json.dumps(dct)

def display_error(msg):
    displayHTML(f'<i><b><font color="red" size=+0 >{msg}</font></b></i>')

def display_ok(msg):
    displayHTML(f'<i><b><font color="#0000CD" size=+0 >{msg}</font></b></i>')

# COMMAND ----------

test_list = []

def run_test(test_name, params):
    print(f"Test: {test_name}")
    try:
        res = dbutils.notebook.run(notebook, 600, params)
        dump_json(res)
        msg = { "status": "OK", "test": test_name}
        display_ok(to_json(msg))
    except Exception as e:
        msg = { "status": "FAILED", "test": test_name}
        display_error(to_json(msg))
        print(f"ERROR: {e}")
    test_list.append(msg)

# COMMAND ----------

def mk_params(src_model_name, src_model_version, dst_model_name):
    return {
        "1. Source model name": src_model_name,
        "2. Source model version": src_model_version,
        "3. New model name": dst_model_name
    }

# COMMAND ----------

# MAGIC %md #### OK Tests

# COMMAND ----------

# MAGIC %md ##### Copy UC to UC
# MAGIC

# COMMAND ----------

# MAGIC %md ###### Note
# MAGIC
# MAGIC Fails if in `Common.copy_model_version` we do not set mlflow.set_registry_uri("databricks-uc") even though the client.registry_uri="databricks-uc"
# MAGIC
# MAGIC MlflowException: Unable to download model artifacts from source artifact location 'models:/andre_catalog.ml_models2.sklearn_wine_best/1' in order to upload them to Unity Catalog. Please ensure the source artifact location exists and that you can download from it via mlflow.artifacts.download_artifacts()

# COMMAND ----------

run_test("UC to UC copy", mk_params(uc_src_name, uc_src_version, uc_dst_name))

# COMMAND ----------

# MAGIC %md ##### Copy WS to UC

# COMMAND ----------

run_test("WS to UC copy", mk_params(ws_src_name, ws_src_version, uc_dst_name))

# COMMAND ----------

# MAGIC %md ##### Copy WS to WS

# COMMAND ----------

run_test("WS to WS copy", mk_params(ws_src_name, ws_src_version, ws_dst_name))

# COMMAND ----------

# MAGIC %md #### Failed Tests

# COMMAND ----------

# MAGIC %md ##### Copy WS to UC - deleted run
# MAGIC
# MAGIC Note: hard-deleted run.

# COMMAND ----------

run_test("UC to UC copy - deleted run", mk_params(ws_src_name_no_run, ws_src_version_no_run, uc_dst_name))

# COMMAND ----------

# MAGIC %md ### Test Report
# MAGIC
# MAGIC Note: all tests pass except test `UC to UC copy - deleted run`.

# COMMAND ----------

import pandas as pd
df = pd.DataFrame.from_dict(test_list)
df = df[["test", "status"]]
display(df)
