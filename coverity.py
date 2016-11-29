#!/usr/bin/env python
import tempfile
import json, sys, re
import base64
import urllib2
from StringIO import StringIO
import gzip
import logging
import os
import ConfigParser
import getopt

progress = 0

def show_progress (count, total):
    progress = (count * 100 / total)
    sys.stdout.write("\r%d %%" % progress)
    sys.stdout.flush()

def send_mail (title, content, toaddr, dry_run):
    if content == "":
        return None
    tmp = tempfile.NamedTemporaryFile ()
    logging.debug ("create temp file %s" % tmp.name)
    f = open (tmp.name, "w")
    f.write (content)
    f.close ()
    cmd = "cat %s | /usr/bin/mail -a \"Content-type: text/html\" -s \"%s\" %s" % (tmp.name , title, toaddr)
    logging.info (cmd)
    if dry_run is False:
        os.system (cmd)
    else:
        logging.info ("Dry run")

class CoverityData:
    def __init__ (self):
        self.action = ""
        self.checker = ""
        self.cid = -1
        self.classification = ""
        self.comment = ""
        self.committed = False
        self.true = ""
        self.cwe = -1
        self.displayCategory = ""
        self.displayComparison = ""
        self.displayComponent = ""
        self.displayFile = ""
        self.displayFirstDetectedBy = ""
        self.displayFunction = ""
        self.displayImpact = ""
        self.displayIssueKind = ""
        self.displayType = ""
        self.domain = ""
        self.externalReference = ""
        self.fileInstanceId = -1
        self.fileLanguage = ""
        self.firstDetected = ""
        self.firstSnapshotDate = ""
        self.firstSnapshotDescription = ""
        self.firstSnapshotId = -1
        self.firstSnapshotStream = ""
        self.firstSnapshotTarget = ""
        self.firstSnapshotVersion = ""
        self.fixTarget = ""
        self.functionMergeName = ""
        self.id = -1
        self.lastDefectInstanceId = -1
        self.lastDetected = ""
        self.lastDetectedDescription = ""
        self.lastDetectedId = -1
        self.lastDetectedStream = ""
        self.lastDetectedTarget = ""
        self.lastDetectedVersion = ""
        self.lastFixed = ""
        self.lastTriaged = ""
        self.legacy = ""
        self.mergeExtra = ""
        self.mergeKey = ""
        self.occurrenceCount = -1
        self.owner = ""
        self.ownerFullName = ""
        self.ownerId = ""
        self.pivotKey = ""
        self.projectId = -1
        self.ruleStrength = ""
        self.severity = ""
        self.status = ""
        self.subcategory = ""
        self.link = ""

class CoverityReport:
    def __init__ (self, coverity_datas):
        pass
    def get_report_by_user (self, owner):
        pass

class CoverityReportStyle1 (CoverityReport):
    def __init__ (self, coverity_datas):
        self.user_data = {}
        self.coverity_datas = coverity_datas

    def get_report_by_user (self, owner):
        logging.debug ("get_report (%s)" % owner)
        report = ""
        logging.debug ("Total %d datas" % len (self.coverity_datas))

        for p in self.coverity_datas:
            content = "<tr><td style=\"border:1px solid #AAAAAA;padding: 3px;\"><a href = \"%s\" target=_blank style = \"color: navy\">%d</a></td><td style=\"border:1px solid #AAAAAA;padding: 3px;\">%s</td><td style=\"border:1px solid #AAAAAA;padding: 3px;\">%s</td><td style=\"border:1px solid #AAAAAA;padding: 3px;\">%s</td><td style=\"border:1px solid #AAAAAA;padding: 3px;\">%s</td><td style=\"border:1px solid #AAAAAA;padding: 3px;\">%s</td></tr>" % (p.link, p.cid, p.firstDetected, p.displayType, p.displayFile, p.displayCategory, p.owner)
            if p.owner in self.user_data:
                self.user_data[p.owner] = self.user_data[p.owner] + "\n" + content
            else:
                self.user_data[p.owner] = content

        for u in self.user_data.keys():
            css = """
<style>
table.t_data
{
    /* border: 1px; - **EDITED** - doesn't seem like influences here */
    background-color: #FFFFFF;
}
table.t_data thead th, table.t_data thead td
{
    margin: 1px;
    padding: 5px;
}

a
{
    color: navy;
}
</style>"""

            data = self.user_data[u]
            data = "<tr style = \"background-color: #CCCCCC;\"><td style=\"border:1px solid #AAAAAA;padding: 3px;\">%s</td><td style=\"border:1px solid #AAAAAA;padding: 3px;\">%s</td><td style=\"border:1px solid #AAAAAA;padding: 3px;\">%s</td><td style=\"border:1px solid #AAAAAA;padding: 3px;\">%s</td><td style=\"border:1px solid #AAAAAA;padding: 3px;\">%s</td><td style=\"border:1px solid #AAAAAA;padding: 3px;\">%s</td></tr>" % ("CID", "First Detected", "Display Type", "Display File", "Display Category", "Owner") + data

            data = "<table class=\"t_data\" style=\"border-collapse:collapse;\">" + data + "</table>"
            logging.debug ("body 0")
            logging.debug (data)
            data = "<body>" + \
                   css + \
                   "<html>" + \
                   data
            logging.debug ("body 1")
            logging.debug (data)
            data = data + \
                   "</html>" + \
                   "</body>"
            logging.debug ("body 3")
            logging.debug (data)
            self.user_data[u] = data

        logging.debug ("[user_data]\n")
        for u in self.user_data.keys():
            logging.debug ("user = %s", u)
        if owner in self.user_data:
            return self.user_data [owner]
        else:
            return None

