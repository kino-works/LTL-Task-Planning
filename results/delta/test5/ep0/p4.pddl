(define (problem dualdeskroom_housework)
    (:domain housework)

    ; Begin objects
    (:objects
        robot - agent
        dualdeskroom - room
        food water_bottle eggs - item
        microwave egg_container - appliance
        dualdesk_1 dualdesk_2 - desk
    )

    ; Begin init
    (:init
		(agent_at robot dualdeskroom)
		(agent_hand_free robot)
		(appliance_at egg_container dualdeskroom)
		(appliance_at microwave dualdeskroom)
		(appliance_on microwave)
		(heated food)
		(is_desk dualdesk_1)
		(is_desk dualdesk_2)
		(is_microwave microwave)
		(item_accessible dualdesk_1)
		(item_accessible dualdesk_2)
		(item_accessible egg_container)
		(item_accessible eggs)
		(item_accessible food)
		(item_accessible microwave)
		(item_accessible water_bottle)
		(item_at dualdesk_1 dualdeskroom)
		(item_at dualdesk_2 dualdeskroom)
		(item_at eggs dualdeskroom)
		(item_on food dualdesk_1)
		(item_on water_bottle dualdesk_1)
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
