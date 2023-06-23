"""
PCATS: Bayesian Causal Inference for General Type of Treatment

The PCATS application programming interface (API) implements two Bayesian's non parametric causal inference modeling, Bayesian's Gaussian process regression and Bayesian additive regression tree, and provides estimates of averaged causal treatment (ATE) and conditional averaged causal treatment (CATE) for adaptive or non-adaptive treatment. The API is able to handle general types of treatment - binary, multilevel, continuous and their combinations, as well as general type of outcomes including bounded summary scores such as health related quality of life and survival outcomes. In addition, the API is able to deal with missing data using user supplied multiply imputed missing data. Summary tables and interactive figures of the results are generated and downloadable.

"""

from .pcats_api import job_status, staticgp, dynamicgp, uploadfile, wait_for_result, printgp, ploturl, staticgp_cate, dynamicgp_cate, results

from .pcats_api_staticgp2 import staticgp2
