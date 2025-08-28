; Header and description
(define (domain exhousework)

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

        (loose ?i - item) 

        (cooked ?i - item)
        (boiled ?i - item)
        (cooked ?i - item)

        (is_bread ?i - item)
        (is_toaster ?ap - appliance)
        (is_kettle ?i - item)
        (is_stove ?ap - appliance)
        (is_cup_ramen ?i - item)
        (is_water_dispenser ?ap - appliance)
        (is_desk ?c - container)
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
            (loose ?i - item) 
        )
        :effect (and
            (not (item_at ?i ?r))
            (not (agent_hand_free ?a))
            (agent_has_item ?a ?i)
            (not (loose ?i - item))
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
            (not (loose ?i - item))
        )
        :effect (and
            (not (item_in ?i ?ap))
            (not (agent_hand_free ?a))
            (agent_has_item ?a ?i)
        )
    )

    (:action place_on_container
        :parameters (?a - agent ?i - item ?c - container ?r - room)
        :precondition (and
            (agent_at ?a ?r)
            (container_at ?c ?r)
            (not (item_on ?i ?c))
            (agent_has_item ?a ?i)
            (not (loose ?i - item))
        )
        :effect (and
            (not (agent_has_item ?a ?i))
            (agent_hand_free ?a)
            (item_on ?i ?c)
        )
    )
    
    (:action place_in_appliance
        :parameters (?a - agent ?i - item ?ap - appliance ?r - room)
        :precondition (and
            (agent_at ?a ?r)
            (not (item_in ?i ?ap))
            (appliance_at ?ap ?r)
            (agent_has_item ?a ?i)
            (not (loose ?i - item))
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
            (item_in ?i ?ap)
            (appliance_at ?ap ?r)
            (is_bread ?i)
            (is_toaster ?ap)
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
            (item_in ?i ?ap)
            (appliance_at ?ap ?r)
            (is_kettle ?i)
            (is_stove ?ap)
            (appliance_on ?ap)
            (not (boiled ?i))
        )
        :effect (and
            (boiled ?i)
        )
    )

    (:action wait_cook_ramen
        :parameters (?a - agent ?i - item ?ap - appliance ?r - room)
        :precondition (and
            (agent_at ?a ?r)
            (item_in ?i ?ap)
            (appliance_at ?ap ?r)
            (is_cup_ramen ?i)
            (is_water_dispenser ?ap)
            (appliance_on ?ap)
            (not (cooked ?i))
        )
        :effect (and
            (cooked ?i)
        )
    )
    ; End actions
)