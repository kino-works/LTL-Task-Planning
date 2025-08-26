(define (problem innerhouse_housework)
    (:domain housework)

    ; Begin objects
    (:objects
        robot - agent
        singledeskroom - room
        bread kettle pot cup_ramen food water_bottle dish_1 dish_2 dish_3 eggs clothes phone dishcloth - item
        induction egg_container toaster stove water_dispenser microwave singledeskroom_lightswitch washing_machine charger - appliance
        singledesk shelf - container
    )
    ; End objects

    ; Begin init
    (:init
        ; Position
        (agent_at robot singledeskroom)
        (agent_hand_free robot)

        (item_on food singledesk)
        (item_on water_bottle singledesk)
        (item_on eggs singledesk)
        (item_on dishcloth singledesk)
        (item_on clothes singledesk)
        (item_on phone singledesk)
        (item_on bread singledesk)
        (item_on cup_ramen singledesk)
        (item_on kettle singledesk)
        (item_on pot singledesk)
        (item_on dish_1 singledesk)
        (item_on dish_2 singledesk)
        (item_on dish_3 singledesk)

        (appliance_at microwave singledeskroom)
        (appliance_at toaster singledeskroom)
        (appliance_at induction singledeskroom)
        (appliance_at stove singledeskroom)
        (appliance_at egg_container singledeskroom)
        (appliance_at water_dispenser singledeskroom)
        (appliance_at washing_machine singledeskroom)
        (appliance_at charger singledeskroom)
        (appliance_at singledeskroom_lightswitch singledeskroom)

        (container_at singledesk singledeskroom)
        (container_at shelf singledeskroom)

        ; Attributes
        (item_accessible food)
        (item_pickable food)
        (item_accessible water_bottle)
        (item_pickable water_bottle)
        (item_accessible eggs)
        (item_pickable eggs)
        (item_accessible dishcloth)
        (item_pickable dishcloth)
        (item_accessible clothes)
        (item_pickable clothes)
        (item_accessible phone)
        (item_pickable phone)
        (item_accessible bread)
        (item_pickable bread)
        (item_accessible cup_ramen)
        (item_pickable cup_ramen)
        (item_accessible kettle)
        (item_pickable kettle)
        (item_accessible pot)
        (item_pickable pot)
        (item_accessible dish_1)
        (item_pickable dish_1)
        (item_accessible dish_2)
        (item_pickable dish_2)
        (item_accessible dish_3)
        (item_pickable dish_3)

        (item_accessible microwave)
        (item_accessible egg_container)
        (item_accessible toaster)
        (item_accessible induction)
        (item_accessible stove)
        (item_accessible water_dispenser)
        (item_accessible washing_machine)
        (item_accessible charger)
        (item_accessible singledeskroom_lightswitch)
        (item_accessible singledesk)

        (is_food food)
        (is_water_bottle water_bottle)
        (is_eggs eggs)
        (is_dishcloth dishcloth)
        (is_clothes clothes)
        (is_phone phone)

        (is_microwave microwave)
        (is_toaster toaster)
        (is_induction induction)
        (is_stove stove)
        (is_washing_machine washing_machine)
        (is_egg_container egg_container)
        (is_charger charger)
        (is_water_dispenser water_dispenser)
        (is_lightswitch singledeskroom_lightswitch)

        (is_desk singledesk)
        (is_shelf shelf)

    )
    ; End init

    ; Begin goal
    (:goal (and
        (cooked bread)
        (item_on bread singledesk)
        (boiled kettle)
        (item_on kettle singledesk)
        (heated pot)
        (item_on pot singledesk)
        (clean_cloth clothes)
        (cooked cup_ramen)
        (item_on cup_ramen singledesk)
        (heated food)
        (item_on food singledesk)
        (charged phone)
        (item_on phone singledesk)
        (item_on water_bottle singledesk)
        (clean_desk singledesk)
        (item_on dish_1 shelf)
        (item_on dish_2 shelf)
        (item_on dish_3 shelf)
        (item_in eggs egg_container)
    ))
    ; End goal
)
