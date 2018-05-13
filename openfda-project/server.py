import http.server
import socketserver
import http.client
import json
socketserver.TCPServer.allow_reuse_adress = True
#Now we stablish the ip and the port of the server
IP = "localhost"
PORT = 8000
class OpenFDAHTML():
    def texto(self,list):
        peanut = ""
        for elements in list:
            peanut = peanut+"\n\t<li>" + elements + "</li>"
        mess = "<!doctype html>" + "\n" +"<html>" + "\n" + "<body>" + "\n" "<ul>" + "\n"+peanut+"</ul>" + "\n" + "</body>" + "\n" + "</html>"
        with open("text.html","w")as f:
            f.write(mess)
class OpenFDAClient():
    def urldrug(self,url):
        headers = {'User-Agent': 'http-client'}
        conn = http.client.HTTPSConnection("api.fda.gov")
        conn.request("GET", url, None, headers)
        r1 = conn.getresponse()
        info1 = r1.read().decode("utf-8")
        info_list = json.loads(info1)
        conn.close()
        return info_list
class OpenFDAParser():
    def equisde(self,info_list,plus):
        list2=[]
        if len(plus)==2:
            for i in range(len(info_list["results"])):
                try:
                    list2.append(info_list["results"][i][plus[0]][plus[1]])
                except KeyError:
                    list2.append("Unknown")
        elif len(plus)==3:
            for i in range(len(info_list["results"])):
                try:
                    list2.append(info_list["results"][i][plus[0]][plus[1]][plus[2]])
                except KeyError:
                    list2.append("Unknonwn")
        return list2
class  testHTTPHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            list2=[]
            if self.path == "/":
                self.send_response(200)
                with open("search2.html","r")as f:
                    mess=f.read()
                with open("text.html","w")as f:
                    f.write(mess)

            elif "searchDrug" in self.path:
                self.send_response(200)
                drug=self.path.split("&")[0].split("=")[1]
                if "limit"in self.path:
                    limit=self.path.split("&")[1].split("=")[1]
                else:
                    limit = "10"
                url ="/drug/label.json?search=active_ingredient:" + drug + "&" + "limit=" + limit
                info_list= OpenFDAClient.urldrug(self,url)
                seed=["active_ingredient",0]
                list2= OpenFDAParser.lol(self,info_list,seed)
                OpenFDAHTML.texto(self,list2)
            elif "searchCompany" in self.path:
                self.send_response(200)
                company = self.path.split("&")[0].split("=")[1]
                if "limit" in self.path:
                    limit = self.path.split("&")[1].split("=")[1]
                else:
                    limit = "10"
                url = "/drug/label.json?search=manufacturer_name:" + company + "&" + "limit=" + limit
                info_list = OpenFDAClient.urldrug(self, url)
                seed = ["openfda", "manufacturer_name", 0]
                list2 = OpenFDAParser.lol(self, info_list, seed)
                OpenFDAHTML.texto(self, list2)
            elif "listDrugs" in self.path:
                self.send_response(200)
                glue =self.path.split("?")[1].split("=")[1]
                url = "/drug/label.json?limit=" + glue
                info_list = OpenFDAClient.urldrug(self, url)
                seed=["openfda","brand_name",0]
                list2 = OpenFDAParser.lol(self,info_list,seed)
                OpenFDAHTML.texto(self, list2)
            elif "listCompanies"in self.path:
                self.send_response(200)
                glue =self.path.split("?")[1].split("=")[1]
                url = "/drug/label.json?limit=" + glue
                info_list = OpenFDAClient.urldrug(self, url)
                seed=["openfda","manufacturer_name",0]
                list2 = OpenFDAParser.lol(self, info_list, seed)
                OpenFDAHTML.texto(self, list2)
            elif "listWarnings" in self.path :
                self.send_response(200)
                glue = self.path.split("?")[1].split("=")[1]
                url = "/drug/label.json?limit=" + glue
                info_list = OpenFDAClient.urldrug(self, url)
                seed = ["warnings", 0]
                list2 = OpenFDAParser.lol(self, info_list, seed)
                OpenFDAHTML.texto(self, list2)
            elif "secret" in self.path:
                self.send_response(401)
                self.send_header("WWW-Authenticate", "Basic realm='OpenFDA Private Zone")
                self.end_headers()
            elif "redirect" in self.path:
                self.send_response(302)
                self.send_header('Location', 'http://localhost:8000/')
                self.end_headers()
            else:
                self.send_response(404)
                list.append("Error 404: Webpage not found")
                OpenFDAHTML.texto(self, list)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open("text.html", "r")as f:
                file = f.read()
            self.wfile.write(bytes(file, "utf8"))
        except KeyError:
            self.send_response(404)
            list.append("Error 404: Webpage not found")
            OpenFDAHTML.texto(self, list)
        return

Handler = http.server.SimpleHTTPRequestHandler
Handler = testHTTPHandler
httpd = socketserver.TCPServer((IP, PORT), Handler)
print("serving at port", PORT)
httpd.serve_forever()