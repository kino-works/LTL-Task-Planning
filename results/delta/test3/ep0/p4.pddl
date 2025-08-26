(define (problem singledeskroom_housework)
    (:domain housework)

    ; Begin objects
    (:objects
        robot - agent
        singledeskroom - room
        food water_bottle eggs - item
        microwave egg_container - appliance
        singledesk - desk
    )

    ; Begin init
    (:init
		(agent_at robot singledeskroom)
		(agent_hand_free robot)
		(appliance_at egg_container singledeskroom)
		(appliance_at microwave singledeskroom)
		(appliance_on microwave)
		(heated food)
		(is_desk singledesk)
		(is_microwave microwave)
		(item_accessible egg_container)
		(item_accessible eggs)
		(item_accessible food)
		(item_accessible microwave)
		(item_accessible singledesk)
		(item_accessible water_bottle)
		(item_at eggs singledeskroom)
		(item_at singledesk singledeskroom)
		(item_on food singledesk)
		(item_on water_bottle singledesk)
		(item_pickable eggs)
		(item_pickable food)
		(item_pickable water_bottle)
    )
    ; End init

    ; Begin goal
(:goal
       (item_in eggs egg_container)
   )
    ; End goal
)
