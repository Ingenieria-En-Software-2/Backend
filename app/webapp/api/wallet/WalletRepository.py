from ...repositories.CrudRepository import CrudRepository
from ...auth.models import db, Wallet
from .schemas import Wallet_Schema, Update_Wallet_Schema, Get_Wallet_Schema

class WalletRepository(CrudRepository):
    """
    A repository for managing Acc objects.
    """

    def __init__(
        self,
        db,
        update_schema=Update_Wallet_Schema,
    ):
        super().__init__(Wallet, db, Update_Wallet_Schema)

    def get_wallets(self):
        """Get all wallets.

        :return: All wallets
        """
        return self.db.session.query(Wallet).all()
    
    def get_wallet_by_id(self, id):
        """
        Gets a account holder by user_id.

        :param user_id: The id of the user to retrieve.
        :return: The user with the specified id, or `None` if no user was
                 found or is not accountholder.
        """
        return (
            self.db.session.query(Wallet)
            .filter(Wallet.id == id)
            .first()
        )