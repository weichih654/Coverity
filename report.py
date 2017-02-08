import logging
log = logging.getLogger('coverity')
class CoverityReport:
    def __init__ (self, coverity_datas):
        pass
    def get_report_by_user (self, owner):
        pass
    def get_summary_by_user (self, owner):
        pass

class CoverityReportStyle1 (CoverityReport):
    def __init__ (self, coverity_datas):
        self.user_data = {}
        self.coverity_datas = coverity_datas

    def get_report_by_user (self, owner):
        log.debug ("get_report (%s)" % owner)
        report = ""
        log.debug ("Total %d datas" % len (self.coverity_datas))

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
            log.debug ("body 0")
            log.debug (data)
            data = "<body>" + \
                   css + \
                   "<html>" + \
                   data
            log.debug ("body 1")
            log.debug (data)
            data = data + \
                   "</html>" + \
                   "</body>"
            log.debug ("body 3")
            log.debug (data)
            self.user_data[u] = data

        log.debug ("[user_data]\n")
        for u in self.user_data.keys():
            log.debug ("user = %s", u)
        if owner in self.user_data:
            return self.user_data [owner]
        else:
            return None
    def get_summary_by_user (self, owner):
        pass

class CoverityReportStyle2 (CoverityReport):
    def __init__ (self, coverity_datas):
        self.user_data = {}
        self.coverity_datas = coverity_datas

    def get_report_by_user (self, owner):
        log.debug ("get_report (%s)" % owner)
        report = ""
        log.debug ("Total %d datas" % len (self.coverity_datas))

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
            log.debug ("body 0")
            log.debug (data)
            data = "<body>" + \
                   css + \
                   "<html>" + \
                   data
            log.debug ("body 1")
            log.debug (data)
            data = data + \
                   "</html>" + \
                   "</body>"
            log.debug ("body 3")
            log.debug (data)
            self.user_data[u] = data

        log.debug ("[user_data]\n")
        for u in self.user_data.keys():
            log.debug ("user = %s", u)
        if owner in self.user_data:
            return self.user_data [owner]
        else:
            return None

    def get_summary_by_user (self, owner):
        log.debug ("get_summary (%s)" % owner)
        report = ""
        return None


class CoverityReportStyleHigh (CoverityReport):
    def __init__ (self, coverity_datas):
        self.user_data = {}
        self.coverity_datas = coverity_datas

    def get_report_by_user (self, owner):
        log.debug ("get_report (%s)" % owner)
        report = ""
        log.debug ("Total %d datas" % len (self.coverity_datas))

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
            log.debug ("body 0")
            log.debug (data)
            data = "<body>" + \
                   css + \
                   "<html>" + \
                   data
            log.debug ("body 1")
            log.debug (data)
            data = data + \
                   "</html>" + \
                   "</body>"
            log.debug ("body 3")
            log.debug (data)
            self.user_data[u] = data

        log.debug ("[user_data]\n")
        for u in self.user_data.keys():
            log.debug ("user = %s", u)
        if owner in self.user_data:
            return self.user_data [owner]
        else:
            return None

    def get_summary_by_user (self, owner):
        log.debug ("get_summary (%s)" % owner)
        report = ""
        return None

