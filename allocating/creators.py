# create elements
from shared.universe import elem
from events.activity import Activity, Bundle
from networks.basic import Zone
from networks.transit import Stop, TransitLine
from networks.pedestrian import Sidewalk

def add_activity(name, U0, Um, Sigma, Lambda, Xi, \
                 time_win, min_duration, \
                 is_madatory, pref_timing):
    elem.activities[name] = Activity(name, U0, Um, Sigma, Lambda, Xi, \
                                     time_win, min_duration, \
                                     is_madatory, pref_timing)

def add_bundle(key, activity_name_list):
    bundle_name = 'PN' + str(key)
    activity_list = map(lambda actv_name: elem.activities[actv_name], \
                        activity_name_list)
    elem.bundles[key] = Bundle(bundle_name, activity_list)

def add_zone(key, activity_name_list, population):
    zone_name = 'ZN' + str(key)
    activity_list = map(lambda actv_name: elem.activities[actv_name], activity_name_list)
    elem.nodes[key] = Zone(zone_name, activity_list, population)

def add_sidewalk(key, head_name, tail_name, walk_time, capacity):
    sidewalk_name = 'SW' + str(key)
    head_node, tail_node = elem.nodes[head_name], elem.nodes[tail_name]
    elem.walks[key] = Sidewalk(sidewalk_name, head_node, tail_node, walk_time, capacity)

def get_stop(key):
    "Return the stop with the given name, creating it if necessary. "
    if key not in elem.nodes:
        stop_name = 'ST' + str(key)
        elem.nodes[key] = Stop(stop_name)
    return elem.nodes[key]

def gen_timetable(offset, headway, dwell_time, total_run, in_vehicle_time):
    " Generate the timetable with given parameters. "
    timetable = [None] * total_run
    sum_in_vehicle_time = [sum(in_vehicle_time[0:i+1]) for i in xrange(len(in_vehicle_time))]
    for run in xrange(total_run):
        move_time = lambda tt: tt + headway*run + offset + dwell_time
        timetable[run] = map(move_time, [0] + sum_in_vehicle_time)
    return timetable

def add_line(key, offset, headway, n_run, stop_name_list, time_list, fare_matrix, capacity):
    line_name = 'LN' + str(key)
    # generate stop list
    stop_list = []
    for stop_name in stop_name_list:
        new_stop = get_stop(stop_name)
        stop_list.append(new_stop)
    # generate timetable
    timetable = gen_timetable(offset, headway, 0, n_run, time_list)
    elem.lines[key] = TransitLine(line_name, timetable, stop_list, fare_matrix, capacity)