class CoverityReportStyle2 (CoverityReport):
    def __init__ (self, coverity_datas):
        self.user_data = {}
        self.coverity_datas = coverity_datas

    def get_report_by_user (self, owner):
        logging.debug ("get_report (%s)" % owner)
        report = ""
        logging.debug ("Total %d datas" % len (self.coverity_datas))

        for p in self.coverity_datas:
            content = """
<tr>
    <td style=\"border:1px solid #AAAAAA;padding: 6px;\"><a href = \"%s\" target=_blank style = \"color: navy\">%d</a></td>
    <td style=\"border:1px solid #AAAAAA;padding: 6px;\">%s</td>
    <td style=\"border:1px solid #AAAAAA;padding: 6px;\">%s</td>
    <td style=\"border:1px solid #AAAAAA;padding: 6px;\">%s</td>
    <td style=\"border:1px solid #AAAAAA;padding: 6px;\">%s</td>
    <td style=\"border:1px solid #AAAAAA;padding: 6px;\">%s</td>
    <td style=\"border:1px solid #AAAAAA;padding: 6px;\">%s</td>
    <td style=\"border:1px solid #AAAAAA;padding: 6px;\">%s</td>
</tr>""" % (p.link, p.cid, p.firstDetected, p.displayImpact, p.displayType, p.displayFile, p.displayFunction, p.displayCategory, p.owner)
            if p.owner in self.user_data:
                self.user_data[p.owner] = self.user_data[p.owner] + "\n" + content
            else:
                self.user_data[p.owner] = content

        for u in self.user_data.keys():
            css = """
<style>
table.t_data
{
    /* border: 1px; - **EDITED** - doesn't seem like influences here */
    background-color: #FFFFFF;
}
table.t_data thead th, table.t_data thead td
{
    margin: 1px;
    padding: 5px;
}

a
{
    color: navy;
}
</style>"""

            data = self.user_data[u]
            data = """
<tr style = \"background-color: #444444;color: #FFFFFF\">
    <td style=\"border:1px solid #AAAAAA;padding: 6px;\">%s</td>
    <td style=\"border:1px solid #AAAAAA;padding: 6px;\">%s</td>
    <td style=\"border:1px solid #AAAAAA;padding: 6px;\">%s</td>
    <td style=\"border:1px solid #AAAAAA;padding: 6px;\">%s</td>
    <td style=\"border:1px solid #AAAAAA;padding: 6px;\">%s</td>
    <td style=\"border:1px solid #AAAAAA;padding: 6px;\">%s</td>
    <td style=\"border:1px solid #AAAAAA;padding: 6px;\">%s</td>
    <td style=\"border:1px solid #AAAAAA;padding: 6px;\">%s</td>
</tr>""" % ("CID", "First Detected", "Impact", "Type", "File", "Function", "Category", "Owner") + data

            data = "<table class=\"t_data\" style=\"border-collapse:collapse;color: #444444\">" + data + "</table>"
            logging.debug ("body 0")
            logging.debug (data)
            data = "<body>" + \
                   css + \
                   "<html>" + \
                   data
            logging.debug ("body 1")
            logging.debug (data)
            data = data + \
                   "</html>" + \
                   "</body>"
            logging.debug ("body 3")
            logging.debug (data)
            self.user_data[u] = data

        logging.debug ("[user_data]\n")
        for u in self.user_data.keys():
            logging.debug ("user = %s", u)
        if owner in self.user_data:
            return self.user_data [owner]
        else:
            return None

