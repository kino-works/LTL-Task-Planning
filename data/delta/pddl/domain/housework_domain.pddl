; Header and description 
(define (domain housework)
    (:requirements :strips :typing :adl)

    ; Begin types
    (:types
        agent room item - object
        container appliance - item
    )
    ; End types

    ; Begin predicates
    (:predicates
        (agent_at ?a - agent ?r - room)
        (agent_hand_free ?a - agent)
        (agent_has_item ?a - agent ?i - item)

        (item_at ?i - item ?r - room)
        (item_on ?i - item ?c - container)
        (item_in ?i - item ?ap - appliance)
        
        (item_accessible ?i - item)
        (item_pickable ?i - item)

        (appliance_on ?ap - appliance)
        (appliance_at ?ap - appliance ?r - room)
        
        (container_at ?c - container ?r - room)

        (neighbor ?r1 - room ?r2 - room)

        (is_bread ?i - item)
        (is_kettle ?i - item)
        (is_cup_ramen ?i - item)
        (is_food ?i - item)
        (is_water_bottle ?i - item)
        (is_eggs ?i - item)
        (is_clothes ?i - item)
        (is_dishcloth ?i - item)
        (is_phone ?i - item)

        (is_microwave ?ap - appliance)
        (is_toaster ?ap - appliance)
        (is_induction ?ap - appliance)
        (is_stove ?ap - appliance)
        (is_washing_machine ?ap - appliance)
        (is_egg_container ?ap - appliance)
        (is_charger ?ap - appliance)
        (is_water_dispenser ?ap - appliance)
        (is_lightswitch ?ap - appliance)

        (is_shelf ?c - container)
        (is_desk ?c - container)

        (heated ?i - item)
        (cooked ?i - item)
        (boiled ?i - item)
        (washed ?i - item)
        (charged ?i - item)
        (clean_desk ?i - item)
        (clean_cloth ?i - item)
    )
    ; End predicates

    ; Begin actions
    (:action goto
        :parameters (?a - agent ?from - room ?to - room)
        :precondition (and
            (agent_at ?a ?from)
            (neighbor ?from ?to)
        )
        :effect (and
            (not (agent_at ?a ?from))
            (agent_at ?a ?to)
        )
    )

    (:action pick_from_room
        :parameters (?a - agent ?i - item ?r - room)
        :precondition (and
            (agent_at ?a ?r)
            (item_at ?i ?r)
            (item_accessible ?i)
            (item_pickable ?i)
            (agent_hand_free ?a)
        )
        :effect (and
            (not (item_at ?i ?r))
            (not (agent_hand_free ?a))
            (agent_has_item ?a ?i)
        )
    )

    (:action pick_from_appliance
        :parameters (?a - agent ?i - item ?ap - appliance ?r - room)
        :precondition (and
            (agent_at ?a ?r)
            (agent_hand_free ?a)
            (item_in ?i ?ap)
            (appliance_at ?ap ?r)
            (item_accessible ?i)
            (item_pickable ?i)
        )
        :effect (and
            (not (item_in ?i ?ap))
            (not (agent_hand_free ?a))
            (agent_has_item ?a ?i)
        )
    )
    (:action pick_from_container
        :parameters (?a - agent ?i - item ?c - container ?r - room)
        :precondition (and
            (agent_at ?a ?r)
            (agent_hand_free ?a)
            (container_at ?c ?r)
            (item_on ?i ?s)
            (is_desk ?s)
            (item_accessible ?i)
            (item_pickable ?i)
        )
        :effect (and
            (not (item_on ?i ?s))
            (not (agent_hand_free ?a))
            (agent_has_item ?a ?i)
        )
    )
    
    (:action place_on_container
        :parameters (?a - agent ?i - item ?c - container ?r - room)
        :precondition (and
            (agent_at ?a ?r)
            (container_at ?c ?r)
            (not (item_on ?i ?s))
            (agent_has_item ?a ?i)
        )
        :effect (and
            (not (agent_has_item ?a ?i))
            (agent_hand_free ?a)
            (item_on ?i ?s)
        )
    )
    
    (:action place_in_appliance
        :parameters (?a - agent ?i - item ?ap - appliance ?r - room)
        :precondition (and
            (agent_at ?a ?r)
            (appliance_at ?ap ?r)
            (not (item_in ?i ?ap))
            (agent_has_item ?a ?i)
        )
        :effect (and
            (not (agent_has_item ?a ?i))
            (agent_hand_free ?a)
            (item_in ?i ?ap)
        )
    )

    (:action turn_on_appliance
        :parameters (?a - agent ?ap - appliance ?r - room)
        :precondition (and
            (agent_at ?a ?r)
            (appliance_at ?ap ?r)
            (not (appliance_on ?ap))
        )
        :effect (and
            (appliance_on ?ap)
        )
    )

    (:action turn_off_appliance
        :parameters (?a - agent ?ap - appliance ?r - room)
        :precondition (and
            (agent_at ?a ?r)
            (appliance_at ?ap ?r)
            (appliance_on ?ap)
        )
        :effect (and
            (not (appliance_on ?ap))
        )
    )

    (:action wait_cook_bread
        :parameters (?a - agent ?i - item ?ap - appliance ?r - room)
        :precondition (and
            (agent_at ?a ?r)
            (appliance_at ?ap ?r)
            (item_in ?i ?ap)
            (appliance_on ?ap)
            (not (cooked ?i))
        )
        :effect (and
            (cooked ?i)
        )
    )
    (:action wait_boil_water
        :parameters (?a - agent ?i - item ?ap - appliance ?r - room)
        :precondition (and
            (agent_at ?a ?r)
            (appliance_at ?ap ?r)
            (item_in ?i ?ap)
            (appliance_on ?ap)
            (not (boiled ?i))
        )
        :effect (and
            (boiled ?i)
        )
    )
    
    (:action wait_heat_pot
        :parameters (?a - agent ?i - item ?ap - appliance ?r - room)
        :precondition (and
            (agent_at ?a ?r)
            (appliance_at ?ap ?r)
            (item_in ?i ?ap)
            (appliance_on ?ap)
            (not (heated ?i))
        )
        :effect (and
            (heated ?i)
        )
    )
    
    (:action wait_wash_clothes
        :parameters (?a - agent ?i - item ?ap - appliance ?r - room)
        :precondition (and
            (agent_at ?a ?r)
            (item_in ?i ?ap)
            (is_washing_machine ?ap)
            (appliance_at ?ap ?r)
            (appliance_on ?ap)
            (not (clean_cloth ?i))
        )
        :effect (and
            (clean_cloth ?i)
        )
    )

    (:action wait_cook_ramen
        :parameters (?a - agent ?i - item ?ap - appliance ?r - room)
        :precondition (and
            (agent_at ?a ?r)
            (appliance_at ?ap ?r)
            (item_in ?i ?ap)
            (appliance_on ?ap)
            (not (cooked ?i))
        )
        :effect (and
            (cooked ?i)
        )
    )

    (:action wait_heat_food
        :parameters (?a - agent ?i - item ?ap - appliance ?r - room)
        :precondition (and
            (agent_at ?a ?r)
            (item_in ?i ?ap)
            (appliance_at ?ap ?r)
            (is_microwave ?ap)
            (appliance_on ?ap)
            (not (heated ?i))
        )
        :effect (and
            (heated ?i)
        )
    )

    (:action wait_charge_phone
        :parameters (?a - agent ?i - item ?ap - appliance ?r - room)
        :precondition (and
            (agent_at ?a ?r)
            (appliance_at ?ap ?r)
            (item_in ?i ?ap)
            (appliance_on ?ap)
            (not (charged ?i))
        )
        :effect (and
            (charged ?i)
        )
    )

    (:action wipe
      :parameters (?a - agent ?i - item ?c - container ?r - room)
      :precondition (and
            (agent_at ?a ?r)
            (container_at ?c ?r)
            (agent_has_item ?a ?i)
        )
      :effect (clean_desk ?s)
    )
    ; End actions
)
