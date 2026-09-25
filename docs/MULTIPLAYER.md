# Multiplayer
Clients emit actions; the server owns room state. Each room broadcasts `game_state`. Player wallets are shared across all games and updated through `wallet_update`.