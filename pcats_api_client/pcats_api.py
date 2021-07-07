import requests
import sys
import time

def _url(path):
    return 'https://pcats.research.cchmc.org' + path

def job_status(jobid):
    """Returns the `jobid` status.

    Parameters
    ----------
    jobid : UUID
            The job id identifier
            
    Returns
    -------
    string
        Status of the `jobid` computation.

    """

    if jobid is None:
        return "Error"
    res=requests.get(_url('/api/job/{}/status'.format(jobid)))
    if res.status_code==200:
        res_json = res.json()
        if 'status' in res_json:
            return res_json['status']
    return None


def wait_for_result(jobid):
    """
    Parameters
    ----------
    jobid : UUID
            The job id identifier
    """
    if jobid is None:
        return "Error"
    while True:
        status = job_status(jobid)
        if status is None or status.startswith("Error"):
            return "Error"
        if status=="Done":
            return status
        time.sleep(5)

def ret_jobid(res):
    if res.status_code==200:
        res_json = res.json()
        if 'jobid' in res_json:
            return res_json['jobid']
    return None

def staticgp(datafile=None,
             dataref=None,
             method="BART",
             outcome=None,
             outcome_type="Continuous", 
             outcome_bound_censor="neither",
             outcome_lb=None,
             outcome_ub=None,
             outcome_censor_yn=None,
             outcome_censor_lv=None,
             outcome_censor_uv=None,
             outcome_link="identity",
             treatment=None, 
             x_explanatory=None,
             x_confounding=None,
             tr_type="Discrete",
             tr2_type="Discrete",             
             tr_values=None,
             tr2_values=None,
             pr_values=None,
             tr_hte=None,
             tr2_hte=None,
             burn_num=500,
             mcmc_num=500,
             x_categorical=None,
             mi_datafile=None,
             mi_dataref=None,
             sheet=None,
             mi_sheet=None,
             seed=5000,
             token=None,
             use_cache=None,
             reuse_cached_jobid=None):
    """
    Parameters
    ----------
    datafile : something
            something
    dataref : something
            something
    """

    data={
        'data': (datafile, open(datafile, 'rb') if datafile!=None else None ),
        'dataref': (None, dataref),
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
        'outcome.type': (None, outcome_type),
        'outcome.censor.lv': (None, outcome_censor_lv),
        'outcome.censor.uv': (None, outcome_censor_uv),
        'outcome.censor.yn': (None, outcome_censor_yn),
        'outcome.link': (None, outcome_link),
        'tr.type': (None, tr_type),
        'tr2.type': (None, tr2_type),
        'tr.values': (None, tr_values),
        'tr2.values': (None, tr2_values),
        'pr.values': (None, pr_values),
        'x.categorical': (None, x_categorical),
        'method': (None, method),
        'mi.data':  (mi_datafile, open(mi_datafile, 'rb')
                     if mi_datafile!=None else None ),
        'mi.dataref': (None, mi_dataref),
        'sheet': (None, sheet),
        'mi.sheet': (None, mi_sheet),
        'seed': (None, seed)
        }

    headers=dict()
    if (str(use_cache)=="1"):
        headers["X-API-Cache"]="1"
    if (str(reuse_cached_jobid)=="1"):
        headers["X-API-Reuse-Cached-Jobid"]="1"

    res=requests.post(_url('/api/staticgp'), files=data, headers=headers);
    return ret_jobid(res)

def print(jobid):
    """Returns printable representation of the results.

    Parameters
    ----------
    jobid : UUID
            The job id identifier
            
    Returns
    -------
    string
        Printable representations of the `jobid` computation.

    """

    return requests.get(_url(
        '/api/job/{}/print'.format(jobid))).content.decode("utf-8") 

def results(jobid):
    """Returns JSON representation of the results.

    Parameters
    ----------
    jobid : UUID
            The job id identifier
            
    Returns
    -------
    string
        Printable representations of the `jobid` computation.

    """

    return requests.get(_url(
        '/api/job/{}/results'.format(jobid))).content.decode("utf-8") 

def staticgp_cate(jobid, 
              x, 
              control_tr, 
              treat_tr, 
              pr_values=None,
              use_cache=None,
              reuse_cached_jobid=None):
    """Returns printable representation of the results.

    Parameters
    ----------
    jobid : UUID
            The job id identifier
    x : UUID
            The job id identifier
    control_tr : UUID
            The job id identifier
    treat_tr : UUID
            The job id identifier
            
    Returns
    -------
    string
        Printable representations of the `jobid` computation.

    """
    data={
        'x': (None, x),
        'control.tr': (None, control_tr),
        'treat.tr': (None, treat_tr),
        'pr.values': (None, pr_values)}

    headers=dict()
    if (str(use_cache)=="1"):
        headers["X-API-Cache"]="1"
    if (str(reuse_cached_jobid)=="1"):
        headers["X-API-Reuse-Cached-Jobid"]="1"

    res=requests.post(_url(
        '/api/job/{}/staticgp.cate'.format(jobid)), files=data, headers=headers);
    return ret_jobid(res)

def _printCATE(jobid):
    return requests.get(_url(
        '/api/job/{}/printCATE'.format(jobid))).content.decode("utf-8") 


