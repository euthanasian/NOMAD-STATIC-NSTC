from wallet import Wallet
from blockchain import Blockchain

coin = Blockchain()

alice = Wallet()
bob = Wallet()
miner = Wallet()

alice_addr = alice.public_key.to_string().hex()
bob_addr = bob.public_key.to_string().hex()
miner_addr = miner.public_key.to_string().hex()

print("\nMINER:", miner_addr)

print("\n--- ADDRESSES ---")
print("ALICE:", alice_addr)
print("BOB:", bob_addr)

# SYSTEM → Alice
coin.add_transaction("SYSTEM", alice_addr, 100, None)

# Alice → Bob
msg = f"{alice_addr}{bob_addr}30"
sig = alice.sign(msg)
coin.add_transaction(alice_addr, bob_addr, 30, sig)

# Bob → Alice
msg2 = f"{bob_addr}{alice_addr}10"
sig2 = bob.sign(msg2)
coin.add_transaction(bob_addr, alice_addr, 10, sig2)

print("\n⛏ MINING START")

# майним ВСЕ транзакции по очереди
while coin.mempool:
    coin.mine_block(miner_addr)

print("\n--- BALANCES ---")
print("ALICE:", coin.get_balance(alice_addr))
print("BOB:", coin.get_balance(bob_addr))
print("MINER:", coin.get_balance(miner_addr))

print("\n--- BLOCKCHAIN ---")
coin.print_chain()

print("\n--- MEMPOOL ---")
coin.print_mempool()