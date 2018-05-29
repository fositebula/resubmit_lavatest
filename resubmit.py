import requests
from bs4 import BeautifulSoup as BS

json_data = """{"parameter": [{"name": "LAVA_SERVER", "value": "10.0.70.68"},{"name": "LAVA_USER", "value": "apuser"}, {"name": "LAVA_PASSWORD", "value": "<DEFAULT>"},{"name": "up_build_id", "value": "%s"}, {"name": "up_jobname", "value": "%s"},{"name": "up_verifier", "value": "%s"}, {"name": "up_build_result", "value": "pass"},{"name": "up_change_url", "value": "%s"}, {"name": "up_module", "value": "%s"},{"name": "build_list", "value": "%s"},{"name": "testpara", "value": "%s"},{"name": "test_case", "value": "%s"}, {"name": "build_type", "value": "full"},{"name": "imgnum", "value": "%s"}, {"name": "stable", "value": "%s"},{"name": "monkeytime", "value": "%s"}, {"name": "monkey_device_amount", "value": "%s"},{"name": "upstream_type", "value": "%s"}], "statusCode": "303", "redirectTo": ".", "Jenkins-Crumb":"3839267a4300c7fe3350437188d81076"}"""

data_str = 'name=LAVA_SERVER&value=10.0.70.68&name=LAVA_USER&value=apuser&' \
		   'name=LAVA_PASSWORD&value=%3CDEFAULT%3E&name=up_build_id&' \
		   'value={up_build_id}&name=up_jobname&value={up_jobname}&' \
		   'name=up_verifier&value={up_verifier}&name=up_build_result&' \
		   'value=pass&name=up_change_url&value={up_change_url}&' \
		   'name=up_module&value={up_module}&name=build_list&value={build_list}&' \
		   'name=testpara&value={testpara}&name=test_case&value={test_case}&' \
		   'name=build_type&value={build_type}&name=imgnum&value={imgnum}&' \
		   'name=stable&value={stable}&name=monkeytime&value={monkeytime}&' \
		   'name=monkey_device_amount&value={monkey_device_amount}&name=upstream_type&' \
		   'value={upstream_type}&statusCode=303&redirectTo=.&' \
		   'Jenkins-Crumb=3839267a4300c7fe3350437188d81076&json={json}&Submit=Build'

HEADER = {
            "Host" : "10.0.64.29:8080",
            # "User-Agent" : "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0",
            "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language" : "en-US,en;q=0.5",
            "Accept-Encoding" : "gzip, deflate",
            "Referer" : "http://10.0.64.29:8080/jenkins/job/lava_test/build?delay=0sec",
            "Content-Type" : "application/x-www-form-urlencoded",
            # "Content-Length" : "2043",
            "Cookie" : "jenkins-timestamper-offset=-28800000; JSESSIONID.ad55068c=node01xkddhut6ubkasaqkntjair8s340.node0",
            "Connection" : "keep-alive",
            "Upgrade-Insecure-Requests" : "1",
}

URL = "http://10.0.64.29:8080/jenkins/job/lava_test/build?delay=0sec"


def get_json_data(kv):
	str = json_data%(kv['up_build_id'],  kv['up_jobname'],  kv['up_verifier'],  kv['up_change_url'],  kv['up_module'],  kv['build_list'],  kv['testpara'],\
				  kv['test_case'],  kv['imgnum'],  kv['stable'],  kv['monkeytime'],  kv['monkey_device_amount'],  kv['upstream_type'])
	return str


def resubmit(data_str):
    print data_str
    resp = requests.post(url=URL, headers=HEADER, data=data_str)
    return resp

if __name__ == '__main__':
    jobids = ()
    for job in range(245136, 245137):
        if job == 245038:
            print "****************", 245038
            continue
        url = 'http://10.0.64.29:8080/jenkins/job/lava_test/{}/parameters/'.format(job)
        res = requests.get(url)
        soup = BS(res.content, 'lxml')
        tbodys = soup.find_all('tbody')
        kv = {}
        for tbody in tbodys:
            kv[tbody.select('.setting-name')[0].text] = tbody.select('.setting-input')[0].get('value').strip()

        jd = get_json_data(kv)
        kv['json'] = jd
        query_str = data_str.format(**kv)
        # print job, resubmit(query_str)
