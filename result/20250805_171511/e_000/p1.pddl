(define (problem home_housework)
    (:domain housework)

    ; Begin objects
    (:objects
        robot - agent
        kitchen livingroom bathroom bedroom - room
        food water_bottle eggs - item
        microwave - appliance
        desk - surface
        egg_container - container
    )

    ; Begin init
    (:init
		
    )
    ; End init

    ; Begin goal
(:goal
       (heated food)
   )
    ; End goal
)
