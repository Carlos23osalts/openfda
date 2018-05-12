import http.server
import socketserver
import http.client
import json

#Now we stablish the ip and the port of the server
IP = "localhost" #Local cause it will work with our local machine
PORT = 8000

socketserver.TCPServer.allow_reuse_address = True
#Now we create a httprequest class
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        #Now we create the code for sending the response status
        sel.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers(

        def active_ingredient(): #This fucntion is used for seacrhing the active ingredients
            headers= {'User-Agent': 'http-client'}
            conn = http.client.HTTPSConnection("api.fda.gov")
            data = self.path.strip('/search').split('&')
            drug = data[0].split('=')[1]
            limit = data[1].split('=')[1]
            print("client has succesfully made a request")

            url = "/drug/label.json?search=active_ingredient:" + drug + '&' + 'limit=' + limit
            print(url)
            conn.request("GET", url, None, headers)
            r1 = conn.getresponse()
            repos_raw = r1.read().decode("utf-8")
            conn.close()
            repos = json.loads(repos_raw)

            drug = []
            a = 0
            nlimit= int(limit)
            intro = "<head>"+ '<h1>' + "Here is your drugs ID list" +'<body style="background-color:snow;">'+'</h1>'+ '</head>'
            sd = "<ol>"

            while a < nlimit:
                try:
                    drug.append(repos['results'][a]['openfda']['brand_name'][0])
                    a += 1

                except:
                    a += 1
                    print("There is no drug with this active ingredient")
                    drug.append('Unknown')

            with open("trial4.html", "w") as f:
                f.write(intro)
                f.write(sd)
                for el in drug:
                    el_1 = "<t>" + "<li>" + el
                    f.write(el_1)

        def manufacturer_name():
            headers = {'User-Agent': 'http-client'}
            conn = http.client.HTTPSConnection("api.fda.gov")
            data = self.path.strip('/search?').split('&')
            manufacturer_name = data[0].split('=')[1]
            limit = data[1].split('=')[1]
            print("client has succesfully made a request")

            url = "/drug/label.json?search=openfda.manufacturer_name:" + manufacturer_name + '&' + 'limit=' + limit
            print(url)
            conn.request("GET", url, None, headers)
            r1 = conn.getresponse()
            repos_raw = r1.read().decode("utf-8")
            conn.close()
            repos = json.loads(repos_raw)

            drug = []
            a = 0
            nlimit = int(limit)
            intro = "<head>" + '<h1>' + "Here is your drug list from the manufacturer you searched." + '<body style="background-color:snow;">' + '</h1>' + '</head>'
            sd = "<ol>"

            while a < nlimit:
                try:
                    drug.append(repos['results'][a]['openfda']['brand_name'][0])
                    a += 1

                except:
                    a += 1
                    print("There is no drug with this active ingredient")
                    drug.append('Unknown')

            with open("trial4.html", "w") as f:
                f.write(intro)
                f.write(sd)
                for el in drug:
                    el_1 = "<t>" + "<li>" + el
                    f.write(el_1)

        def drug_list(): #for giving the default drug list
            headers = {'User-Agent': 'http-client'}
            conn = http.client.HTTPSConnection("api.fda.gov")
            data = self.path.strip('label.json?').split('=')
            limit = data[1]
            print("client has succesfully made a request")
            url = "/drug/label.json?limit=" + limit
            print(url)
            conn.request("GET", url, None, headers)
            r1 = conn.getresponse()
            repos_raw = r1.read().decode("utf-8")
            conn.close()
            repos = json.loads(repos_raw)

            drug = []
            a = 0
            nlimit = int(limit)
            intro = "<head>" + '<h1>' + "Here is your drug default list" + '<body style="background-color:snow;">' + '</h1>' + '</head>'
            sd = "<ol>"

            while a < nlimit:
                try:
                    drug.append(repos['results'][a]['openfda']['brand_name'][0])
                    a += 1

                except:
                    a += 1
                    print("There is no drug with this active ingredient")
                    drug.append('Unknown')


            with open("trial4.html", "w") as f:
                f.write(intro)
                f.write(sd)
                for el in drug:
                    el_1 = "<t>" + "<li>" + el
                    f.write(el_1)

        def manufacturer_list():  # for giving the default manufacturer name list
            headers = {'User-Agent': 'http-client'}
            conn = http.client.HTTPSConnection("api.fda.gov")
            data = self.path.strip('label.json?').split('=')
            limit = data[1]
            print("client has succesfully made a request")
            url = "/drug/label.json?limit=" + limit
            print(url)
            conn.request("GET", url, None, headers)
            r1 = conn.getresponse()
            repos_raw = r1.read().decode("utf-8")
            conn.close()
            repos = json.loads(repos_raw)

            drug = []
            a = 0
            nlimit = int(limit)
            intro = "<head>" + '<h1>' + "Here is your manufacturer name default list" + '<body style="background-color:snow;">' + '</h1>' + '</head>'
            sd = "<ol>"

            while a < nlimit:
                try:
                    drug.append(repos['results'][a]['openfda']['manufacturer_name'][0])
                    a += 1

                except:
                    a += 1
                    print("There is no drug with this active ingredient")
                    drug.append('Unknown')

            with open("trial4.html", "w") as f:
                f.write(intro)
                f.write(sd)
                for el in drug:
                    el_1 = "<t>" + "<li>" + el
                    f.write(el_1)


        if self.path == "/":
            try:
                print("SEARCH: client entered search web")
                with open("search.html",'r') as f:
                    mensaje= f.read()
                    self.wfile.write(bytes(mensaje, "utf8"))
            except KeyError:
                print('ERROR')
                with open("error.html",'r') as f:
                    mensaje= f.read()
                    self.wfile.write(bytes(mensaje, "utf8"))


        elif 'active' in self.path: # let´s try to find a drug and a limit entered by user
            try:
                active_ingredient()
                with open("trial4.html", "r") as f:
                    ingr = f.read()
                    self.wfile.write(bytes(ingr, "utf8"))
            except KeyError:
                print('ERROR')
                with open("error.html", 'r') as f:
                    mensaje = f.read()
                    self.wfile.write(bytes(mensaje, "utf8"))


        elif 'manufacturer' in self.path:
            try:
                manufacturer_list()
                with open("trial4.html", "r") as f:
                    ingr = f.read()
                    self.wfile.write(bytes(ingr, "utf8"))
            except KeyError:
                print('ERROR')
                with open("error.html", 'r') as f:
                    mensaje = f.read()
                    self.wfile.write(bytes(mensaje, "utf8"))


        elif 'druglist'in self.path:
            try:
                drug_list()
                with open("trial4.html", "r") as f:
                    ingr = f.read()
                    self.wfile.write(bytes(ingr, "utf8"))
            except KeyError:
                print('ERROR')
                with open("error.html", 'r') as f:
                    mensaje = f.read()
                    self.wfile.write(bytes(mensaje, "utf8"))

        elif 'manufacturerlist'in self.path:
            try:
                manufacturer_list()
                with open("trial4.html", "r") as f:
                    ingr = f.read()
                    self.wfile.write(bytes(ingr, "utf8"))
            except KeyError:
                print('ERROR')
                with open("error.html", 'r') as f:
                    mensaje = f.read()
                    self.wfile.write(bytes(mensaje, "utf8"))

        return






# Handler = http.server.SimpleHTTPRequestHandler
Handler = testHTTPRequestHandler

httpd = socketserver.TCPServer((IP, PORT), Handler)
print("serving at port", PORT)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    pass

httpd.server_close()
print("")
print("Server stopped")