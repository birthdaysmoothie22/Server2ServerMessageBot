import discord
import json
import os
from dotenv import load_dotenv

#load environment variables
load_dotenv()

BOT_KEY = os.getenv('BOT_KEY')
CHANNEL_ID_PAIRS = json.loads(os.getenv('CHANNEL_ID_PAIRS'))

sender_channel_ids = []
for sender_id in CHANNEL_ID_PAIRS:
	sender_channel_ids.append(int(sender_id))

# Format message for sending
def format_message(message, original_message):
	sender_message = '**'+message.author.name+'**'
	if original_message:
		sender_message += ' (in reply to **'+original_message.author.name+'**)\n'
		original_message_list = original_message.content.split('\n')
		for line in original_message_list:
			sender_message += '> '+line+'\n'
	else:
		sender_message += '\n'

	sender_message += message.content

	return sender_message

client = discord.Client()

@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
	if message.content == '!channel_id':
		await message.channel.send(message.channel.id)
		return

	# only process messages that are from the sender channel
	if message.channel.id not in sender_channel_ids:
		return

	# if the message is from the bot, dont do anything
	if message.author == client.user:
		return

	# cast message channel id to string so we can compare with channel_id_pairs
	message_channel_id_str = str(message.channel.id)

	# find the receiver channel and send the message to that channel
	receiver_channel = client.get_channel(CHANNEL_ID_PAIRS[message_channel_id_str])

	if message.reference is not None:
		original = await message.channel.fetch_message(id=message.reference.message_id)

		sender_message = format_message(message, original)
		await receiver_channel.send(sender_message)
		return
	
	sender_message = format_message(message, None)
	await receiver_channel.send(sender_message)
	return

client.run(BOT_KEY)
