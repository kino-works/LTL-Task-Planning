; Header and description
(define (domain exhousework)

    (:requirements :strips :typing :adl)

    ; Begin types
    (:types
        agent room item surface - object
    )
    ; End types

    ; Begin predicates
    (:predicates
        (agent_at ?a - agent ?r - room)
        (agent_hand_free ?a - agent)
        (agent_has_item ?a - agent ?i - item)

        (item_at ?i - item ?r - room)
        (item_on ?i - item ?s - surface)
        (item_in ?i - item ?ap - item)

        (item_accessible ?i - item)
        (item_pickable ?i - item)

        (neighbor ?r1 - room ?r2 - room)

        (is_bread ?i - item)
        (is_toaster ?i - item)
        (is_kettle ?i - item)
        (is_stove ?i - item)
        (is_cup_ramen ?i - item)
        (is_water_dispenser ?i - item)
        (is_desk ?s - surface)

        (toasted ?i - item)
        (boiled ?i - item)
        (cooked ?i - item)
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

    (:action pickfromappliance
        :parameters (?a - agent ?i - item ?ap - item ?r - room)
        :precondition (and
            (agent_at ?a ?r)
            (item_in ?i ?ap)
            (item_at ?ap ?r)
            (item_accessible ?ap)
            (agent_hand_free ?a)
            (not (appliance_on ?ap))
        )
        :effect (and
            (not (item_in ?i ?ap))
            (not (agent_hand_free ?a))
            (agent_has_item ?a ?i)
        )
    )

    (:action placeonsurface
        :parameters (?a - agent ?i - item ?s - surface ?r - room)
        :precondition (and
            (agent_at ?a ?r)
            (agent_has_item ?a ?i)
            (item_at ?s ?r)    ; 표면이 있는 방
        )
        :effect (and
            (not (agent_has_item ?a ?i))
            (agent_hand_free ?a)
            (item_on ?i ?s)
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

    (:action toast_bread
        :parameters (?a - agent ?b - item ?t - item ?r - room)
        :precondition (and
            (agent_at ?a ?r)
            (item_in ?b ?t)
            (is_bread ?b)
            (is_toaster ?t)
            (appliance_on ?t)
            (not (toasted ?b))
        )
        :effect (and
            (toasted ?b)
        )
    )

    (:action boil_water
        :parameters (?a - agent ?k - item ?s - item ?r - room)
        :precondition (and
            (agent_at ?a ?r)
            (item_at ?k ?r)
            (is_kettle ?k)
            (item_at ?s ?r)
            (is_stove ?s)
            (appliance_on ?s)
            (not (boiled ?k))
        )
        :effect (and
            (boiled ?k)
        )
    )

    (:action cook_ramen
        :parameters (?a - agent ?cr - item ?wd - item ?r - room)
        :precondition (and
            (agent_at ?a ?r)
            (item_at ?cr ?r)
            (is_cup_ramen ?cr)
            (item_at ?wd ?r)
            (is_water_dispenser ?wd)
            (appliance_on ?wd)
            (not (cooked ?cr))
        )
        :effect (and
            (cooked ?cr)
        )
    )
    ; End actions
)
