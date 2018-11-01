from flask import Flask, render_template, request, jsonify
import json
import os
import psycopg2


app = Flask(__name__)

@app.route('/' , strict_slashes=False)
def index_parser():
    return render_template("index.html")

@app.route('/signup' , strict_slashes=False)
def signup_parser():
    return render_template("signup.html")


@app.route('/signuphandler', methods=['POST'] , strict_slashes=False)
def signup():
    location = json.loads(request.data)
    #print location['lon']
    try:
        conn = psycopg2.connect(host="localhost",database="cloud", user="postgres", password="postgres")
        cur = conn.cursor()
        query = "insert into customer values(1,'"+location['name']+"' ,st_setsrid(st_point("+str(location['lon'])+","+str(location['lat'])+"),4326))"
        print (query)
        cur.execute(query)
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

    return jsonify(request.data)




@app.route('/help', methods=['POST'] , strict_slashes=False)
def helper():
    location = json.loads(request.data)
    radius = 1000
    ret_list = []
    try:
        conn = psycopg2.connect(host="localhost",database="cloud", user="postgres", password="postgres")
        cur = conn.cursor()
        while (len(ret_list)<2 and radius <5000):
            ret_list = []
            query = "SELECT name, ST_AsText(location) FROM  customer WHERE ST_DWithin(st_transform(location::geometry,900913),st_transform(ST_GeomFromText('POINT("+str(location['lon'])+" "+str(location['lat'])+")',4326),900913) ,"+str(radius)+")"
            print (query)
            cur.execute(query)
            for row in cur:
                temp = row[1]
                temp = temp.replace("POINT(", "")
                temp = temp.replace(")", "")
                temp = temp.split(" ")
                ret_list.append({'pname':row[0],"lon":temp[0], "lat":temp[1]})
            radius = radius*2

        print (ret_list)
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

    return jsonify(results = ret_list)


if __name__ == '__main__':
    app.run(host= '127.0.0.1',port=8080,debug=True)
