(define (problem dualdeskroom_housework)
    (:domain housework)

    ; Begin objects
    (:objects
        robot - agent
        dualdeskroom - room
        bread kettle cup_ramen - item
        toaster stove water_dispenser - appliance
        dualdesk_1 dualdesk_2 - desk
    )

    ; Begin init
    (:init
        ; Connections
        ; (No neighbors in this scene graph)

        ; Positions
        (agent_at robot dualdeskroom)
        (agent_hand_free robot)
        (item_at bread dualdeskroom)
        (item_at kettle dualdeskroom)
        (item_at cup_ramen dualdeskroom)
        (item_at dualdesk_1 dualdeskroom)
        (item_at dualdesk_2 dualdeskroom)
        (appliance_at toaster dualdeskroom)
        (appliance_at stove dualdeskroom)
        (appliance_at water_dispenser dualdeskroom)

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
        (item_accessible dualdesk_1)
        (item_accessible dualdesk_2)

        (is_bread bread)
        (is_toaster toaster)
        (is_kettle kettle)
        (is_stove stove)
        (is_cup_ramen cup_ramen)
        (is_water_dispenser water_dispenser)
        (is_desk dualdesk_1)
        (is_desk dualdesk_2)
    )
    ; End init

    ; Begin goal
(:goal
       (cooked bread)
   )
    ; End goal
)
