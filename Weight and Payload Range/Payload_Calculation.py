# calculates payload weight (includes crew)
# last updated: 4/13/23

##############
# RFP Values #
##############

num_of_pass = 50            # number of passengers
num_of_crew = 3             # number of crew
W_sing_pass = 200           # weight of each passenger (lbf)
W_sing_pass_bag = 40        # weight of each passenger luggage (lbf)
W_sing_crew = 190           # weight of each crew (lbf)
W_sing_crew_bag = 30        # weight of each crew luggage (lbf)


W_crew = num_of_crew * (W_sing_crew + W_sing_crew_bag)      # total crew w_eight
W_pass = num_of_pass * (W_sing_pass + W_sing_pass_bag)      # total passenger w_eight
W_payload = W_crew + W_pass