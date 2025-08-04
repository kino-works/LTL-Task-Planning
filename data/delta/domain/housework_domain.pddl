; Header and description 
(define (domain housework)
    (:requirements :strips :typing :adl)

    ; Begin types
    (:types
        agent room item - object
        surface container - item 
    )
    ; End types

    ; Begin predicates
    (:predicates
        (agent_at ?a - agent ?r - room)
        (agent_loaded ?a - agent)         
        (agent_has_item ?a - agent ?i - item)

        (item_at ?i - item ?r - room)
        (item_on ?i - item ?s - surface)
        (item_in ?i - item ?c - container)

        (item_accessible ?i - item)
        (item_pickable ?i - item)
        (heated ?i - item)
        (appliance_on ?i - item)

        (neighbor ?r1 - room ?r2 - room)

        (is_food ?i - item)
        (is_microwave ?i - item)
        (is_water_bottle ?i - item)
        (is_eggs ?i - item)
        (is_desk ?s - surface)
        (is_egg_container ?c - container)
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

    (:action pickfromroom
        :parameters (?a - agent ?i - item ?r - room)
        :precondition (and
            (agent_at ?a ?r)
            (item_at ?i ?r)
            (item_accessible ?i)
            (item_pickable ?i)
            (not (agent_loaded ?a))
        )
        :effect (and
            (not (item_at ?i ?r))
            (agent_loaded ?a)
            (agent_has_item ?a ?i)
        )
    )

    (:action pickfromappliance
        :parameters (?a - agent ?i - item ?ap - item ?r - room)
        :precondition (and
            (agent_at ?a ?r)
            (item_in ?i ?ap)
            (item_at ?ap ?r)
            (item_accessible ?ap)
            (not (appliance_on ?ap))
            (not (agent_loaded ?a))
        )
        :effect (and
            (not (item_in ?i ?ap))
            (agent_loaded ?a)
            (agent_has_item ?a ?i)
        )
    )

    (:action placeonsurface
        :parameters (?a - agent ?i - item ?s - surface ?r - room)
        :precondition (and
            (agent_at ?a ?r)
            (item_at ?s ?r)
            (agent_loaded ?a)
            (agent_has_item ?a ?i)
        )
        :effect (and
            (not (agent_has_item ?a ?i))
            (not (agent_loaded ?a))
            (item_on ?i ?s)
        )
    )

    (:action placeinappliance
        :parameters (?a - agent ?i - item ?ap - item ?r - room)
        :precondition (and
            (agent_at ?a ?r)
            (item_at ?ap ?r)
            (item_accessible ?ap)
            (not (appliance_on ?ap))
            (agent_loaded ?a)
            (agent_has_item ?a ?i)
        )
        :effect (and
            (not (agent_has_item ?a ?i))
            (not (agent_loaded ?a))
            (item_in ?i ?ap)
        )
    )

    (:action turnon
        :parameters (?a - agent ?i - item ?r - room)
        :precondition (and
            (agent_at ?a ?r)
            (item_at ?i ?r)
            (item_accessible ?i)
            (not (agent_loaded ?a))
            (not (appliance_on ?i))
        )
        :effect (appliance_on ?i)
    )

    (:action turnoff
        :parameters (?a - agent ?i - item ?r - room)
        :precondition (and
            (agent_at ?a ?r)
            (item_at ?i ?r)
            (item_accessible ?i)
            (not (agent_loaded ?a))
            (appliance_on ?i)
        )
        :effect (not (appliance_on ?i))
    )

    (:action wait
        :parameters (?a - agent)
        :precondition ()   
        :effect ()      
    )

    (:action heat_food
        :parameters (?a - agent ?f - item ?m - item ?r - room)
        :precondition (and
            (agent_at ?a ?r)
            (item_in ?f ?m)
            (is_microwave ?m)
            (appliance_on ?m)
        )
        :effect (heated ?f)
    )

    (:action store_item
        :parameters (?a - agent ?i - item ?c - container ?r - room)
        :precondition (and
            (agent_at ?a ?r)
            (item_at ?c ?r)
            (is_egg_container ?c)
            (agent_loaded ?a)
            (agent_has_item ?a ?i)
        )
        :effect (and
            (not (agent_has_item ?a ?i))
            (not (agent_loaded ?a))
            (item_in ?i ?c)
        )
    )
    ; End actions
)
