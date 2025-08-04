;Header and description
(define (domain housework)
    (:requirements :strips :typing :adl)

    ; Begin types
    (:types
        agent room item - object
        surface container - item ; Surfaces and containers are specific types of items
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
        :precondition (and (agent_at ?a ?from) (neighbor ?from ?to))
        :effect (and (not (agent_at ?a ?from)) (agent_at ?a ?to))
    )

    (:action pick
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

    (:action turn-on-appliance
        :parameters (?a - agent ?i - item ?r - room)
        :precondition (and
            (agent_at ?a ?r)
            (item_at ?i ?r)
            (is_microwave ?i)
            (not (appliance_on ?i))
        )
        :effect (appliance_on ?i)
    )

    (:action heat-food
        :parameters (?a - agent ?f - item ?m - item ?r - room)
        :precondition (and
            (agent_at ?a ?r)
            (item_at ?f ?r)
            (is_food ?f)
            (item_at ?m ?r)
            (is_microwave ?m)
            (appliance_on ?m)
        )
        :effect (heated ?f)
    )

    (:action place-on-surface
        :parameters (?a - agent ?i - item ?s - surface ?r - room)
        :precondition (and
            (agent_at ?a ?r)
            (item_at ?s ?r)
            (is_desk ?s)
            (agent_loaded ?a)
            (agent_has_item ?a ?i)
        )
        :effect (and
            (not (agent_has_item ?a ?i))
            (not (agent_loaded ?a))
            (item_on ?i ?s)
        )
    )

    (:action store-in-container
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
