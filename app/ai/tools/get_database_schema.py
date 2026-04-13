from app.schemas.query import UserDbData
from app.services.database_executor import RemoteDatabaseService
from app.models.users_db import UserDB


def get_database_schema(user_db: UserDB):
    """
    Consulta o banco de dados para obter o schema atualizado, 
    incluindo tabelas, colunas, tipos de dados e nulidade.
    Use esta ferramenta sempre que precisar conhecer a estrutura do banco antes de gerar SQL.
    """
    async def get_schema() -> str:
        remote_db = RemoteDatabaseService(
            UserDbData(
                db_name=user_db.db_name,
                db_password=user_db.db_password_cryp,
                db_host=user_db.db_host,
                db_port=user_db.db_port,
                db_user=user_db.db_user,
                db_ssl_mode=user_db.db_ssl_mode
            )
        )

        schema_dict = await remote_db.get_db_schema()

        schema_text = "Estrutura do Banco de Dados:\n"

        for table, columns in schema_dict["tables"].items():
            for col in columns:
                schema_text += (
                    f"Tabela: {table} | "
                    f"Coluna: {col["column_type"]} | "
                    f"Tipo: {col["data_type"]}"
                    f"Nulável: {"SIM" if col["is_nullable"] else "NÃO"}\n"
                )

        return schema_text

    return get_schema
