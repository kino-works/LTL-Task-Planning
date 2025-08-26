(define (problem inner_house_housework)
    (:domain housework)

    ; Begin objects
    (:objects
        robot - agent
        kitchen bathroom bedroom livingroom - room
        bread kettle cup_ramen - item
        toaster stove water_dispenser - appliance
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
        (item_at bread kitchen)
        (item_at kettle kitchen)
        (item_at cup_ramen kitchen)
        (item_at livingroom_desk livingroom)
        (appliance_at toaster kitchen)
        (appliance_at stove kitchen)
        (appliance_at water_dispenser kitchen)

        ; Attributes
        (item_accessible bread)
        (item_pickable bread)
        (item_accessible toaster)
        (item_accessible kettle)
        (item_pickable kettle)
        (item_accessible stove)
        (item_accessible cup_ramen)
        (item_pickable cup_ramen)
        (item_accessible water_dispenser)
        (item_accessible livingroom_desk)

        (is_bread bread)
        (is_toaster toaster)
        (is_kettle kettle)
        (is_stove stove)
        (is_cup_ramen cup_ramen)
        (is_water_dispenser water_dispenser)
        (is_desk livingroom_desk)
    )
    ; End init

    ; Begin goal
    (:goal (and
        (cooked bread)
        (item_on bread livingroom_desk)
        (boiled kettle)
        (item_on kettle livingroom_desk)
        (cooked cup_ramen)
        (item_on cup_ramen livingroom_desk)
    ))
    ; End goal
)
