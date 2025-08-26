(define (problem singledeskroom_housework)
    (:domain housework)

    ; Begin objects
    (:objects
        robot - agent
        singledeskroom - room
        bread kettle cup_ramen - item
        toaster stove water_dispenser - appliance
        singledesk - desk
    )

    ; Begin init
    (:init
		(agent_at robot singledeskroom)
		(agent_hand_free robot)
		(appliance_at stove singledeskroom)
		(appliance_at toaster singledeskroom)
		(appliance_at water_dispenser singledeskroom)
		(appliance_on stove)
		(appliance_on water_dispenser)
		(boiled kettle)
		(cooked bread)
		(is_bread bread)
		(is_cup_ramen cup_ramen)
		(is_desk singledesk)
		(is_kettle kettle)
		(is_stove stove)
		(is_toaster toaster)
		(is_water_dispenser water_dispenser)
		(item_accessible bread)
		(item_accessible cup_ramen)
		(item_accessible kettle)
		(item_accessible singledesk)
		(item_accessible stove)
		(item_accessible toaster)
		(item_accessible water_dispenser)
		(item_at cup_ramen singledeskroom)
		(item_at singledesk singledeskroom)
		(item_on bread singledesk)
		(item_on kettle singledesk)
		(item_pickable bread)
		(item_pickable cup_ramen)
		(item_pickable kettle)
    )
    ; End init

    ; Begin goal
(:goal
       (cooked cup_ramen)
   )
    ; End goal
)
