
from unittest.mock import patch

import cherrypy
from cherrypy.test import helper
from cherrypy.lib.sessions import RamSession

from checkMeIn import CheckMeIn


class SimpleCPTest(helper.CPWebCase):
    @staticmethod
    def setup_server():
        cherrypy.tree.mount(CheckMeIn(), '/', {})

    def test_report_page(self):
        self.getPage("/reports/")
        self.assertStatus('200 OK')

    def test_reports(self):
        self.getPage("/reports/standard?startDate=2018-09-03&endDate=2018-09-03")
        self.assertStatus('200 OK')

    def test_sql(self):
        self.getPage(
            "/reports/customSQLReport?sql=SELECT+*+FROM+members%3B%0D%0A+++++")
        self.assertStatus('200 OK')
    def test_bad_sql(self):
        self.getPage(
            "/reports/customSQLReport?sql=SELECT+FROM+members%3B%0D%0A+++++")
        self.assertStatus('200 OK')

    def tests_savereport(self):
        self.getPage(
            "/reports/saveCustom?sql=SELECT+*+FROM+members%3B%0D%0A+++++&report_name=Fred")
        self.assertStatus('200 OK')

    def test_customReportGood(self):
        self.getPage("/reports/savedCustom?report_id=1")
        self.assertStatus('200 OK')

    def test_customReportBad(self):
        self.getPage("/reports/savedCustom?report_id=100")
        self.assertStatus('200 OK')

    def test_buildingGraph(self):
        self.getPage("/reports/graph?startDate=2019-12-01&endDate=2019-12-30")
        self.assertStatus('200 OK')
