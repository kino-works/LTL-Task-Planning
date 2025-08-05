(define (problem home_housework)
    (:domain housework)

    ; Begin objects
    (:objects
        robot - agent
        kitchen bathroom bedroom livingroom - room
        food water_bottle eggs - item
        microwave - appliance
        desk - surface
        egg_container - container
    )

    ; Begin init
    (:init
		(agent_at robot kitchen)
		(agent_hand_free robot)
		(appliance_on microwave)
		(heated food)
		(is_desk desk)
		(is_egg eggs)
		(is_egg_container egg_container)
		(is_food food)
		(is_microwave microwave)
		(is_water_bottle water_bottle)
		(item_accessible desk)
		(item_accessible egg_container)
		(item_accessible eggs)
		(item_accessible food)
		(item_accessible microwave)
		(item_accessible water_bottle)
		(item_at desk livingroom)
		(item_at egg_container kitchen)
		(item_at eggs kitchen)
		(item_at microwave kitchen)
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
(:goal (and (item_at food livingroom)))
    ; End goal
)
