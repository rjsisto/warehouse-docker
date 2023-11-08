import papermill as pm
import os

#os.chdir("notebooks")
pm.execute_notebook("data_preprocess.ipynb", None)
pm.execute_notebook("model_build.ipynb", None)
