(define (problem home_housework)
    (:domain housework)

    ; Begin objects
    (:objects
        robot - agent
        kitchen bathroom bedroom livingroom - room
        food water_bottle eggs - item
        microwave - appliance
        egg_container - container
        desk - surface
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
        (item_at microwave kitchen)
        (item_at water_bottle kitchen)
        (item_at eggs kitchen)
        (item_at egg_container kitchen)
        (item_at desk livingroom)

        ; Attributes
        (item_accessible food)
        (item_pickable food)
        (item_accessible microwave)
        (item_accessible water_bottle)
        (item_pickable water_bottle)
        (item_accessible eggs)
        (item_pickable eggs)
        (item_accessible egg_container)
        (item_accessible desk)

        (is_microwave microwave)

        (not (heated food))
        (not (appliance_on microwave))
    )
    ; End init

    ; Begin goal
    (:goal (and
        (heated food)
        (item_on food desk)
        (item_on water_bottle desk)
        (item_stored eggs egg_container)
    ))
    ; End goal
)
