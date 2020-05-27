from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
# import cgi

## Importing necessary files for CRUD operation
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

## Creating Session and connecting to DB (restauranmenu.db)
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBsession = sessionmaker(bind = engine)
session = DBsession()

class webserverHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith('/restaurants'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                restaurants = session.query(Restaurant).all()

                output = "<html><body>"
                output += "<h3> <a href='/restaurants/new'> Add a new restaurant </a> </h3> <br>"
                for restaurant in restaurants:
                    output += restaurant.name
                    output += "<br>"
                    output += f'''<a href="/restaurants/{restaurant.id}/edit"> Edit </a><br>'''
                    output += f'''<a href="/restaurants/{restaurant.id}/delete"> Delete </a> <br>'''
                    output += "<br>"
                output += "</body></html>"
                self.wfile.write(output.encode())

            elif self.path.endswith('/restaurants/new'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = "<html><body>"
                output += '''<form method="POST" enctype="multipart/form-data" action="/restaurants/new">'''
                output += '''<h2>Enter New Restaurant Name</h2>'''
                output += '''<input name="message" type="text">'''
                output += '''<input type="submit" value="Create">'''
                output += "</form>"
                output += "</body></html>"

                self.wfile.write(output.encode())
            elif self.path.endswith('/edit'):
                id = self.path.split('/')[2]
                restaurant = session.query(Restaurant).filter(id == Restaurant.id).one()

                if restaurant != []:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()

                    output = "<html><body>"
                    output += f'''<form method="POST" enctype="multipart/form-data" action="/restaurants/{id}/edit">'''
                    output += f'''<h2>{restaurant.name}</h2>'''
                    output += f'''<input name="message" type="text" value="{restaurant.name}">'''
                    output += '''<input type="submit" value="Rename">'''
                    output += "</form>"
                    output += "</body></html>"

                    self.wfile.write(output.encode())
            elif self.path.endswith('/delete'):
                id = self.path.split('/')[2]
                restaurant = session.query(Restaurant).filter(id == Restaurant.id).one()

                if restaurant != []:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()

                    output = "<html><body>"
                    output += f'''<form method="POST" enctype="multipart/form-data" action="/restaurants/{id}/delete">'''
                    output += f'''<h2>Are you sure to delete restaurant {restaurant.name}</h2>'''
                    output += '''<input type="submit" value="Delete">'''
                    output += "</form>"
                    output += "</body></html>"

                    self.wfile.write(output.encode())
            elif self.path.endswith('/hello'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = "<html><body>"
                output += "<h1>Hola!!</h1>"
                output += '''<form method="POST" enctype="multipart/form-data" action="/hello">'''
                output += '''<h2>What do you want me to display in this page?</h2>'''
                output += '''<input name="message" type="text">'''
                output += '''<input type="submit" value="submit">'''
                output += "</form>"
                output += "<a href='/hola'>Go to Hola</a>"
                output += "</body></html>"

                self.wfile.write(output.encode())
                print(output)
                return
            elif self.path.endswith('/hola'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = "<html><body>"
                output += "<h1>Hola!!</h1>"
                output += '''<form method="POST" enctype="multipart/form-data" action="/hello">'''
                output += '''<h2>What do you want me to display in this page?</h2>'''
                output += '''<input name="message" type="text">'''
                output += '''<input type="submit" value="submit">'''
                output += "</form>"
                output += "<a href='/hello'>Back to Hello</a>"
                output += "</body></html>"

                self.wfile.write(output.encode())
                print(output)
                return

        except IOError:
            self.send_error(404, "File Not Found" + self.path)

    def do_POST(self):
        try:
            if self.path.endswith('/restaurants/new'):
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location ', '/restaurants')
                self.end_headers()

                length = int(self.headers.get('Content-length', 0))
                data = parse_qs(self.rfile.read(length).decode())
                restaurantName = data.get(' name')[0].split('\n')[2]

                newRestaurant = Restaurant(name = restaurantName)
                session.add(newRestaurant)
                session.commit()
            elif self.path.endswith('/edit'):
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location ', '/restaurants')
                self.end_headers()

                length = int(self.headers.get('Content-length', 0))
                data = parse_qs(self.rfile.read(length).decode())
                newName = data.get(' name')[0].split('\n')[2]

                id = self.path.split('/')[2]
                restaurant = session.query(Restaurant).filter(id == Restaurant.id).one()
                if restaurant != []:
                    restaurant.name = newName
                    session.add(restaurant)
                    session.commit()
            elif self.path.endswith('/delete'):
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()

                id = self.path.split('/')[2]
                restaurant = session.query(Restaurant).filter(id == Restaurant.id).one()
                if restaurant != []:
                    session.delete(restaurant)
                    session.commit()
            elif self.path.endswith('/hello') or self.path.endswith('/hola'):
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                #print("Entered")
                length = int(self.headers.get('Content-length', 0))
                data = parse_qs(self.rfile.read(length).decode())
                message = data.get(' name')[0].split('\n')[2]
                #print(data)

                #ctype, pdict = cgi.parse_header(self.headers.get('Content-type'))
                #if ctype == "multipart/form-data":
                    #fields = cgi.parse_multipart(self.rfile, pdict)
                    #content = fields.get("message")[0].decode()

                output = "<html><body>"
                output += "<h1>Hello!!</h1>"
                output += f"<h1> {message} </h1>"
                output += f'''<form method="POST" enctype="multipart/form-data" action="/hello">'''
                output += '''<h2>What do you want me to display in this page?</h2>'''
                output += '''<input name="message" type="text">'''
                output += '''<input type="submit" value="submit">'''
                output += "</form>"
                output += "<a href='/hola'>Go to Hola</a>"
                output += "</body></html>"
                #print(content)
                #print("Wassup")
                self.wfile.write(output.encode('utf-8'))


        except:
            print("Error in parsing")

def main():
    try:
        PORT = 8080
        server = HTTPServer(('', PORT), webserverHandler)
        print("Web Server running on port :", PORT)
        server.serve_forever()

    except KeyboardInterrupt:
        print("^C entered...Stopping web server...")
        server.socket.close()

if __name__ == "__main__":
    main()