class CoverityReportStyleHigh (CoverityReport):
    def __init__ (self, coverity_datas):
        self.user_data = {}
        self.coverity_datas = coverity_datas

    def get_report_by_user (self, owner):
        logging.debug ("get_report (%s)" % owner)
        report = ""
        logging.debug ("Total %d datas" % len (self.coverity_datas))

        for p in self.coverity_datas:
            content = """
<tr>
    <td style=\"border:1px solid #AAAAAA;padding: 6px;\"><a href = \"%s\" target=_blank style = \"color: navy\">%d</a></td>
    <td style=\"border:1px solid #AAAAAA;padding: 6px;\">%s</td>
    <td style=\"border:1px solid #AAAAAA;padding: 6px;\">%s</td>
    <td style=\"border:1px solid #AAAAAA;padding: 6px;\">%s</td>
    <td style=\"border:1px solid #AAAAAA;padding: 6px;\">%s</td>
    <td style=\"border:1px solid #AAAAAA;padding: 6px;\">%s</td>
    <td style=\"border:1px solid #AAAAAA;padding: 6px;\">%s</td>
    <td style=\"border:1px solid #AAAAAA;padding: 6px;\">%s</td>
</tr>""" % (p.link, p.cid, p.firstDetected, p.displayImpact, p.displayType, p.displayFile, p.displayFunction, p.displayCategory, p.owner)
            if p.owner in self.user_data:
                self.user_data[p.owner] = self.user_data[p.owner] + "\n" + content
            else:
                self.user_data[p.owner] = content

        for u in self.user_data.keys():
            css = """
<style>
table.t_data
{
    /* border: 1px; - **EDITED** - doesn't seem like influences here */
    background-color: #FFFFFF;
}
table.t_data thead th, table.t_data thead td
{
    margin: 1px;
    padding: 5px;
}

a
{
    color: navy;
}
</style>"""

            data = self.user_data[u]
            data = """
<tr style = \"background-color: red;color: #ffffff\">
    <td style=\"border:1px solid #AAAAAA;padding: 6px;\">%s</td>
    <td style=\"border:1px solid #AAAAAA;padding: 6px;\">%s</td>
    <td style=\"border:1px solid #AAAAAA;padding: 6px;\">%s</td>
    <td style=\"border:1px solid #AAAAAA;padding: 6px;\">%s</td>
    <td style=\"border:1px solid #AAAAAA;padding: 6px;\">%s</td>
    <td style=\"border:1px solid #AAAAAA;padding: 6px;\">%s</td>
    <td style=\"border:1px solid #AAAAAA;padding: 6px;\">%s</td>
    <td style=\"border:1px solid #AAAAAA;padding: 6px;\">%s</td>
</tr>""" % ("CID", "First Detected", "Impact", "Type", "File", "Function", "Category", "Owner") + data

            data = "<table class=\"t_data\" style=\"border-collapse:collapse;color: #444444\">" + data + "</table>"
            logging.debug ("body 0")
            logging.debug (data)
            data = "<body>" + \
                   css + \
                   "<html>" + \
                   data
            logging.debug ("body 1")
            logging.debug (data)
            data = data + \
                   "</html>" + \
                   "</body>"
            logging.debug ("body 3")
            logging.debug (data)
            self.user_data[u] = data

        logging.debug ("[user_data]\n")
        for u in self.user_data.keys():
            logging.debug ("user = %s", u)
        if owner in self.user_data:
            return self.user_data [owner]
        else:
            return None

