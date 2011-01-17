# Activity class
import math
import hashlib
import scipy.integrate as integrate
from utils.convert import min2slice, slice2min
from shared.universe import conf

class Activity(object):
    "Each activity is specified as a set of confeters which determine its marginal utility. "
    def __init__(self, name, U0, Um, Sigma, Lambda, Xi, \
                 time_win, min_duration, \
                 is_madatory = 0, pref_timing = 0):
        ''' U0 is the baseline utility level of acivity. 
            Um is the maximum utility of activity. 
            Sigma determines the slope or steepness of the curve. 
            Lambda determines the relative position of the inflection point. 
            Xi determines the time of day at which the marginal utility reaches the maximum. 
            time_win is the interval of starting time for this activity (a tuple). 
            min_duration is the minimum duration for this activity. 
        '''
        # activity type
        self.name, self.is_madatory, self.pref_timing = name, is_madatory, pref_timing
        # utility function parameters
        self.U0, self.Um = U0, Um
        self.Sigma, self.Lambda, self.Xi = Sigma, Lambda, Xi
        # spatial and temproal constraints
        self.locations = []
        self.time_win = (min2slice(time_win[0]), min2slice(time_win[1]))
        self.min_duration = min2slice(min_duration)
        
    def __hash__(self):
        return int(hashlib.md5(repr(self)).hexdigest(), 16)
        
    def __repr__(self):
        return "%s" % (self.name)

    def __eq__(self, other):
        return self.name == other.name

    def add_location(self, pos):
        self.locations.append(pos)
    
    def marginal_util(self, time):
        "The marginal activity utility is ONLY a function of the duration. "
        nominator = self.Sigma*self.Lambda*self.Um
        denominator = (math.exp( self.Sigma*(time-self.Xi) ) *
            math.pow(1.0+math.exp( -self.Sigma*(time-self.Xi) ), self.Lambda+1.0) )
        return self.U0 + nominator/denominator
        
    def discrete_util(self, timeslice):
        lower = slice2min(timeslice) - conf.TICK/2.0
        upper = lower + conf.TICK
        if timeslice == 0:
            ans = integrate.quad(self.marginal_util, 0.0, conf.TICK/2.0)[0] + \
                integrate.quad(self.marginal_util, conf.DAY-conf.TICK/2.0, conf.DAY)[0]
        else:
            ans = integrate.quad(self.marginal_util, lower, upper)[0]
        return ans

    def calc_schedule_delay(self, timeslice):
        if not self.is_madatory:
            return 0.0
        lower = self.pref_timing - conf.DELTA - slice2min(timeslice)
        upper = slice2min(timeslice) - conf.DELTA - self.pref_timing
        if lower > 0.0:
            early_cost = lower * conf.ALPHA_early
            return early_cost
        if upper > 0.0:
            late_cost = upper * conf.ALPHA_late
            return late_cost
        return 0.0


class Bundle(object):
    def __init__(self, name, activity_list):
        self.name = name
        self.activity_set = frozenset(activity_list)

    def __hash__(self):
        return int(hashlib.md5(repr(self)).hexdigest(), 16)
        
    def __repr__(self):
        return "%s" % (sorted(self.activity_set))

    def __eq__(self, other):
        return self.name == other.name

def main():
    fout = open('activity_util.log', 'w')
    creat_activity_4node()
    gen_activity_util()
    export_activity_util(fout)
    creat_activity_pattern_4node()
    for key, pattern in elem.patterns.items():
        print key, pattern
 
if __name__ == '__main__':
    main()