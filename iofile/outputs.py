# export data to file
from shared.universe import conf, elem, util, prob, flow
from utils.convert import min2slice
from planning.markov import enum_commodity, enum_state
from stats.estimator import calc_average_activity_duration

def export_activity_util(export):
    print>>export, '---------- activity utility ----------'
    for timeslice in xrange(min2slice(conf.DAY)+1):
        util.activity_util.append(dict() )
        for each_actv in elem.activities:
            print>>export, util.activity_util[timeslice][each_actv],
            print>>export, '\t', 
        print>>export

def export_OD_trips(export):
    print>>export, '\n-------- aggregate O-D trips ---------\n'
    for timeslice in xrange(min2slice(conf.DAY)):
##            print>>export, " [%3d] " % s
            for O in elem.zone_list:
                print>>export, " [%3d] " % timeslice,
                for D in elem.zone_list:
                    print>>export, "\t %08.1f" % (flow.OD_trips[timeslice][O][D]),
##                    print>>export, "%2d:%08.1f   " % (D, aggreg_trips[s][O][D]),
                print>>export

def export_depart_flows(export):
    print>>export, '\n-------- departure flows ---------\n'
    for O in elem.zone_list:
        for D in elem.zone_list:
            print>>export, "\t %s->%s" % (O, D), 
    print>>export
    for timeslice in xrange(min2slice(conf.DAY)):
        print>>export, " [%3d] " % timeslice,
        for O in elem.zone_list:
            for D in elem.zone_list:
                print>>export, "\t %08.1f" % (flow.OD_trips[timeslice][O][D]),
##                    print>>export, "%2d:%08.1f   " % (D, aggreg_trips[s][O][D]),
        print>>export
    
def export_state_flows(export):
    print>>export, '\n-------- state flows ---------\n'
    for comm in enum_commodity():
        print>>export, ">>commodity %s " % comm
        for timeslice in xrange(min2slice(conf.DAY)+1):
            print>>export, " [%03d]\t" % timeslice, 
            zone_population = {}
            for each_actv in comm.bundle.activity_set:
                zone_population[each_actv] = 0.0
            for state in enum_state(comm, timeslice):
                zone_population[state.activity] += flow.state_flows[comm][timeslice][state]
##                print>>export, flow.transition_flows[comm][timeslice][state].values(),
            for each_actv in sorted(comm.bundle.activity_set):
                print>>export, "%8.2f\t" % (zone_population[each_actv]),
            print>>export
        print>>export

def export_zone_population(export):
    print>>export, '\n-------- zone passengers ---------\n'
    for zone in sorted(elem.zone_list):
        print>>export, "\t %s" % (zone),
    print>>export
    for timeslice in xrange(min2slice(conf.DAY)):
        print>>export, "[%3d]   " % timeslice, 
        for zone in sorted(elem.zone_list):
            print>>export, "\t %08.1f" % flow.zone_population[timeslice][zone],
        print>>export

def export_actv_population(export):
    print>>export, '\n-------- activity passengers ---------\n'
    for each_actv in elem.activities.values():
        print>>export, "\t %s" % (each_actv), 
    print>>export
    for timeslice in xrange(min2slice(conf.DAY)):
        print>>export, "[%3d]   " % timeslice, 
        for each_actv in elem.activities.values():
            print>>export, "\t %08.1f" % flow.actv_population[timeslice][each_actv],
        print>>export

def export_optimal_util(export):
    print>>export, '\n------optimal utility------\n'
    for comm in enum_commodity():
        print>>export, " commodity %s " % comm
        for timeslice in xrange(min2slice(conf.DAY)):
            print>>export, " [%3d s] " % timeslice, 
            for state in enum_state(comm, timeslice):
                print>>export, ("\t %s: %4.2f" % (state, util.state_optimal_util[comm][timeslice][state])), 
            print>>export
        print>>export

def export_movement_flows(export):
    print>>export, '\n------movement flows------\n'
    sorted_moves = sorted(flow.movement_flows.keys(), key = repr)
    max_bus_flow = float('-inf')
    max_sub_flow = float('-inf')
    for each_move in sorted_moves:
        print>>export, each_move, flow.movement_flows[each_move]
        if each_move.related_edge.related_vector.capacity == conf.CAPACITY_bus:
            if max_bus_flow < flow.movement_flows[each_move]:
                max_bus_flow = flow.movement_flows[each_move]
        if each_move.related_edge.related_vector.capacity == conf.CAPACITY_sub:
            if max_sub_flow < flow.movement_flows[each_move]:
                max_sub_flow = flow.movement_flows[each_move]
    print>>export, " maximum transit line flows %6.1f png" % (max_bus_flow)
    print>>export, " maximum subway line flows %6.1f png" % (max_sub_flow)


def export_bundle_choice(export):
    print>>export, '\n ------- bundle choice -------\n'
    for home in elem.home_list:
        print>>export, "[Home %s, Population %6.2f]" % (home, home.population)
        print>>export, "%s \t %6.2f" % (elem.in_home_bundle, home.population * \
                                        prob.in_home_choice_prob[home])
        for bundle in elem.bundles.values():
            if bundle == elem.in_home_bundle:
                continue
            print>>export, "%s \t %6.2f" % (bundle, home.population * \
                                            (1.0 - prob.in_home_choice_prob[home]) * \
                                            prob.bundle_choice_prob[home][bundle])
        print>>export

def export_activity_duration(export):
    print>>export, '\n ------- activity duration -------\n'
    for comm in enum_commodity():
        average_duration = calc_average_activity_duration(comm)
        for key, value in average_duration.items():
            print>>export, "%s: %.1f\t" % (key, value),
        print>>export

def export_travel_times(export):
    print>>export, '\n ------- dynamic travel time -------\n'
    for timeslice in xrange(min2slice(conf.DAY)):
        print>>export, "[%d]" % timeslice
        for origin in elem.zone_list:
            print>>export, "(%s)  " % origin,
            for dest in elem.zone_list:
                print>>export, "%s: %3.2f  " % (dest, flow.dyna_travel_times[timeslice][origin][dest]),
            print>>export
    
# export computational results
def export_data(case):
    export_file_name = 'export_data_'+case+'.txt'
    export_file = open(export_file_name, 'w')
    export_pattern_flow(export_file)
    export_zone_passenger_raw(export_file)
    export_zone_passenger(export_file)
##     export_aggreg_trip(export_file)
##     export_activity_trip(export_file)
##     export_passenger_trip(export_file)
##     export_optimal_util(export_file)
##     export_path_set(export_file)
##     export_link_flow(export_file)