class Requests:
    class Response :
        def __init__ (self):
            self.status_code = None
            self.encoding = None
            self.text = None
            self.headers = {}

    def __init__ (self):
        self.resp = self.Response()

    def get (self, url, params = {}, headers = {}):
        url = url + "?"
        for p in params:
            url = url + p + "=" + str(params[p]) + "&"
        req = urllib2.Request(url)
        for i in headers:
            req.add_header(i, headers[i])
        resp = urllib2.urlopen(req)
        self.resp.text = resp.read()
        self.resp.status_code = resp.getcode()
        self.resp.headers = resp.info()
        return self.resp

    def post (self, url, params = None, headers = None):
        url = url
        ps = ""
        for p in params:
            ps = ps + p + "=" + params[p] + "&"
        req = urllib2.Request(url, ps)
        for i in headers:
            req.add_header(i, headers[i])
        resp = urllib2.urlopen(req)
        self.resp.text = resp.read()
        self.resp.status_code = resp.getcode()
        self.resp.headers = resp.info()
        return self.resp

    def post_binary (self, url, params = None, headers = None):
        url = url
        ps = ""
        req = urllib2.Request(url, params)
        for i in headers:
            req.add_header(i, headers[i])
        resp = urllib2.urlopen(req)
        self.resp.status_code = resp.getcode()
        self.resp.headers = resp.info()

        buf = StringIO(resp.read())
        f = gzip.GzipFile(fileobj=buf)
        self.resp.text = f.read()
        logging.debug(self.resp.text)
        return self.resp

requests = Requests()

class Coverity:
    def __init__ (self, id, pwd, projectId = 10002, viewId = 10177):
        self.projectId=projectId
        self.viewId=viewId
        self.loginId=id
        self.loginPwd=pwd
        self.host='http://172.17.31.40:8080'
        self.cookie = self.__get_cookie__()
        self.xsecurity = ""
        self.__login__()
        self.__now_page = 1
        self.all_coverity_datas = []
        self.all_users = []
        self.__progress = 0

    def __login__ (self):
        url = 'http://172.17.31.40:8080/j_spring_security_check;' + self.cookie
        params = dict(
                j_username=self.loginId,
                j_password=self.loginPwd
                )
        headers = {'Cookie': self.cookie}
        resp = requests.post(url=url, params=params, headers=headers)
        match = re.search("csrf.*?X-SECURITY.*?token.*?'(.*?)'", resp.text)
        self.xsecurity =  match.group(1)

    def __get_cookie__ (self):
        url = 'http://172.17.31.40:8080/login/login.htm'
        params = dict()
        headers = {'Cookie': ""}
        resp = requests.get(url=url, params=params, headers=headers)

        match = re.search("j_spring_security_check;(.*?)\"", resp.text)
        cookie =  match.group(1)
        return cookie

    def get_defactInstanceId(self, cid):
        url = self.host + '/defects/search.json'
        params = dict(
            cids=str(cid)
        )
        headers = {'Cookie': self.cookie}
        resp = requests.get(url=url, params=params, headers=headers)
        data = json.loads(resp.text)
        defactInstanceId=str(data[u'dataSrc'][u'resultSet'][u'results'][0][u'defectInstanceId'])

        return defactInstanceId

    def get_url (self, cid):
        return self.host + "/query/defects.htm?projectId=" + str(self.projectId) + "&cid=" + str(cid)

    def __get_outstanding (self):
        global progress
        progress = progress + 1
        show_progress (progress, 100)
        logging.debug("now page = " + str(self.__now_page))
        self.__set_page(self.__now_page)
        url = self.host + '/reports/table.json'
        params = dict(
            projectId=self.projectId,
            viewId=self.viewId,
        )
        headers = {'Cookie': self.cookie}
        resp = requests.get(url=url, params=params, headers=headers)
        data = json.loads(resp.text)
        coverity_datas = []
        local_datas = data[u'resultSet'][u'results']
        for c in local_datas:
            cdata = CoverityData()
            cdata.cid = int(c[u'cid'])
            cdata.owner = c[u'owner']
            cdata.firstDetected = c[u'firstDetected']
            cdata.displayType = c[u'displayType']
            cdata.displayImpact = c[u'displayImpact']
            cdata.displayFile = c[u'displayFile']
            cdata.displayFunction = c[u'displayFunction']
            cdata.displayCategory = c[u'displayCategory']
            cdata.link = self.get_url (cdata.cid)
            logging.debug("[cdata] cid = %s, owner = %s, firstDetected = %s, displayType = %s, displayFile = %s, displayCategory = %s" % (cdata.cid, cdata.owner, cdata.firstDetected, cdata.displayType, cdata.displayFile, cdata.displayCategory))
            coverity_datas.append (cdata)

        logging.debug("offset = " + str(data[u'resultSet'][u'offset']))
        logging.debug(len(local_datas))
        progress = progress + 1
        show_progress (progress, 100)
        if len(local_datas) != 0:
            logging.debug("first cid = " + str(local_datas[0][u'cid']))
            self.all_coverity_datas = self.all_coverity_datas + coverity_datas
            self.__now_page = self.__now_page + 1
            self.__get_outstanding()

    def __set_page (self, page_num):
        req = Requests()
        url = self.host + '/views/table.json'
        cookie = self.cookie
        headers = {'Cookie': cookie, 'Pragma': 'no-cache' , 'Accept-Encoding': 'gzip, deflate' ,
                'Accept-Language': 'en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4' , 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36' ,
                'Content-Type': 'application/json; charset=UTF-8' , 'Accept': 'application/json, text/javascript, */*; q=0.01' , 'Cache-Control': 'no-cache' , 'X-Requested-With': 'XMLHttpRequest' , 'Connection': 'keep-alive' , 'X-SECURITY': self.xsecurity}
        params = '{"projectId":' + str(self.projectId) + ',"viewId":' + str(self.viewId) + ',"pageNum":' + str (page_num) + ', "offset":321}'
        resp = req.post_binary (url=url, params=params, headers=headers)

    def __have_high (self, datas):
        have_high = False
        for d in datas:
            if d.displayImpact == 'High':
                have_high = True
                break
        return have_high

    def get_report (self, owner=""):
        logging.debug ("get_report (%s)" % owner)
        if len(self.all_coverity_datas) == 0:
            self.__get_outstanding()
        if owner != "" and self.__have_high (self.get_all_datas_by_user (owner)) is True:
            coverity_report = CoverityReportStyleHigh (self.all_coverity_datas)
        else:
            coverity_report = CoverityReportStyle2 (self.all_coverity_datas)

        report = coverity_report.get_report_by_user (owner)
        if report is None:
            logging.error ("report is Empty")
        return report

    def get_all_users (self):
        if len(self.all_coverity_datas) == 0:
            self.__get_outstanding()
        for p in self.all_coverity_datas:
            if p.owner not in self.all_users:
                self.all_users.append (p.owner)
        return self.all_users

    def get_all_datas (self):
        if len(self.all_coverity_datas) == 0:
            self.__get_outstanding()
        return self.all_coverity_datas

    def get_all_datas_by_user (self, user):
        if len(self.all_coverity_datas) == 0:
            self.__get_outstanding()
        d = []
        for l in self.all_coverity_datas:
            if l.owner == user:
                d.append(l)
        return d

