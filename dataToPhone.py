from twilio.rest import Client

account_sid = 'ACad664cd9ce3589929d44850af2f431c6'
auth_token = 'b90c63bbaa00b3e094b332ae0e4ec88f'
client = Client(account_sid, auth_token)

message = client.messages.create(
  from_='+18556161034',
  body='Alert this person is a potential threat',
  to='+14043999109'
)

print(message.sid)
