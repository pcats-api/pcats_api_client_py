import requests
import sys
import time

def _url(path):
    return 'https://pcats.research.cchmc.org' + path

def job_status(jobid):
    """Return job status.

    Return status of the previously submitted job

    Parameters
    ----------
    jobid : UUID
            Job ID of the previously submitted job

    Returns
    -------
    string
        status

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
    """Wait while the job status is pending

    Return when the job status is finished (either successfully or otherwise)

    Parameters
    ----------
    jobid : UUID
            Job ID of the previously submitted job

    Returns
    -------
    string
        status
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
             tr_values=None,
             c_margin=None,
             tr_hte=None,
	         time=None,
	         time_value=None,
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
    """Performs a data analysis for data with non-adaptive treatment(s).

      Bayesian's Gaussian process regression or Bayesian additive regression tree for data with non-adaptive treatment(s).

    Parameters
    ----------
    datafile File to upload (.csv or .xls)
    dataref Reference to already uploaded file.
    method The method to be used. "GP" for GP method and "BART" for BART method. The default value is "BART".
    outcome The name of the outcome variable.
    outcome.type Outcome type ("Continuous" or "Discrete"). The default value is "Continuous".
    outcome.bound_censor The default value is "neither".
          "neither" if the outcome is not bounded or censored.
          "bounded" if the outcome is bounded.
          "censored" if the outcome is censored.
    outcome.lb Putting a lower bound if the outcome is bounded.
    outcome.ub Putting a upper bound if the outcome is bounded.
    outcome.censor.yn Censoring variable if outcome is censored.
    outcome.censor.lv lower variable of censored interval if outcome is censored.
    outcome.censor.uv upper variable of censored interval if outcome is censored.
    outcome.link function for outcome; the default value is "identity".
          "identity" if no transformation needed.
          "log" for log transformation.
          "logit" for logit transformation.
    treatment The vector of the name of the treatment variables. Users can input at most two treatment variables.
    x.explanatory The vector of the name of the explanatory variables.
    x.confounding The vector of the name of the confounding variables.
    tr.type The type of the first treatment. "Continuous" for continuous treatment and "Discrete" for categorical treatment. The default value is "Discrete".
    tr.values user-defined values for the calculation of ATE if the first treatment variable is continuous
    c.margin An optional vector of user-defined values of c for PrTE.
    tr.hte An optional vector specifying variables which may have heterogeneous treatment effect with the first treatment variable
    time
    time.value
    burn.num numeric; the number of MCMC 'burn-in' samples, i.e. number of MCMC to be discarded. The default value is 500.
    mcmc.num numeric; the number of MCMC samples after 'burn-in'. The default value is 500.
    x.categorical A vector of the name of categorical variables in data.
    mi.datafile File to upload (.csv or .xls) that contains the imputed data in the model.
    mi.dataref Reference to already uploaded file that contains the imputed data in the model.
    sheet If \code{datafile} or \code{dataref} points to an Excel file this variable specifies which sheet to load.
    mi.sheet If \code{mi.datafile} or \code{mi.dataurl} points to an Excel file this variable specifies which sheet to load.
    seed Sets the seed. The default value is 5000.
    token Authentication token.
    use_cache Use cached results (default True).


    Returns
    -------
    UUID
        jobid
    """

    data={
        'data': (datafile, open(datafile, 'rb') if datafile!=None else None ),
        'dataref': (None, dataref),
        'outcome': (None, outcome),
        'treatment': (None, treatment),
        'x.explanatory': (None, x_explanatory),
        'x.confounding': (None, x_confounding),
        'tr.hte': (None, tr_hte),
        'time': (None, time),
        'time.value': (None, time_value),
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
        'tr.values': (None, tr_values),
        'c.margin': (None, c_margin),
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
    elif (str(use_cache)=="0"):
        headers["X-API-Cache"]="0"

    if (str(reuse_cached_jobid)=="1"):
        headers["X-API-Reuse-Cached-Jobid"]="1"
    elif (str(reuse_cached_jobid)=="0"):
        headers["X-API-Reuse-Cached-Jobid"]="0"

    if token is not None:
        headers["Authorization"]="Bearer {}".format(token)

    res=requests.post(_url('/api/staticgp'), files=data, headers=headers);
    return ret_jobid(res)

def printgp(jobid,
            token=None):
    """Print job results

   Return formatted string with job results

    Parameters
    ----------
    jobid : UUID
            Job ID of the previously submitted job
    token : string
            Authentication token.
            
    Returns
    -------
    string
        formatted text

    """

    headers=dict()
    if token is not None:
        headers["Authorization"]="Bearer {}".format(token)

    return requests.get(_url(
        '/api/job/{}/print'.format(jobid)),
        headers=headers).content.decode("utf-8") 

def results(jobid,
            token=None):
    """Return job results

    Return job results

    Parameters
    ----------
    jobid : UUID
            Job ID of the previously submitted job
    token : string
            Authentication token.
            
    Returns
    -------
    json
        results

    """

    headers=dict()
    if token is not None:
        headers["Authorization"]="Bearer {}".format(token)

    return requests.get(_url(
        '/api/job/{}/results'.format(jobid)),
        headers=headers).content.decode("utf-8") 

def staticgp_cate(jobid, 
              x, 
              control_tr, 
              treat_tr, 
              c_margin=None,
              token=None,
              use_cache=None,
              reuse_cached_jobid=None):
    """Get conditional average treatment effect

    Estimate the conditional average treatment effect of user-specified treatment groups.

    The contrast of potential outcomes for the reference group and the treatment group is estimated at each value of x.

    The conditional average treatment effect is estimated based on the sample data. The observations with missing covariates in the model are excluded. For the unspecified variables in the model, the original data is used to estimate the conditional average treatment effect.

    Parameters
    ----------
    jobid job id of the "staticGP".
    x The name of a categorical variable which may have the heterogeneous treatment effect.
    control.tr The value of the treatment variable as the reference group.
    treat.tr The value of the treatment variable compared to the reference group.
    c.margin An optional vector of user-defined values of c for PrCTE.
    token Authentication token.
    use_cache Use cached results (default True).

    Returns
    -------
    UUID
        jobid

    """
    data={
        'x': (None, x),
        'control.tr': (None, control_tr),
        'treat.tr': (None, treat_tr),
        'c.margin': (None, c_margin)}

    headers=dict()
    if (str(use_cache)=="1"):
        headers["X-API-Cache"]="1"
    if (str(reuse_cached_jobid)=="1"):
        headers["X-API-Reuse-Cached-Jobid"]="1"

    if token is not None:
        headers["Authorization"]="Bearer {}".format(token)

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
              stg1_time=None,
              stg1_time_value=None,
              stg1_outcome_type="Continuous",
              stg1_outcome_bound_censor="neither",
              stg1_outcome_lb=None,
              stg1_outcome_ub=None,
              stg1_outcome_censor_lv=None,
              stg1_outcome_censor_uv=None,
              stg1_outcome_censor_yn=None,
              stg1_outcome_link="identity",
              stg1_c_margin=None,

              stg2_outcome=None,
              stg2_treatment=None,
              stg2_x_explanatory=None,
              stg2_x_confounding=None,
              stg2_tr1_hte=None,
              stg2_tr2_hte=None,
              stg2_tr_values=None,
              stg2_tr_type="Discrete",
              stg2_time=None,
              stg2_time_value=None,
              stg2_outcome_type="Continuous",
              stg2_outcome_bound_censor="neither",
              stg2_outcome_lb=None,
              stg2_outcome_ub=None,
              stg2_outcome_censor_lv=None,
              stg2_outcome_censor_uv=None,
              stg2_outcome_censor_yn=None,
              stg2_outcome_link="identity",
              stg2_c_margin=None,

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
    """Performs a data analysis for data with adaptive treatments.

    Performs Bayesian's Gaussian process regression or Bayesian additive regression tree for data with adaptive treatment(s).

    Parameters
    ----------
    datafile File to upload (.csv or .xls)
    dataref Reference to already uploaded file.
    method The method to be used. "GP" for GP method and "BART" for BART method. The default value is "BART".
    stg1.outcome The name of the intermediate outcome variable for stage 1.
    stg1.treatment The name of the treatment variable for stage 1.
    stg1.x.explanatory A vector of the name of the explanatory variables for stage 1.
    stg1.x.confounding A vector of the name of the confounding variables for stage 1.
    stg1.tr.hte An optional vector specifying categorical variables which may have heterogeneous treatment effect with the treatment variable for stage 1.
    stg1.time
    stg1.time.value
    stg1.outcome.bound_censor The default value is "neither".
        "neither" if the intermediate outcome is not bounded or censored.
        "bounded" if the intermediate outcome is bounded.
        "censored" if the intermediate outcome is censored.
    stg1.outcome.lb Stage 1 lower bound if the intermediate outcome is bounded.
    stg1.outcome.ub Stage 1 upper bound if the intermediate outcome is bounded.
    stg1.outcome.type Intermediate outcome type ("Continuous" or "Discrete") for stage 1.
    stg1.outcome.censor.yn Censoring variable if the intermediate outcome is censored.
    stg1.outcome.censor.lv lower variable of censored interval if the intermediate outcome is censored.
    stg1.outcome.censor.uv upper variable of censored interval if the intermediate outcome is censored.
    stg1.outcome.link function for the intermediate outcome; the default value is ``identity''.
        "identity" if no transformation needed.
        "log" for log transformation.
        "logit" for logit transformation.
    stg1.tr.values User-defined values for the calculation of ATE if the treatment variable is continuous for stage 1.
    stg1.tr.type The type of treatment at stage 1. "Continuous" for continuous treatment and "Discrete" for categorical treatment. The default value is "Discrete".
    stg1.c.margin An optional vector of user-defined values of c for PrTE at stage 1.
    stg2.outcome The name of the outcome variable for stage 2.
    stg2.treatment The name of the treatment variable for stage 2.
    stg2.x.explanatory A vector of the name of the explanatory variables for stage 2.
    stg2.x.confounding A vector of the name of the confounding variables for stage 2.
    stg2.tr1.hte At stage 2, an optional vector specifying cate-gorical variables which may have heterogeneoustreatment effect with the stage 1 treatment variable
    stg2.tr2.hte At stage 2, an optional vector specifying cate-gorical variables which may have heterogeneoustreatment effect with the stage 2 treatment variable
    stg2.time
    stg2.time.value
    stg2.outcome.bound_censor The default value is "neither".
        "neither" if the intermediate outcome is not bounded or censored.
        "bounded" if the intermediate outcome is bounded.
        "censored" if the intermediate outcome is censored.
    stg2.outcome.lb Stage 2 lower bound if the outcome is bounded.
    stg2.outcome.ub Stage 2 upper bound if the outcome is bounded.
    stg2.outcome.type Outcome type ("Continuous" or "Discrete") for stage 2.
    stg2.outcome.censor.yn Censoring variable if the outcome is censored.
    stg2.outcome.censor.lv lower variable of censored interval if the outcome is censored.
    stg2.outcome.censor.uv upper variable of censored interval if the outcome is censored.
    stg2.outcome.link function for the outcome; the default value is ``identity''.
        "identity" if no transformation needed.
        "log" for log transformation.
        "logit" for logit transformation.
    stg2.tr.values User-defined values for the calculation of ATE if the treatment variable is continuous for stage 2.
    stg2.tr.type The type of treatment at stage 2. "Continuous" for continuous treatment and "Discrete" for categorical treatment. The default value is "Discrete".
    stg2.c.margin An optional vector of user-defined values of c for PrTE at stage 2.
    burn.num numeric; the number of MCMC 'burn-in' samples, i.e. number of MCMC to be discarded. The default value is 500.
    mcmc.num numeric; the number of MCMC samples after 'burn-in'. The default value is 500.
    x.categorical A vector of the name of categorical variables in data.
    mi.datafile File to upload (.csv or .xls) that contains the imputed data in the model.
    mi.dataref Reference to already uploaded file that contains the imputed data in the model.
    sheet If \code{datafile} or \code{dataref} points to an Excel file this variable specifies which sheet to load.
    mi.sheet If \code{mi.datafile} or \code{mi.dataurl} points to an Excel file this variable specifies which sheet to load.
    seed Sets the seed. The default value is 5000.
    token Authentication token.
    use_cache Use cached results (default True).

    Returns
    -------
    UUID
        jobid

    """

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
        'stg1.time': (None, stg1_time),
        'stg1.time.value': (None, stg1_time_value),
        'stg1.outcome.type': (None, stg1_outcome_type),
        'stg1.outcome.bound_censor': (None, stg1_outcome_bound_censor),
        'stg1.outcome.lb': (None, stg1_outcome_lb),
        'stg1.outcome.ub': (None, stg1_outcome_ub),
        'stg1.outcome.censor.lv': (None, stg1_outcome_censor_lv),
        'stg1.outcome.censor.uv': (None, stg1_outcome_censor_uv),
        'stg1.outcome.censor.yn': (None, stg1_outcome_censor_yn),
        'stg1.outcome.link': (None, stg1_outcome_link),
        'stg1.c.margin': (None, stg1_c_margin),
        'stg2.outcome': (None, stg2_outcome),
        'stg2.treatment': (None, stg2_treatment),
        'stg2.x.explanatory': (None, stg2_x_explanatory),
        'stg2.x.confounding': (None, stg2_x_confounding),
        'stg2.tr1.hte': (None, stg2_tr1_hte),
        'stg2.tr2.hte': (None, stg2_tr2_hte),
        'stg2.tr.values': (None, stg2_tr_values),
        'stg2.tr.type': (None, stg2_tr_type),
        'stg2.time': (None, stg2_time),
        'stg2.time.value': (None, stg2_time_value),
        'stg2.outcome.type': (None, stg2_outcome_type),
        'stg2.outcome.bound_censor': (None, stg2_outcome_bound_censor),
        'stg2.outcome.lb': (None, stg2_outcome_lb),
        'stg2.outcome.ub': (None, stg2_outcome_ub),
        'stg2.outcome.censor.lv': (None, stg2_outcome_censor_lv),
        'stg2.outcome.censor.uv': (None, stg2_outcome_censor_uv),
        'stg2.outcome.censor.yn': (None, stg2_outcome_censor_yn),
        'stg2.outcome.link': (None, stg2_outcome_link),
        'stg2.c.margin': (None, stg2_c_margin),
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
    elif (str(use_cache)=="0"):
        headers["X-API-Cache"]="0"

    if (str(reuse_cached_jobid)=="1"):
        headers["X-API-Reuse-Cached-Jobid"]="1"
    elif (str(reuse_cached_jobid)=="0"):
        headers["X-API-Reuse-Cached-Jobid"]="0"
    if token is not None:
        headers["Authorization"]="Bearer {}".format(token)

    res=requests.post(_url('/api/dynamicgp'), files=data, headers=headers);
    return ret_jobid(res)

def dynamicgp_cate(jobid, 
              x, 
              control_tr, 
              treat_tr, 
              c_margin=None,
              token=None,
              use_cache=None,
              reuse_cached_jobid=None):
    """Get conditional average treatment effect for data with two time points.

    Estimate the conditional average treatment effect of user-specified treatment groups.

    The contrast of potential outcomes for the reference group and the treatment group is estimated at a list of x values if x is not a factor. If x is a factor, the conditional average treatment effect is estimated at each value of levels of x.

    The conditional average treatment effect is estimated based on the sample data. The observations with missing covariates in the model are excluded. For the unspecified variables in the model, the observed data is used to estimate the conditional average treatment effect.

    Parameters
    ----------
    jobid job id of the "dynamicGP".
    x The name of variable which may have the heterogeneous treatment effect. x should be a categorical variable.
    control.tr A vector of the values of the treatment variables at all stages as the reference group.
    treat.tr A vector of the values of the treatment variables at all stages compared to the reference group.
    c.margin An optional vector of user-defined values of c for PrCTE.
    token Authentication token.
    use_cache Use cached results (default True).

    Returns
    -------
    UUID
        jobid

    """
    data={
        'x': (None, x),
        'control.tr': (None, control_tr),
        'treat.tr': (None, treat_tr),
        'c.margin': (None, c_margin)}

    headers=dict()
    if (str(use_cache)=="1"):
        headers["X-API-Cache"]="1"
    if (str(reuse_cached_jobid)=="1"):
        headers["X-API-Reuse-Cached-Jobid"]="1"
    if token is not None:
        headers["Authorization"]="Bearer {}".format(token)

    res=requests.post(_url(
        '/api/job/{}/dynamicgp.cate'.format(jobid)), files=data, headers=headers);
    return ret_jobid(res)

def uploadfile(datafile,
               token=None):
    """Upload a file

    Upload a file

    Parameters
    ----------
    filename Filename of a file to upload

    Returns
    -------
    backend filename reference
    """
    data={
        'data': (datafile, open(datafile, 'rb') if datafile!=None else None ),
        }

    headers=dict()
    if token is not None:
        headers["Authorization"]="Bearer {}".format(token)

    res=requests.post(_url('/api/uploadfile'), files=data, headers=headers);
    if res.status_code==200:
        res_json = res.json()
        if 'fileref' in res_json:
            return res_json['fileref']
    return None

def ploturl(jobid,plottype=None):
    """Return plot URL

    Return plot URL

    Parameters
    ----------
    jobid : UUID
            Job ID of the previously submitted job

    plottype : string
            Plot Type

    Returns
    -------
    string
        url

    """

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
