class WalletReconciler:
    def reconcile(self, opening, entries):
        return int(opening)+sum(int(e.amount) for e in entries)
