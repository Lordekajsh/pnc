# TOKEN do bot
BOT_TOKEN = "5776169197:AAGe9FpcoZMAvcL_mZuzr4_1T7KFEJzCars"

# ID e Hash da API do Telegram. Isso NÃO é o token do bot e não deve ser alterado.
API_ID = 16324978
API_HASH = "8ce32752288177bf1d88bf66ccddd135"

# Chat ID para o chat de compras do cliente.
CLIENT_CHAT = -1001440494253

# ID do chat para logs de compras e adição de saldo
ADMIN_CHAT = -1001279779619

# Lista de IDs de administradores que podem acessar o painel e adicionar novos materiais ao bot.
ADMINS = [5080091404, 5544928399]

# Chat ID para logs de erros
LOG_CHAT = -1001279779619

# Quantidade de tarefas que devem ser tratadas em paralelo. Use valores altos para servidores low-end.
WORKERS = 35

# Lista de IDs de usuários que podem presentear outras pessoas.
GIFTERS = [5544928399]

# Lista de IDs de usuários que têm acesso total ao servidor e podem executar comandos.
SUDOERS = [5080091404, 5544928399]

# Todos os usuários sudoers também devem ser administradores.
ADMINS.extend(SUDOERS)