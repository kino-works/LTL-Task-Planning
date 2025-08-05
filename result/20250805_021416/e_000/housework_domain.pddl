(define (domain housework)

    (:requirements :strips :typing :adl)

    ; Begin types
    (:types
        agent room item container - object
    )
    ; End types

    ; Begin predicates
    (:predicates
        (agent_at ?a - agent ?r - room)
        (agent_hand_free ?a - agent)
        (agent_has_item ?a - agent ?i - item)

        (item_at ?i - item ?r - room)
        (item_in ?i - item ?ap - item)
        (item_accessible ?i - item)
        (item_pickable ?i - item)

        (neighbor ?r1 - room ?r2 - room)

        (is_food ?i - item)
        (is_microwave ?i - item)
        (is_container ?c - container)

        (heated ?i - item)
        (appliance_on ?i - item)
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
            (agent_hand_free ?a)
        )
        :effect (and
            (not (item_at ?i ?r))
            (not (agent_hand_free ?a))
            (agent_has_item ?a ?i)
        )
    )

    (:action placeinappliance
        :parameters (?a - agent ?i - item ?ap - item ?r - room)
        :precondition (and
            (agent_at ?a ?r)
            (agent_has_item ?a ?i)
            (item_at ?ap ?r)
            (item_accessible ?ap)
            (not (appliance_on ?ap))
        )
        :effect (and
            (not (agent_has_item ?a ?i))
            (agent_hand_free ?a)
            (item_in ?i ?ap)
        )
    )

    (:action heat_food
        :parameters (?a - agent ?f - item ?m - item ?r - room)
        :precondition (and
            (agent_at ?a ?r)
            (item_in ?f ?m)
            (is_food ?f)
            (is_microwave ?m)
            (appliance_on ?m)
            (not (heated ?f))
        )
        :effect (and
            (heated ?f)
        )
    )

    (:action store_item
        :parameters (?a - agent ?i - item ?c - container ?r - room)
        :precondition (and
            (agent_at ?a ?r)
            (agent_has_item ?a ?i)
            (item_at ?c ?r)
            (is_container ?c)
        )
        :effect (and
            (not (agent_has_item ?a ?i))
            (agent_hand_free ?a)
            (item_in ?i ?c)
        )
    )

    (:action turnon
        :parameters (?a - agent ?i - item ?r - room)
        :precondition (and
            (agent_at ?a ?r)
            (item_at ?i ?r)
            (item_accessible ?i)
            (agent_hand_free ?a)
            (not (appliance_on ?i))
        )
        :effect (and
            (appliance_on ?i)
        )
    )

    (:action turnoff
        :parameters (?a - agent ?i - item ?r - room)
        :precondition (and
            (agent_at ?a ?r)
            (item_at ?i ?r)
            (item_accessible ?i)
            (agent_hand_free ?a)
            (appliance_on ?i)
        )
        :effect (and
            (not (appliance_on ?i))
        )
    )

    (:action wait
        :parameters (?a - agent)
        :precondition ()
        :effect ()
    )

    ; End actions
)
