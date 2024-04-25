import ngrok

ngrok.set_auth_token("2fb5IKJduHgYmK6HV9S2tz2atGo_A3DBmEsa21eghzektiru")
listener = ngrok.forward(1000)

print(f"Ingress established at {listener.url()}")
print("press Ctrl+C to exit")
while True:
    pass
