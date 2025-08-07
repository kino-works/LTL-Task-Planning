(define (problem home_housework)
    (:domain housework)

    ; Begin objects
    (:objects
        robot - agent
        kitchen bathroom bedroom livingroom - room
        food water_bottle eggs - item
        microwave egg_container - appliance
        desk - desk
    )

    ; Begin init
    (:init
		(agent_at robot kitchen)
		(agent_hand_free robot)
		(appliance_at egg_container kitchen)
		(appliance_at microwave kitchen)
		(appliance_on microwave)
		(heated food)
		(is_desk desk)
		(is_microwave microwave)
		(item_accessible desk)
		(item_accessible egg_container)
		(item_accessible eggs)
		(item_accessible food)
		(item_accessible microwave)
		(item_accessible water_bottle)
		(item_at desk livingroom)
		(item_at eggs kitchen)
		(item_at water_bottle kitchen)
		(item_in food microwave)
		(item_pickable eggs)
		(item_pickable food)
		(item_pickable water_bottle)
		(neighbor kitchen livingroom)
		(neighbor livingroom kitchen)
    )
    ; End init

    ; Begin goal
(:goal
       (item_on food desk)
   )
    ; End goal
)
