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
        ; Connections
        (neighbor kitchen livingroom)
        (neighbor livingroom kitchen)

        ; Positions
        (agent_at robot livingroom)
        (agent_hand_free robot)
        (item_at food kitchen)
        (item_at water_bottle kitchen)
        (item_at livingroom_desk livingroom)
        (appliance_at microwave kitchen)

        ; Attributes
        (item_accessible food)
        (item_pickable food)
        (item_accessible microwave)
        (item_accessible water_bottle)
        (item_pickable water_bottle)
        (item_accessible livingroom_desk)

        (is_microwave microwave)
        (is_desk livingroom_desk)
    )
    ; End init

    ; Begin goal
    (:goal (and
        (heated food)
        (item_on food livingroom_desk)
        (item_on water_bottle livingroom_desk)
    ))
    ; End goal
)
