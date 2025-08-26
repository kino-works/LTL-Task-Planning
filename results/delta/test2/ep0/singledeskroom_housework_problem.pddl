(define (problem singledeskroom_housework)
    (:domain housework)

    ; Begin objects
    (:objects
        robot - agent
        singledeskroom - room
        bread kettle cup_ramen - item
        toaster stove water_dispenser - appliance
        singledesk - desk
    )

    ; Begin init
    (:init
        ; Connections
        ; No neighbors as there is only one room

        ; Positions
        (agent_at robot singledeskroom)
        (agent_hand_free robot)
        (item_at bread singledeskroom)
        (item_at kettle singledeskroom)
        (item_at cup_ramen singledeskroom)
        (item_at singledesk singledeskroom)
        (appliance_at toaster singledeskroom)
        (appliance_at stove singledeskroom)
        (appliance_at water_dispenser singledeskroom)

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
        (item_accessible singledesk)

        (is_bread bread)
        (is_toaster toaster)
        (is_kettle kettle)
        (is_stove stove)
        (is_cup_ramen cup_ramen)
        (is_water_dispenser water_dispenser)
        (is_desk singledesk)
    )
    ; End init

    ; Begin goal
    (:goal (and
        (cooked bread)
        (item_on bread singledesk)
        (boiled kettle)
        (item_on kettle singledesk)
        (cooked cup_ramen)
        (item_on cup_ramen singledesk)
    ))
    ; End goal
)
