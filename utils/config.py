def fill_messages_with_time(messages):
    max_time = max([msg["time"] + max([dest.get("delay", 0) for dest in msg.get("receivers", [])], default=0) for msg in messages])
    full_messages = []
    
    for t in range(max_time + 1):
        msg_at_time = next((msg for msg in messages if msg["time"] == t), None)
        if msg_at_time:
            full_messages.append(msg_at_time)
        else:
            full_messages.append({"time": t})
    
    return full_messages