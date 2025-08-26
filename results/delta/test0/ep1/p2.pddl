(define (problem innerhouse_housework)
    (:domain housework)

    ; Begin objects
    (:objects
        robot - agent
        kitchen bathroom bedroom livingroom - room
        bread kettle cup_ramen - item
        toaster stove water_dispenser - appliance
        livingroom_desk - desk
    )

    ; Begin init
    (:init
		(agent_at robot kitchen)
		(agent_hand_free robot)
		(appliance_at stove kitchen)
		(appliance_at toaster kitchen)
		(appliance_at water_dispenser kitchen)
		(appliance_on water_dispenser)
		(cooked bread)
		(is_bread bread)
		(is_cup_ramen cup_ramen)
		(is_desk livingroom_desk)
		(is_kettle kettle)
		(is_stove stove)
		(is_toaster toaster)
		(is_water_dispenser water_dispenser)
		(item_accessible bread)
		(item_accessible cup_ramen)
		(item_accessible kettle)
		(item_accessible livingroom_desk)
		(item_accessible stove)
		(item_accessible toaster)
		(item_accessible water_dispenser)
		(item_at cup_ramen kitchen)
		(item_at kettle kitchen)
		(item_at livingroom_desk livingroom)
		(item_in bread water_dispenser)
		(item_pickable bread)
		(item_pickable cup_ramen)
		(item_pickable kettle)
		(neighbor kitchen livingroom)
		(neighbor livingroom kitchen)
    )
    ; End init

    ; Begin goal
(:goal
       (item_on bread livingroom_desk)
   )
    ; End goal
)
