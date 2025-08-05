
(define (problem home_housework)
    (:domain housework)

    ; Begin objects
    (:objects
        robot - agent
        kitchen bathroom bedroom livingroom - room
        bread toaster kettle induction cup_ramen water_dispenser food microwave water_bottle dish_1 dish_2 dish_3 eggs - item
        desk - surface
        kitchen_lightswitch bathroom_lightswitch bedroom_lightswitch livingroom_lightswitch - item
        washing_machine - appliance
        clothes phone - item
        charger - appliance
        shelf - surface
        egg_container - container
        dishcloth - item
    )

    ; Begin init
    (:init
        ; Connections
        (neighbor kitchen bathroom)
        (neighbor bathroom kitchen)
        (neighbor kitchen bedroom)
        (neighbor bedroom kitchen)
        (neighbor kitchen livingroom)
        (neighbor livingroom kitchen)
        (neighbor bathroom bedroom)
        (neighbor bedroom bathroom)
        (neighbor bathroom livingroom)
        (neighbor livingroom bathroom)
        (neighbor bedroom livingroom)
        (neighbor livingroom bedroom)

        ; Positions
        (agent_at robot livingroom)
        (agent_hand_free robot)
        (item_at bread kitchen)
        (item_at toaster kitchen)
        (item_at kettle kitchen)
        (item_at induction kitchen)
        (item_at cup_ramen kitchen)
        (item_at water_dispenser kitchen)
        (item_at food kitchen)
        (item_at microwave kitchen)
        (item_at water_bottle kitchen)
        (item_at dish_1 kitchen)
        (item_at dish_2 kitchen)
        (item_at dish_3 kitchen)
        (item_at eggs kitchen)
        (item_at kitchen_lightswitch kitchen)
        (item_at bathroom_lightswitch bathroom)
        (item_at bedroom_lightswitch bedroom)
        (item_at livingroom_lightswitch livingroom)
        (item_at washing_machine bathroom)
        (item_at clothes bedroom)
        (item_at phone bedroom)
        (item_at charger bedroom)
        (item_at desk livingroom)
        (item_at shelf kitchen)
        (item_at egg_container kitchen)
        (item_at dishcloth livingroom)

        ; Attributes
        (item_accessible bread)
        (item_pickable bread)
        (item_accessible toaster)
        (item_accessible kettle)
        (item_pickable kettle)
        (item_accessible induction)
        (item_accessible cup_ramen)
        (item_pickable cup_ramen)
        (item_accessible water_dispenser)
        (item_accessible food)
        (item_pickable food)
        (item_accessible microwave)
        (item_accessible water_bottle)
        (item_pickable water_bottle)
        (item_accessible dish_1)
        (item_pickable dish_1)
        (item_accessible dish_2)
        (item_pickable dish_2)
        (item_accessible dish_3)
        (item_pickable dish_3)
        (item_accessible eggs)
        (item_pickable eggs)
        (item_accessible kitchen_lightswitch)
        (item_accessible bathroom_lightswitch)
        (item_accessible bedroom_lightswitch)
        (item_accessible livingroom_lightswitch)
        (item_accessible washing_machine)
        (item_accessible clothes)
        (item_pickable clothes)
        (item_accessible phone)
        (item_pickable phone)
        (item_accessible charger)
        (item_accessible desk)
        (item_accessible shelf)
        (item_accessible egg_container)
        (item_accessible dishcloth)
        (item_pickable dishcloth)

        (is_bread bread)
        (is_toaster toaster)
        (is_kettle kettle)
        (is_stove induction)
        (is_cup_ramen cup_ramen)
        (is_water_dispenser water_dispenser)
        (is_desk desk)
        (is_microwave microwave)
        (is_phone phone)
        (is_charger charger)
        (is_lightswitch kitchen_lightswitch)
        (is_lightswitch bathroom_lightswitch)
        (is_lightswitch bedroom_lightswitch)
        (is_lightswitch livingroom_lightswitch)
        (is_egg_container egg_container)

        (not (toasted bread))
        (not (boiled kettle))
        (not (cooked cup_ramen))
        (not (heated food))
        (not (clean clothes))
        (not (charged phone))
        (not (clean desk))
        (not (appliance_on toaster))
        (not (appliance_on induction))
        (not (appliance_on water_dispenser))
        (not (appliance_on microwave))
        (not (appliance_on washing_machine))
        (not (appliance_on charger))
    )
    ; End init

    ; Begin goal
(:goal
       (toasted bread)
   )
    ; End goal
)
