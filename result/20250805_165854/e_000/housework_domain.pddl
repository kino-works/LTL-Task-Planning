(define (domain housework)

    (:requirements :strips :typing :adl)

    ; Begin types
    (:types
        agent room item - object
        surface appliance container - item ; Surfaces, appliances, and containers are special types of items
    )
    ; End types

    ; Begin predicates
    (:predicates
        (agent_at ?a - agent ?r - room)
        (agent_hand_free ?a - agent)
        (agent_has_item ?a - agent ?i - item)

        (item_at ?i - item ?r - room)
        (item_on ?i - item ?s - surface)
        (item_in ?i1 - item ?i2 - appliance) ; Represents an item being inside an appliance
        (item_in_container ?i - item ?c - container) ; Represents an item being inside a container

        (item_accessible ?i - item)
        (item_pickable ?i - item)

        (neighbor ?r1 - room ?r2 - room)
        (appliance_on ?app - appliance)

        ; Task-specific states
        (toasted ?i - item)
        (boiled ?i - item)
        (cooked ?i - item)
        (heated ?i - item)
        (clean ?i - item)
        (charged ?i - item)

        ; Item type identification
        (is_bread ?i - item)
        (is_toaster ?i - appliance)
        (is_kettle ?i - item)
        (is_stove ?i - appliance)
        (is_cup_ramen ?i - item)
        (is_water_dispenser ?i - appliance)
        (is_desk ?s - surface)
        (is_microwave ?i - appliance)
        (is_phone ?i - item)
        (is_charger ?i - appliance)
        (is_lightswitch ?i - item)
        (is_egg_container ?c - container)
    )
    ; End predicates

    ; Begin actions
    (:action goto
        :parameters (?a - agent ?from - room ?to - room)
        :precondition (and (agent_at ?a ?from) (neighbor ?from ?to))
        :effect (and (not (agent_at ?a ?from)) (agent_at ?a ?to))
    )

    (:action pick_from_room
        :parameters (?a - agent ?i - item ?r - room)
        :precondition (and (agent_at ?a ?r) (item_at ?i ?r) (item_accessible ?i) (item_pickable ?i) (agent_hand_free ?a))
        :effect (and (not (item_at ?i ?r)) (not (agent_hand_free ?a)) (agent_has_item ?a ?i))
    )

    (:action pick_from_appliance
        :parameters (?a - agent ?i - item ?app - appliance ?r - room)
        :precondition (and (agent_at ?a ?r) (item_in ?i ?app) (not (appliance_on ?app)) (agent_hand_free ?a))
        :effect (and (not (item_in ?i ?app)) (not (agent_hand_free ?a)) (agent_has_item ?a ?i))
    )

    (:action place_on_surface
        :parameters (?a - agent ?i - item ?s - surface ?r - room)
        :precondition (and (agent_at ?a ?r) (item_at ?s ?r) (agent_has_item ?a ?i))
        :effect (and (not (agent_has_item ?a ?i)) (agent_hand_free ?a) (item_on ?i ?s))
    )

    (:action place_in_appliance
        :parameters (?a - agent ?i - item ?app - appliance ?r - room)
        :precondition (and (agent_at ?a ?r) (item_at ?app ?r) (agent_has_item ?a ?i))
        :effect (and (not (agent_has_item ?a ?i)) (agent_hand_free ?a) (item_in ?i ?app))
    )

    (:action turnon
        :parameters (?a - agent ?app - appliance ?r - room)
        :precondition (and (agent_at ?a ?r) (item_at ?app ?r) (not (appliance_on ?app)))
        :effect (appliance_on ?app)
    )

    (:action turnoff
        :parameters (?a - agent ?app - appliance ?r - room)
        :precondition (and (agent_at ?a ?r) (item_at ?app ?r) (appliance_on ?app))
        :effect (not (appliance_on ?app))
    )

    (:action toast_bread
        :parameters (?a - agent ?b - item ?t - appliance ?r - room)
        :precondition (and
            (agent_at ?a ?r) (item_at ?t ?r) (is_toaster ?t)
            (item_in ?b ?t)
            (appliance_on ?t)
            (not (toasted ?b))
        )
        :effect (toasted ?b)
    )

    (:action boil_water
        :parameters (?a - agent ?k - item ?s - appliance ?r - room)
        :precondition (and
            (agent_at ?a ?r) (item_at ?s ?r) (is_stove ?s)
            (item_in ?k ?s)
            (appliance_on ?s)
            (not (boiled ?k))
        )
        :effect (boiled ?k)
    )

    (:action heat_pot
        :parameters (?a - agent ?p - item ?i - appliance ?r - room)
        :precondition (and
            (agent_at ?a ?r) (item_at ?i ?r) (is_microwave ?i)
            (item_in ?p ?i)
            (appliance_on ?i)
            (not (heated ?p))
        )
        :effect (heated ?p)
    )

    (:action wash_clothes
        :parameters (?a - agent ?c - item ?wm - appliance ?r - room)
        :precondition (and
            (agent_at ?a ?r) (item_at ?wm ?r)
            (item_in ?c ?wm)
            (appliance_on ?wm)
            (not (clean ?c))
        )
        :effect (clean ?c)
    )

    (:action cook_ramen
        :parameters (?a - agent ?cr - item ?wd - appliance ?r - room)
        :precondition (and
            (agent_at ?a ?r) (item_at ?wd ?r) (is_water_dispenser ?wd)
            (item_in ?cr ?wd)
            (appliance_on ?wd)
            (not (cooked ?cr))
        )
        :effect (cooked ?cr)
    )

    (:action heat_food
        :parameters (?a - agent ?f - item ?m - appliance ?r - room)
        :precondition (and
            (agent_at ?a ?r) (item_at ?m ?r) (is_microwave ?m)
            (item_in ?f ?m)
            (appliance_on ?m)
            (not (heated ?f))
        )
        :effect (heated ?f)
    )

    (:action charge_phone
        :parameters (?a - agent ?p - item ?c - appliance ?r - room)
        :precondition (and
            (agent_at ?a ?r) (item_at ?c ?r) (is_charger ?c)
            (item_in ?p ?c)
            (appliance_on ?c)
            (not (charged ?p))
        )
        :effect (charged ?p)
    )

    (:action wipe
        :parameters (?a - agent ?cl - item ?s - surface ?r - room)
        :precondition (and (agent_at ?a ?r) (item_on ?s ?r) (agent_has_item ?a ?cl))
        :effect (clean ?s)
    )

    (:action store_in_container
        :parameters (?a - agent ?i - item ?c - container ?r - room)
        :precondition (and (agent_at ?a ?r) (item_at ?c ?r) (agent_has_item ?a ?i))
        :effect (and (not (agent_has_item ?a ?i)) (agent_hand_free ?a) (item_in_container ?i ?c))
    )
    ; End actions
)
