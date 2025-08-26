(define (problem dualdeskroom_housework)
    (:domain housework)

    ; Begin objects
    (:objects
        robot - agent
        dualdeskroom - room
        bread kettle cup_ramen - item
        toaster stove water_dispenser - appliance
        dualdesk_1 dualdesk_2 - desk
    )

    ; Begin init
    (:init
		(agent_at robot dualdeskroom)
		(agent_hand_free robot)
		(appliance_at stove dualdeskroom)
		(appliance_at toaster dualdeskroom)
		(appliance_at water_dispenser dualdeskroom)
		(appliance_on stove)
		(appliance_on water_dispenser)
		(boiled kettle)
		(cooked bread)
		(is_bread bread)
		(is_cup_ramen cup_ramen)
		(is_desk dualdesk_1)
		(is_desk dualdesk_2)
		(is_kettle kettle)
		(is_stove stove)
		(is_toaster toaster)
		(is_water_dispenser water_dispenser)
		(item_accessible bread)
		(item_accessible cup_ramen)
		(item_accessible dualdesk_1)
		(item_accessible dualdesk_2)
		(item_accessible kettle)
		(item_accessible stove)
		(item_accessible toaster)
		(item_accessible water_dispenser)
		(item_at cup_ramen dualdeskroom)
		(item_at dualdesk_1 dualdeskroom)
		(item_at dualdesk_2 dualdeskroom)
		(item_in kettle stove)
		(item_on bread dualdesk_1)
		(item_pickable bread)
		(item_pickable cup_ramen)
		(item_pickable kettle)
    )
    ; End init

    ; Begin goal
(:goal
       (item_on kettle dualdesk_1)
   )
    ; End goal
)
