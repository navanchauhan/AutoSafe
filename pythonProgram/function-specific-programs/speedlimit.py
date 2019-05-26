import overpy
import sys
import simplejson as sjson
import json
import geocoder 

g = geocoder.ip('me')

def maxspeed(coordinates, radius):
    lat, lon = coordinates
    api = overpy.Overpass()

    result = api.query("""
            way(around:""" + radius + """,""" + lat  + """,""" + lon  + """) ["maxspeed"];
                (._;>;);
                    out body;
                        """)
    results_list = []
    for way in result.ways:
        road = {}
        road["name"] = way.tags.get("name", "n/a")
        road["speed_limit"] = way.tags.get("maxspeed", "n/a")
        nodes = []
        for node in way.nodes:
            nodes.append((node.lat, node.lon))
        road["nodes"] = nodes
        results_list.append(road)
    return results_list


results = maxspeed((sys.argv[1], sys.argv[2]), sys.argv[3])
# Alternative
# results = maxspeed((lat, long, radius))
speedlimit = sjson.dumps(results[0]['speed_limit']).strip('\"')
print(speedlimit)