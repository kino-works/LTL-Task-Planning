(define (problem innerhouse_housework)
    (:domain housework)

    ; Begin objects
    (:objects
        robot - agent
        kitchen bathroom bedroom livingroom - room
        food water_bottle eggs - item
        microwave egg_container - appliance
        livingroom_desk - desk
    )

    ; Begin init
    (:init
		(agent_at robot kitchen)
		(agent_hand_free robot)
		(appliance_at egg_container kitchen)
		(appliance_at microwave kitchen)
		(appliance_on microwave)
		(heated food)
		(is_desk livingroom_desk)
		(is_microwave microwave)
		(item_accessible egg_container)
		(item_accessible eggs)
		(item_accessible food)
		(item_accessible livingroom_desk)
		(item_accessible microwave)
		(item_accessible water_bottle)
		(item_at eggs kitchen)
		(item_at livingroom_desk livingroom)
		(item_on food livingroom_desk)
		(item_on water_bottle livingroom_desk)
		(item_pickable eggs)
		(item_pickable food)
		(item_pickable water_bottle)
		(neighbor bathroom kitchen)
		(neighbor bathroom livingroom)
		(neighbor bedroom kitchen)
		(neighbor bedroom livingroom)
		(neighbor kitchen bathroom)
		(neighbor kitchen bedroom)
		(neighbor kitchen livingroom)
		(neighbor livingroom bathroom)
		(neighbor livingroom bedroom)
		(neighbor livingroom kitchen)
    )
    ; End init

    ; Begin goal
(:goal
       (item_in eggs egg_container)
   )
    ; End goal
)
