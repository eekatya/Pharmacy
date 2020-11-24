import cherrypy

from connect import parse_cmd_line
from connect import create_connection


@cherrypy.expose
class App:
    def __init__(self, args):
        self.args = args

    @cherrypy.expose
    def start(self):
        return "This web application was made by ITMO team 7"

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def drugs(self):
        with create_connection(self.args) as db:
            print(self.args)
            cur = db.cursor()
            cur.execute("SELECT id, tradename, intern_name FROM Drug")
            drugs = cur.fetchall()
        return [{"id": str(drug[0]).encode('iso8859').decode('utf8'),
                 "tradename": drug[1].encode('').decode('utf8'),
                 "inn": drug[2]}
                for drug in drugs]

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def pharmacies(self):
        with create_connection(self.args) as db:
            cur = db.cursor()
            cur.execute("SELECT id, address FROM Pharmacy_shop")
            pharmacies = cur.fetchall()
        return [{"id": pharmacy[0], "address": pharmacy[1]} for pharmacy in pharmacies]


cherrypy.config.update({
  'server.socket_host': '0.0.0.0',
  'server.socket_port': 8888,
})
cherrypy.quickstart(App(parse_cmd_line()))