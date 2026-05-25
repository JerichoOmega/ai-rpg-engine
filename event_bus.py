# =========================
# EVENT BUS SYSTEM
# =========================

event_listeners = {}

# =========================
# REGISTER LISTENER
# =========================

def subscribe(

    event_name,
    callback

):

    if event_name not in event_listeners:

        event_listeners[
            event_name
        ] = []

    event_listeners[
        event_name
    ].append(callback)

# =========================
# REMOVE LISTENER
# =========================

def unsubscribe(

    event_name,
    callback

):

    if event_name in event_listeners:

        if (

            callback

            in

            event_listeners[
                event_name
            ]

        ):

            event_listeners[
                event_name
            ].remove(callback)

# =========================
# EMIT EVENT
# =========================

def emit(

    event_name,
    **data

):

    print(
        f"\n[EVENT]"
        f" {event_name}"
    )

    if event_name in event_listeners:

        for callback in event_listeners[
            event_name
        ]:

            callback(data)

# =========================
# DEBUG EVENTS
# =========================

def show_registered_events():

    print(
        "\n=== REGISTERED EVENTS ==="
    )

    if len(event_listeners) == 0:

        print(
            "No events registered."
        )

        return

    for event_name in event_listeners:

        print(
            "\n•",
            event_name
        )

        print(
            "Listeners:",
            len(

                event_listeners[
                    event_name
                ]
            )
        )

# =========================
# CLEAR EVENTS
# =========================

def clear_event_bus():

    event_listeners.clear()

    print(
        "\nEvent bus cleared."
    )