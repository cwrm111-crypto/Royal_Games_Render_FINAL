# Shared balance and real-time updates
Every user has one server-side virtual coin balance in SQLite. Games call WalletService for debits/credits. After room events the server emits `wallet_update` to the user's socket room and includes current `coins` in room player state. This is the shared balance used by all game modes.
