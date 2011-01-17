import hashlib
from shared.universe import conf, elem, util
from utils.convert import min2slice
from itertools import combinations

#class InitDict(dict):
#    def __init__(self, default = None):
#        self.default = default
#
#    def __getitem__(self, key):
#        if not self.has_key(key):
#            self[key] = self.default()
#        return dict.__getitem__(self, key)


class Commodity(object):
    """ The passengers choosing each activity bundles at every residential location (home)
        is a commodity. Or the activity bundles are enumerated implicitly. """
    def __init__(self, home, bundle):
        self.home, self.bundle = home, bundle
        self.init_state = State(elem.home_am_activity, self.home, self.bundle.activity_set)
        self.term_state = State(elem.home_pm_activity, self.home, frozenset([elem.home_pm_activity]))
        
    def __repr__(self):
        return "%s-%s" % (self.home, self.bundle)
        
    def __hash__(self):
        return int(hashlib.md5(repr(self)).hexdigest(), 16)
        
    def __eq__(self, other):
        return self.home == other.home and self.bundle == other.bundle

    
class State(object):
    """ The state contains the position of the traveler (zone), the activity participated
        and lagged variable (autoregressive process), excluding timeslice. 
    """
    def __init__(self, activity, zone, todo, lagged=0):
        self.zone, self.activity, self.todo, self.lagged = \
            zone, activity, todo, lagged
        
    def __repr__(self):
        return "%s-%s(%s)-%d" % (self.zone, self.activity, sorted(self.todo), self.lagged)
        
    def __hash__(self):
        return int(hashlib.md5(repr(self)).hexdigest(), 16)
        
    def __eq__(self, other):
        return self.activity == other.activity and \
               self.zone == other.zone and \
               self.todo == other.todo and \
               self.lagged == other.lagged

    
class Transition(object):
    """ Transition defines the next state according to current state, including timeslice. 
    """
    def __init__(self, state, path):
        self.state, self.path = state, path
        
    def __repr__(self):
        return "%s-%s" % (self.state, self.path)
        
    def __hash__(self):
        return int(hashlib.md5(repr(self)).hexdigest(), 16)
        
    def __eq__(self, other):
        return self.state == other.state and \
               self.path == other.path

def enum_commodity():
    # for different home location and activity bundles
    for home in elem.home_list:
        for bundle in elem.bundles.values():
            yield Commodity(home, bundle)

def enum_state(commodity, timeslice):
    activity_bundle = commodity.bundle.activity_set
    indoor_activities = [elem.home_am_activity, elem.home_pm_activity]
    outdoor_activities = activity_bundle.difference(indoor_activities)
    # yield a state with all activities
    yield commodity.init_state
    # yield states with different number of activities
    for N in xrange(len(outdoor_activities)):
        # generate different combinations from the N activities
        for todo_list in combinations(outdoor_activities, N+1):
            todo_set = frozenset(todo_list + (elem.home_pm_activity , ))
            # pick up each activity in the todo list
            for each_actv in todo_list:
                if each_actv.time_win[0] > timeslice or \
                   timeslice > each_actv.time_win[1]:
                    continue
                # choose one location for the activity
                for position in each_actv.locations:
                    yield State(each_actv, position, todo_set)
    # yield a state with the last activity: in-home activity in PM
    yield commodity.term_state

def enum_path(timeslice, this_zone, next_zone):
    for each_path in elem.paths[this_zone][next_zone]:
        # for travel_time, prob in each_path.travel_time_distribution:
        travel_timeslice, travel_cost = each_path.calc_travel_impedences(timeslice)
        arrival_timeslice = timeslice + travel_timeslice
        starting_time = arrival_timeslice+1
        if starting_time > min2slice(conf.DAY):
            continue
        yield each_path, starting_time, travel_cost

def enum_transition(commodity, timeslice, state):
    for next_actv in state.todo:
        if next_actv == elem.home_pm_activity:
            if len(state.todo) > 2:
                continue
            location_set = [commodity.home]
        else:
            location_set = next_actv.locations
        if next_actv <> state.activity:
            next_todo = state.todo.difference([state.activity])
        else:
            next_todo = state.todo
        for next_zone in location_set:
            # calculate the new state variable
            next_state = State(next_actv, next_zone, next_todo)
            for each_path, starting_time, travel_cost in \
                enum_path(timeslice, state.zone, next_zone):
                if util.state_optimal_util[commodity][starting_time][next_state] == float('-inf'):
                    continue
                # calculate of schedule delay
                schedule_delay = 0.0
                if state.activity <> next_actv:
                    schedule_delay = next_actv.calc_schedule_delay(starting_time)
                yield (Transition(next_state, each_path), 
                       starting_time, travel_cost, schedule_delay)
