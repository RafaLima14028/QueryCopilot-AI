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

        query = """
        SELECT 
            table_schema, 
            table_name, 
            column_name, 
            data_type, 
            is_nullable
        FROM 
            information_schema.columns
        WHERE 
            table_schema NOT IN ('information_schema', 'pg_catalog')
        ORDER BY 
            table_name, ordinal_position;
        """

        result = await remote_db.execute_query(query=query)

        if not result:
            return "O schema está vazio ou não foi possível acesá-lo"

        schema_text = "Estrutura do Banco de Dados:\n"
        for row in result:
            schema_text += f"Tabela: {row['table_name']} | Coluna: {row['column_name']} | Tipo: {row['data_type']} | Nulável: {row['is_nullable']}\n"

        return schema_text

    return get_schema
