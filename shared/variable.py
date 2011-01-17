# Utilities, probabilites and flows 

class UtilVar(object):
    def __init__(self):
        # 1-dimension dict nested in 1-dimension list, 
        # i.e. activity_util[timeslice][activity_name]
        self.activity_util = []
        # 1-dimension dict nested in 1-dimension list, and then in a dict
        # i.e. state_optimal_util[commodity][timeslice][state]
        # the expected maximum utility: E{max_d {V_d} }
        self.state_optimal_util = {}
        # 1-dimension dict, i.e. commodity_optimal_util[commodity]
        self.commodity_optimal_util = {}
        # expected utility for all out-of-home patterns
        # 1-dimension dict, i.e. out_of_home_util[home]
        self.out_of_home_util = {}
        # expected utility for in-home pattern
        # 1-dimension dict, i.e. in_home_util[home]
        self.in_home_util = {}


class ProbVar(object):
    def __init__(self):
        # in-home pattern choice probability
        self.in_home_choice_prob = {}
        # 1-dimension dict, i.e. bundle_choice_prob[home][pattern]
        self.bundle_choice_prob = {}
        # 2-dimension dict nested in 1-dimension list, and then in a dict
        # i.e. transition_choice_prob[commodity][timeslice][state][transition]
        self.transition_choice_prob = {}

class FlowVar(object):
    """ The world of the economic activities and transport network. 
        The variables in this class define the rules of this world.
    """
    def __init__(self):
        
        # assginment
        # 1-dimension dict, i.e. link_flows[move]
        self.movement_flows = {}
        self.movement_steps = {}
        # 2-dimension dict nested in 1-dimension list, and then in a dict
        # i.e. transition_flows[commodity][timeslice][state][transition]
        self.transition_flows = {}
##        # 2-dimension dict nested in 1-dimension list, and then in a dict
##        # i.e. transition_flows[commodity][timeslice][state][transition]
##        self.transition_flows = {}
##        # 1-dimension dict nested in 1-dimension list, 
##        # i.e. commodity_flows[commodity][timeslice]
##        self.commodity_flows = {}
        # 1-dimension dict nested in 1-dimension list, and then in a dict
        # i.e. state_flows[commodity][timeslice][state]
        self.state_flows = {}
        # 1-dimension dict, i.e. commodity_flows[commodity]
        self.commodity_flows = {}
        # 2-dimension dict nested in 1-dimension list
        # i.e. OD_trips[timeslice][origin][destination]
        self.OD_trips = []
        # 1-dimension dict nested in 1-dimension list
        # i.e. zone_population[timeslice][zone]
        self.zone_population = []
        # 1-dimension dict nested in 1-dimension list
        # i.e. actv_population[timeslice][actv]
        self.actv_population = []
        # dynamic travel time between zones
        # i.e. dyna_travel_times[timeslice][zone_a][zone_b]
        self.dyna_travel_times = []
        # static travel time between zones
        # i.e. dyna_travel_times[zone_a][zone_b]
        self.static_travel_times = {}

        
        ## export to MATLAB
        ## mat_pattern_flow = [None] * num_sample
        ## mat_zone_passenger = [None] * num_sample
        ## mat_aggrg_trip = [None] * num_sample

