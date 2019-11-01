
    #print(pb.a)
    #print(pb.p)
    #print(pb.l)
    #print(pb.c)

    print("##################")
    #initial state for testing
    state = pb.initial
    print("---STATE---")
    print(state)
    print()


    actions = pb.actions(state)
    print("---ACTIONS---")
    print(actions)
    print()

    print("---ACTION---")
    action = actions[0]
    print(action)
    print()

    print("---NEW STATE----")
    new_state = pb.result(state,action)
    print(new_state)
##### round 2
    print()
    actions = pb.actions(new_state)
    print(actions)

    action = actions[1]

    new_state = pb.result(new_state,action)

    print(new_state)
