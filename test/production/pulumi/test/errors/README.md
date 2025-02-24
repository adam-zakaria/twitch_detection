  aws:ec2:Instance (my-instance):
    error: 1 error occurred:
    	* creating EC2 Instance: operation error EC2: RunInstances, https response error StatusCode: 400, RequestID: cb90a8d4-2209-458c-b3b9-f7c53b5d8e1d, api error VcpuLimitExceeded: You have requested more vCPU capacity than your current vCPU limit of 8 allows for the instance bucket that the specified instance type belongs to. Please visit http://aws.amazon.com/contact-us/ec2-request to request an adjustment to this limit.

A bucket is a collection of instances of a particular type. i.e. g, m, etc. And in this case the error is because the quota of 40 we set is for spot instances.