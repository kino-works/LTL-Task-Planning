
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

        (is_food food)
        (is_microwave microwave)
        (is_desk desk)
        (is_water_bottle water_bottle)
        (is_egg eggs)
        (is_egg_container egg_container)

        (not (heated food))
        (not (appliance_on microwave))
    )
    ; End init

    ; Begin goal
(:goal (heated food))
    ; End goal
)
