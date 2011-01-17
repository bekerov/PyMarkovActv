# compute equilibrium flows
from shared.universe import flow
from utils.get import get_move_flow
from planning.dynaprog import calc_state_optimal_util, calc_bundle_choice_prob
from loading.load import calc_commodity_flow, calc_state_flows
from loading.init import init_state_optimal_util, init_transition_choice_prob
from loading.init import init_state_flows, init_transition_flows
from loading.init import init_OD_trips, init_zone_population, init_actv_population
#from loading.init import init_movement_steps

#def update_movement_flows(iter_num):
#    for each_move in flow.movement_flows.keys():
#        flow.movement_flows[each_move] *= (iter_num / (iter_num + 1.0))
#    for each_move in flow.movement_steps.keys():
#        get_move_flow(each_move)
#        flow.movement_flows[each_move] += (flow.movement_steps[each_move] / (iter_num + 1.0))

def find_fixed_point(N):
    " Find the equilibrium flows using method of successive average (MSA). "
    # iterate demand and supply sides
    for iter_num in xrange(N):
        
        print "\n  ### interation %d ###" % iter_num
        
        print '\n [dynamic programming]'
#        init_movement_steps()
#        print '  init_movement_steps()'
        init_state_optimal_util(float('-inf'))
        print "  init_state_optimal_util(float('-inf'))"
        init_transition_choice_prob(0.0)
        print '  init_transition_choice_prob(0.0)'
        
        calc_state_optimal_util()
        print '  calc_state_optimal_util()'
        calc_bundle_choice_prob()
        print '  calc_choice_prob()'
        calc_commodity_flow()
        print '  calc_commodity_flow()'
        
        print '\n [traffic assignment]'
        init_state_flows(0.0)
        print '  init_state_flows(0.0)'
        init_transition_flows(0.0)
        print '  init_transition_flows(0.0)'
        init_zone_population(0.0)
        print '  init_zone_population(0.0)'
        init_actv_population(0.0)
        print '  init_actv_population(0.0)'
        init_OD_trips(0.0)
        print '  init_OD_trips(0.0)'

        calc_state_flows()
        print '  calc_state_flows()'
#        update_movement_flows(iter_num)
#        print "  update_move_flows(%d)" % iter_num