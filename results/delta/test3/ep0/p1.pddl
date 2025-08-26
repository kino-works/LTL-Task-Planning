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
        ; Connections
        ; (No neighbors in this scene graph)

        ; Positions
        (agent_at robot singledeskroom)
        (agent_hand_free robot)
        (item_at food singledeskroom)
        (item_at water_bottle singledeskroom)
        (item_at eggs singledeskroom)
        (item_at singledesk singledeskroom)
        (appliance_at microwave singledeskroom)
        (appliance_at egg_container singledeskroom)

        ; Attributes
        (item_accessible food)
        (item_pickable food)
        (item_accessible microwave)
        (item_accessible water_bottle)
        (item_pickable water_bottle)
        (item_accessible eggs)
        (item_pickable eggs)
        (item_accessible egg_container)
        (item_accessible singledesk)

        (is_microwave microwave)
        (is_desk singledesk)
    )
    ; End init

    ; Begin goal
(:goal
       (heated food)
   )
    ; End goal
)
