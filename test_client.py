from time import strftime, localtime

def example(req):
    req.add_common_vars()
    env_vars = req.subprocess_env
    getReqStr = env_vars['QUERY_STRING']     # the url after the ?
    getReqArr = getReqStr.split('&')         #'split to array of k-v pairs
    getReqDict = {}

    for item in getReqArr:      
       tempArr = item.split('=')   
       getReqDict[tempArr[0]] = tempArr[1]

    req.content_type = 'text/html'
    time_str = strftime("%a %b %d %H:%M:%S %Y", localtime())
    message = "<h1>Hello from mod_python!</h1>"
    message += "<p>The time on this server is %s</p>" % (time_str)
    message += "Query : " + str(getReqDict)
    return message
