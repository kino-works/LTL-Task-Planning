; Header and description 
(define (domain housework)
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
        (appliance_at ?ap - appliance ?r - room)

        (neighbor ?r1 - room ?r2 - room)

        (is_food ?i - item)
        (is_microwave ?ap - appliance)
        (is_water_bottle ?i - item)
        (is_eggs ?i - item)
        (is_desk ?d - desk)
        (is_egg_container ?ap - appliance)

        (heated ?i - item)
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

    (:action place_on_desk
        :parameters (?a - agent ?i - item ?d - desk ?r - room)
        :precondition (and
            (agent_at ?a ?r)
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

    (:action store_item
        :parameters (?a - agent ?i - item ?ap - appliance ?r - room)
        :precondition (and
            (agent_at ?a ?r)
            (appliance_at ?ap ?r)
            (is_egg_container ?ap)
            (agent_has_item ?a ?i)
        )
        :effect (and
            (not (agent_has_item ?a ?i))
            (item_in ?i ?ap)
            (agent_hand_free ?a)
        )
    )
    ; End actions
)
