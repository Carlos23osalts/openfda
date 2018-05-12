import http.server
import socketserver
import http.client
import json




# -- IP and the port of the server
IP = "localhost"  # Localhost means "I": your local machine
PORT = 8000

socketserver.TCPServer.allow_reuse_address = True
# HTTPRequestHandler class
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    # GET
    def do_GET(self):

        path =self.path  #We use this step so that all the different status codes change in the diferent cases we have

        if path == "/" or 'searchDrug' in path or 'searchCompany' in path or 'listDrugs' in path or 'listCompanies' in path or 'listWarnings' in path:
            status_code = 200
        elif 'redirect' in path:
            status_code = 302
        elif 'secret' in path:
            status_code = 401
        else:
            status_code = 404

        self.send_response(status_code)

        if path == "/" or 'searchDrug' in path or 'searchCompany' in path or 'listDrugs' in path or 'listCompanies' in path or 'listWarnings' in path:
            self.send_header('Content-type', 'text/html')
        elif 'redirect' in path:
            self.send_header('Location', 'http://localhost:8000/')
        elif 'secret' in path:
            self.send_header('WWW-Authenticate', 'Basic realm="OpenFDA Private Zone"')


        # Send response status code
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()



        def active_ingredient():  #For searching the active ingredient
            headers = {'User-Agent': 'http-client'}
            conn = http.client.HTTPSConnection("api.fda.gov")
            data = self.path.strip('/search?').split('&')
            drug = data[0].split('=')[1]
            if 'limit'in self.path:
                limit = data[1].split('=')[1]
                if 'limit' == '':  #In case the limit is empty we use 10 as default
                    limit= '10'
            else:
                limit= '10'
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

        def manufacturer_name():  #For the manufacturer name of a drug
            headers = {'User-Agent': 'http-client'}
            conn = http.client.HTTPSConnection("api.fda.gov")
            data = self.path.strip('/search?').split('&')
            manufacturer_name = data[0].split('=')[1]
            if 'limit'in self.path:
                limit = data[1].split('=')[1]
                if 'limit' == '':
                    limit = '10'
            else:
                limit= '10'
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
            nlimit = int(limit) #We transform the limit into an integer, so we can use it.
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

        def warning_list():  # for giving the warnings of a drug list
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
            warnin = []
            a = 0
            b = 0
            i = 0
            nlimit = int(limit)
            intro = "<head>" + '<h1>' + "Here is your warning list" + '<body style="background-color:snow;">' + '</h1>' + '</head>'
            sd = "<ol>"

            while a < nlimit:
                try:
                    drug.append(repos['results'][a]['openfda']['brand_name'][0])
                    a += 1

                except:
                    a += 1
                    print("There is no drug with this active ingredient")
                    drug.append('Unknown')

            while b < nlimit:
                try:
                    warnin.append(repos['results'][a]['warnings'][0])
                    b += 1

                except:
                    b += 1
                    print("There is no drug with this active ingredient")
                    warnin.append('Unknown')

            with open("trial4.html", "w") as f:
                f.write(intro)
                f.write(sd)
                while i < nlimit:
                    for el in drug:
                        el_1 = "<t>" + "<li>" + 'The warning for:' + drug[i] + ' '+ 'is' + ' '+ warnin[i]
                        f.write(el_1)
                        i += 1