def __usage__ ():
    #print "Usage: " + sys.argv[0] + " [option] [id] [pwd (base64 encode)] [args...]"
    print """
Usage
-r
    get report.

    -u
        user
    -s [mail address, separate by space.
        Send mail to
    -o [file name]
        Write to file
    -a
        Send mail to all user.
    -d dry run
-l
    list all users

    """
    sys.exit (0)

class OutputType:
    FILE = 1
    STDOUT = 2
    MAIL = 3

def __output__ (type, title, content, to = None, dry_run = False):
    show_progress (100, 100)
    if content is None:
        content = ""
    if type == OutputType.FILE:
        f = open(to, 'w')
        f.write (content)
        f.close()
    elif type == OutputType.MAIL:
        send_mail (title, content, to, dry_run)
    elif type == OutputType.STDOUT:
        print content

def get_send_list (file):
    logging.debug ("get_send_list")
    if file == "":
        return []
    list = []
    try:
        with open(file) as fp:
            for line in fp:
                line = line.strip()
                list.append(line)
    except:
        logging.warning ("file not exist")
    return list

if __name__ == '__main__':
    config = ConfigParser.RawConfigParser({"white_list": ""})

    send_list = []
    try:
        cfgpath = os.path.dirname(os.path.abspath(__file__)) + "/setting.cfg"
        config.read(cfgpath)
        host = config.get("global", "host")
        port = config.getint("global", "port")
        id = config.get("global", "id")
        password = config.get("global", "password")
        white_list = config.get("global", "white_list")
        project_id = config.get("coverity", "project_id")
        view_id = config.get("coverity", "view_id")

    except ConfigParser.Error:
        logging.error ("Get cfg fail")
        exit (2)

    debug = "debug"
    try:
        debug = config.get("global", "debug")
    except:
        pass

    level = logging.ERROR
    if debug == "info":
        level = logging.INFO
    elif debug == "error":
        level = logging.ERROR
    elif debug == "warning":
        level = logging.WARNING
    elif debug == "debug":
        level = logging.DEBUG
    elif debug == "critical":
        level = logging.CRITICAL
    else:
        level = logging.ERROR

    logging.basicConfig(filename="/var/log/coverity.log", level=level)

    logging.debug ("host = %s, port = %d, id = %s, password = %s, white_list = %s, project_id = %s, view_id = %s" % (host, port, id, password, white_list, project_id, view_id))

    if white_list != "":
        send_list = get_send_list (white_list)

    logging.info ("host = %s, port = %d, id = %s, password = %s" % (host, port, id, password))

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hru:w:o:s:lad", ["help", "report", "user=", "writeto=", "output_file=", "send_mail =", "list", "sendtoall", "dry_run"])
    except getopt.GetoptError as err:
        logging.warning (err)
        __usage__()
        sys.exit(2)

    output = ""
    opts_dict = {}
    for o, v in opts:
        opts_dict [o] = v

    logging.debug (opts_dict)

    progress

    if "-r" in opts_dict:
        co = Coverity (id, password.decode("base64"), project_id, view_id)
        progress = progress + 1
        show_progress (progress, 100)
        datas = co.get_all_datas ()
        progress = progress + 1
        show_progress (progress, 100)
        if "-a" in opts_dict:
            if len (send_list) == 0:
                users = co.get_all_users ()
            else:
                logging.info ("Get users from %s" % white_list)
                users = send_list
            logging.info ("%d users" % len (users))
            for u in users:
                if u == "Unassigned":
                    continue
                content = co.get_report (u)
                if content is None:
                    logging.warning ("Content of %s is Empty" % u)
                    continue

                ds = co.get_all_datas_by_user (u)
                issues_count = len (ds)
                mail = u + "@qnap.com"
                logging.debug ("user = %s, mail = %s" % (u, mail))
                title = "Coverity: %s - %d issues" % (u, issues_count)
                logging.debug ("title = %s\n" % title)
                progress = progress + 1
                show_progress (progress, 100)
                dry_run = False
                if "-d" in opts_dict:
                    dry_run = True
                __output__ (OutputType.MAIL, title, content, mail, dry_run)
            exit (0)
        user = ""
        if "-u" in opts_dict:
            user = opts_dict ["-u"]
        output = co.get_report (user)
        if output is None:
            logging.error ("output is None")

        type = None
        to = ""
        if "-o" in opts_dict:
            logging.info ("output to file")
            to = opts_dict ["-o"]
            type = OutputType.FILE
        elif "-s" in opts_dict:
            logging.info ("send mail")
            to = opts_dict ["-s"]
            if not re.match(r"[^@]+@[^@]+\.[^@]+", to):
                logging.warning ("Email %s is invalid" % to)
                exit (2)

            type = OutputType.MAIL
        else:
            logging.info ("output to stdout")
            type = OutputType.STDOUT

        ds = co.get_all_datas_by_user (user)
        issues_count = len (ds)
        title = "Coverity: %s - %d issues" % (user, issues_count)
        dry_run = False
        if "-d" in opts_dict:
            dry_run = True
        __output__ (type, title, output, to, dry_run)
    elif "-l" in opts_dict:
        co = Coverity (id, password.decode("base64"), project_id, view_id)
        output = ""
        for u in co.get_all_users():
            high_count = 0
            data = co.get_all_datas_by_user (u)
            for d in data:
                if d.displayImpact == 'High':
                    high_count = high_count + 1
            data_count_by_user = len (data)
            #output = output + u + " (" + str(data_count_by_user) + ") (" + high_count + " High)\n"
            output = output + "%s (%d) (%d High)\n" % (u, data_count_by_user, high_count)

        __output__ (OutputType.STDOUT, "", output)
    else:
        __usage__ ()

    exit (0)
