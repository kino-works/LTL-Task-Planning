; Header and description
(define (domain exhousework)

    (:requirements :strips :typing :adl)

    ; Begin types
    (:types
        agent room item - object
        desk appliance - item
    )
    ; End types

    ; Begin predicates
    (:predicates
        (agent_at ?a - agent ?r - room)
        (agent_hand_free ?a - agent)
        (agent_has_item ?a - agent ?i - item)

        (item_at ?i - item ?r - room)
        (item_on ?i - item ?d - desk)
        (item_in ?i - item ?ap - appliance) 

        (item_accessible ?i - item)
        (item_pickable ?i - item)

        (appliance_on ?ap - appliance)

        (neighbor ?r1 - room ?r2 - room)

        (toasted ?i - item)
        (boiled ?i - item)
        (cooked ?i - item)

        (is_bread ?i - item)
        (is_toaster ?ap - appliance)
        (is_kettle ?i - item)
        (is_stove ?ap - appliance)
        (is_cup_ramen ?i - item)
        (is_water_dispenser ?ap - appliance)
        (is_desk ?d - desk)
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
        :parameters (?a - agent ?i - item ?ap appliance ?r - room)
        :precondition (and
            (agent_at ?a ?r)
            (agent_hand_free ?a)
            (item_at ?i ?r)
            (item_in ?i ?ap)
            (item_accessible ?i)
            (item_pickable ?i)
        )
        :effect (and
            (not (item_in ?i ?ap))
            (not (agent_hand_free ?a))
            (agent_has_item ?a ?i)
        )
    )

    (:action place_on_desk
        :parameters (?a - agent ?i - item ?d - desk ?r - room)
        :precondition (and
            (agent_at ?a ?r)
            (item_at ?i ?r)
            (not (item_on ?i ?d))
            (agent_has_item ?a ?i)
        )
        :effect (and
            (not (agent_has_item ?a ?i))
            (agent_hand_free ?a)
            (item_on ?i ?d)
        )
    )
    
    (:action place_in_appliance
        :parameters (?a - agent ?i - item ?ap - appliance ?r - room)
        :precondition (and
            (agent_at ?a ?r)
            (item_at ?i ?r)
            (not (item_in ?i ?ap))
            (appliance_at ?ap ?r)
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
            (item_at ?i ?r)
            (not (appliance_on ?ap))
        )
        :effect (appliance_on ?ap)
    )

    (:action turn_off_appliance
        :parameters (?a - agent ?ap - appliance ?r - room)
        :precondition (and
            (agent_at ?a ?r)
            (item_at ?ap ?r)
            (appliance_on ?ap)
        )
        :effect (not (appliance_on ?ap))
    )

    (:action wait_cook_bread
        :parameters (?a - agent ?i - item ?ap - appliance ?r - room)
        :precondition (and
            (agent_at ?a ?r)
            (item_at ?i ?r)
            (is_toaster ?ap)
            (item_in ?i ?ap)
            (appliance_on ?ap)
            (not (toasted ?i))
        )
        :effect (toasted ?i)
    )

    (:action wait_boil_water
        :parameters (?a - agent ?i - item ?ap - appliance ?r - room)
        :precondition (and
            (agent_at ?a ?r)
            (item_at ?i ?r)
            (is_stove ?ap)
            (item_in ?i ?ap)
            (appliance_on ?ap)
            (not (boiled ?i))
        )
        :effect (boiled ?i)
    )

    (:action wait_cook_ramen
        :parameters (?a - agent ?i - item ?ap - appliance ?r - room)
        :precondition (and
            (agent_at ?a ?r)
            (item_at ?i ?r)
            (is_water_dispenser ?ap)
            (item_in ?i ?ap)
            (appliance_on ?ap)
            (not (cooked ?i))
        )
        :effect (cooked ?i)
    )
    ; End actions
)
