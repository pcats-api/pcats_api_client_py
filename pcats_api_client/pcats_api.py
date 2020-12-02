import requests
import sys
import numpy as np
from numpy import savetxt
import time

def _url(path):
    return 'https://pcats.research.cchmc.org' + path

def job_status(jobid):
    res=requests.get(_url('/api/job/{}/status'.format(jobid)))
    if res.status_code==200:
        res_json = res.json()
        if 'status' in res_json:
            return res_json['status']
    return None


def wait_for_result(jobid):
    while True:
        status = job_status(jobid)
        if status is None or status=="Error":
            return "Error"
        if status=="Done":
            return status
        time.sleep(5)

def ret_jobid(res):
    if res.status_code==200:
        res_json = res.json()
        if 'jobid' in res_json:
            return res_json['jobid'][0]
    return None

def staticgp(dataurl, outcome, treatment, x_explanatory=None, x_confounding=None,
             tr_hte=None, tr2_values=None,
             burn_num=500, mcmc_num=500, outcome_type="Continuous", 
             outcome_lb=None, outcome_ub=None,
             outcome_bound_censor="neither",
             outcome_censor_yn=None,
             outcome_censor_lv=None,
             outcome_censor_uv=None,
             outcome_link="identity",
             tr_type="Discrete",
             tr2_type="Discrete",             
             pr_values=None,
             method="BART",
             x_categorical=None,
             mi_dataurl=None):

    data={
        'data': (dataurl, open(dataurl, 'rb')),
        'outcome': (None, outcome),
        'treatment': (None, treatment),
        'x.explanatory': (None, x_explanatory),
        'x.confounding': (None, x_confounding),
        'tr.hte': (None, tr_hte),
        'tr2.values': (None, tr2_values),
        'burn.num': (None, burn_num),
        'mcmc.num': (None, mcmc_num),
        'outcome.lb': (None, outcome_lb),
        'outcome.ub': (None, outcome_ub),
        'outcome.bound_censor': (None, outcome_bound_censor),
        'outcome.censor.yn': (None, outcome_censor_yn),
        'outcome.censor.lv': (None, outcome_censor_lv),
        'outcome.censor.uv': (None, outcome_censor_uv),
        'outcome.type': (None, outcome_type),
        'outcome.link': (None, outcome_link),
        'pr.values': (None, pr_values),
        'tr.type': (None, tr_type),
        'tr2.type': (None, tr2_type),
        'method': (None, method),
        'x.categorical': (None, x_categorical),
        'mi.data':  (mi_dataurl, open(mi_dataurl, 'rb')
                     if mi_dataurl!=None else None )}

    res=requests.post(_url('/api/staticgp'), files=data);
    return ret_jobid(res)

def print(jobid):
    return requests.get(_url(
        '/api/job/{}/print'.format(jobid))).content.decode("utf-8") 

def staticgp_cate(jobid, x, control_tr, treat_tr, pr_values=None):
    data={
        'x': (None, x),
        'control.tr': (None, control_tr),
        'treat.tr': (None, treat_tr),
        'pr.values': (None, pr_values)}

    res=requests.post(_url(
        '/api/job/{}/staticgp.cate'.format(jobid)), files=data);
    return ret_jobid(res)

def _printCATE(jobid):
    return requests.get(_url(
        '/api/job/{}/printCATE'.format(jobid))).content.decode("utf-8") 


def dynamicgp(dataurl, stg1_outcome, stg1_treatment, 
              stg2_outcome, stg2_treatment,
              stg1_x_explanatory=None, stg1_x_confounding=None,
              stg1_tr_hte=None, stg1_tr_values=None, stg1_outcome_type="Continuous",
              stg1_tr_type="Discrete",
              stg1_outcome_lb=None, stg1_outcome_ub=None,
              stg1_outcome_bound_censor="neither", stg1_outcome_censor_yn=None,
              stg1_outcome_censor_lv=None, stg1_outcome_censor_uv=None,
              stg1_outcome_link="identity", stg1_pr_values=None,
              stg2_x_explanatory=None, stg2_x_confounding=None,
              stg2_tr_hte=None, stg2_tr_values=None, stg2_outcome_type="Continuous",
              stg2_tr_type="Discrete",
              stg2_outcome_lb=None, stg2_outcome_ub=None,
              stg2_outcome_bound_censor="neither", stg2_outcome_censor_yn=None,
              stg2_outcome_censor_lv=None, stg2_outcome_censor_uv=None,
              stg2_outcome_link="identity",stg2_pr_values=None,
              burn_num=500, mcmc_num=500,
              method="BART",
              x_categorical=None,
              mi_dataurl=None):

    data={
        'data': (dataurl, open(dataurl, 'rb')),
        'stg1.outcome': (None, stg1_outcome),
        'stg1.treatment': (None, stg1_treatment),
        'stg1.x.explanatory': (None, stg1_x_explanatory),
        'stg1.x.confounding': (None, stg1_x_confounding),
        'stg1.tr.hte': (None, stg1_tr_hte),
        'stg1.tr.values': (None, stg1_tr_values),
        'stg1.outcome.lb': (None, stg1_outcome_lb),
        'stg1.outcome.ub': (None, stg1_outcome_ub),
        'stg1.outcome.bound_censor': (None, stg1_outcome_bound_censor),
        'stg1.outcome.censor.lv': (None, stg1_outcome_censor_lv),
        'stg1.outcome.censor.uv': (None, stg1_outcome_censor_uv),
        'stg1.outcome.link': (None, stg1_outcome_link),
        'stg1.outcome.censor.yn': (None, stg1_outcome_censor_yn),
        'stg1.outcome.type': (None, stg1_outcome_type),
        'stg1.tr.type': (None, stg1_tr_type),
        'stg1.pr.values': (None, stg1_pr_values),
        'stg2.outcome': (None, stg2_outcome),
        'stg2.treatment': (None, stg2_treatment),
        'stg2.x.explanatory': (None, stg2_x_explanatory),
        'stg2.x.confounding': (None, stg2_x_confounding),
        'stg2.tr.hte': (None, stg2_tr_hte),
        'stg2.tr.values': (None, stg2_tr_values),
        'stg2.outcome.lb': (None, stg2_outcome_lb),
        'stg2.outcome.ub': (None, stg2_outcome_ub),
        'stg2.outcome.bound_censor': (None, stg2_outcome_bound_censor),
        'stg2.outcome.censor.lv': (None, stg2_outcome_censor_lv),
        'stg2.outcome.censor.uv': (None, stg2_outcome_censor_uv),
        'stg2.outcome.link': (None, stg2_outcome_link),
        'stg2.outcome.censor.yn': (None, stg2_outcome_censor_yn),
        'stg2.outcome.type': (None, stg2_outcome_type),
        'stg2.tr.type': (None, stg2_tr_type),
        'stg2.pr.values': (None, stg2_pr_values),
        'burn.num': (None, burn_num),
        'mcmc.num': (None, mcmc_num),
        'x.categorical': (None, x_categorical),
        'method': (None, method),
        'mi.data':  (mi_dataurl, open(mi_dataurl, 'rb') if mi_dataurl!=None else None )}

    res=requests.post(_url('/api/dynamicgp'), files=data);
    return ret_jobid(res)