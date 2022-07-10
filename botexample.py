from Whatsapp.bot import Client

bot = Client(prefix="!",ever_connection=True, location="./")


@bot.event("message")
def teste(message):
    print(message)


@bot.event("ready")
def online_heheh(user):
    print("conectado com sucesso\nUsuario: {0}\nDescrição: {1}\n".format(user.user.username,user.user.description))


bot.run()