def dynamicgp(datafile=None,
              dataref=None,
              method="BART",

              stg1_outcome=None,
              stg1_treatment=None, 
              stg1_x_explanatory=None,
              stg1_x_confounding=None,
              stg1_tr_hte=None,
              stg1_tr_values=None,
              stg1_tr_type="Discrete",
              stg1_outcome_type="Continuous",
              stg1_outcome_bound_censor="neither",
              stg1_outcome_lb=None,
              stg1_outcome_ub=None,
              stg1_outcome_censor_lv=None,
              stg1_outcome_censor_uv=None,
              stg1_outcome_censor_yn=None,
              stg1_outcome_link="identity",
              stg1_pr_values=None,

              stg2_outcome=None,
              stg2_treatment=None,
              stg2_x_explanatory=None,
              stg2_x_confounding=None,
              stg2_tr1_hte=None,
              stg2_tr2_hte=None,
              stg2_tr_values=None,
              stg2_tr_type="Discrete",
              stg2_outcome_type="Continuous",
              stg2_outcome_bound_censor="neither",
              stg2_outcome_lb=None,
              stg2_outcome_ub=None,
              stg2_outcome_censor_lv=None,
              stg2_outcome_censor_uv=None,
              stg2_outcome_censor_yn=None,
              stg2_outcome_link="identity",
              stg2_pr_values=None,

              burn_num=500,
              mcmc_num=500,
              x_categorical=None,
              mi_datafile=None,
              mi_dataref=None,
              sheet=None,
              mi_sheet=None,
              seed=5000,
              token=None,
              use_cache=None,
              reuse_cached_jobid=None):

    data={
        'data': (datafile, open(datafile, 'rb') if datafile!=None else None ),
        'dataref': (None, dataref),
        'stg1.outcome': (None, stg1_outcome),
        'stg1.treatment': (None, stg1_treatment),
        'stg1.x.explanatory': (None, stg1_x_explanatory),
        'stg1.x.confounding': (None, stg1_x_confounding),
        'stg1.tr.hte': (None, stg1_tr_hte),
        'stg1.tr.values': (None, stg1_tr_values),
        'stg1.tr.type': (None, stg1_tr_type),
        'stg1.outcome.type': (None, stg1_outcome_type),
        'stg1.outcome.bound_censor': (None, stg1_outcome_bound_censor),
        'stg1.outcome.lb': (None, stg1_outcome_lb),
        'stg1.outcome.ub': (None, stg1_outcome_ub),
        'stg1.outcome.censor.lv': (None, stg1_outcome_censor_lv),
        'stg1.outcome.censor.uv': (None, stg1_outcome_censor_uv),
        'stg1.outcome.censor.yn': (None, stg1_outcome_censor_yn),
        'stg1.outcome.link': (None, stg1_outcome_link),
        'stg1.pr.values': (None, stg1_pr_values),
        'stg2.outcome': (None, stg2_outcome),
        'stg2.treatment': (None, stg2_treatment),
        'stg2.x.explanatory': (None, stg2_x_explanatory),
        'stg2.x.confounding': (None, stg2_x_confounding),
        'stg2.tr1.hte': (None, stg2_tr1_hte),
        'stg2.tr2.hte': (None, stg2_tr2_hte),
        'stg2.tr.values': (None, stg2_tr_values),
        'stg2.tr.type': (None, stg2_tr_type),
        'stg2.outcome.type': (None, stg2_outcome_type),
        'stg2.outcome.bound_censor': (None, stg2_outcome_bound_censor),
        'stg2.outcome.lb': (None, stg2_outcome_lb),
        'stg2.outcome.ub': (None, stg2_outcome_ub),
        'stg2.outcome.censor.lv': (None, stg2_outcome_censor_lv),
        'stg2.outcome.censor.uv': (None, stg2_outcome_censor_uv),
        'stg2.outcome.censor.yn': (None, stg2_outcome_censor_yn),
        'stg2.outcome.link': (None, stg2_outcome_link),
        'stg2.pr.values': (None, stg2_pr_values),
        'burn.num': (None, burn_num),
        'mcmc.num': (None, mcmc_num),
        'x.categorical': (None, x_categorical),
        'method': (None, method),
        'mi.data':  (mi_datafile, open(mi_datafile, 'rb') if mi_datafile!=None else None ),
        'mi.dataref': (None, mi_dataref),
        'sheet': (None, sheet),
        'mi.sheet': (None, mi_sheet),
        'seed': (None, seed)
        }

    headers=dict()
    if (str(use_cache)=="1"):
        headers["X-API-Cache"]="1"
    if (str(reuse_cached_jobid)=="1"):
        headers["X-API-Reuse-Cached-Jobid"]="1"

    res=requests.post(_url('/api/dynamicgp'), files=data, headers=headers);
    return ret_jobid(res)

def dynamicgp_cate(jobid, 
              x, 
              control_tr, 
              treat_tr, 
              pr_values=None,
              use_cache=None,
              reuse_cached_jobid=None):
    data={
        'x': (None, x),
        'control.tr': (None, control_tr),
        'treat.tr': (None, treat_tr),
        'pr.values': (None, pr_values)}

    headers=dict()
    if (str(use_cache)=="1"):
        headers["X-API-Cache"]="1"
    if (str(reuse_cached_jobid)=="1"):
        headers["X-API-Reuse-Cached-Jobid"]="1"

    res=requests.post(_url(
        '/api/job/{}/dynamicgp.cate'.format(jobid)), files=data, headers=headers);
    return ret_jobid(res)

def uploadfile(datafile):
    data={
        'data': (datafile, open(datafile, 'rb') if datafile!=None else None ),
        }

    res=requests.post(_url('/api/uploadfile'), files=data);
    if res.status_code==200:
        res_json = res.json()
        if 'fileref' in res_json:
            return res_json['fileref']
    return None

def ploturl(jobid,plottype=None):
    if plottype!=None:
        plottype="/{}".format(plottype)
    else:
        plottype=""
    res=requests.get(_url(
        '/api/job/{}/ploturl'.format(jobid))).content.decode("utf-8") 
    if res.status_code==200:
        res_json = res.json()
        if 'url' in res_json:
            return "{}{}".format(res_json['url'],plottype)
    return None
