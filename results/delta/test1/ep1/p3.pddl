(define (problem innerhouse_housework)
    (:domain housework)

    ; Begin objects
    (:objects
        robot - agent
        kitchen bathroom bedroom livingroom - room
        food water_bottle - item
        microwave - appliance
        livingroom_desk - desk
    )

    ; Begin init
    (:init
		(agent_at robot kitchen)
		(agent_hand_free robot)
		(appliance_at microwave kitchen)
		(appliance_on microwave)
		(heated food)
		(is_desk livingroom_desk)
		(is_microwave microwave)
		(item_accessible food)
		(item_accessible livingroom_desk)
		(item_accessible microwave)
		(item_accessible water_bottle)
		(item_at livingroom_desk livingroom)
		(item_at water_bottle kitchen)
		(item_on food livingroom_desk)
		(item_pickable food)
		(item_pickable water_bottle)
		(neighbor kitchen livingroom)
		(neighbor livingroom kitchen)
    )
    ; End init

    ; Begin goal
(:goal
       (item_on water_bottle livingroom_desk)
   )
    ; End goal
)
