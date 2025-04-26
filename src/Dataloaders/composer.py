# from typing import Any, Optional, Dict, Type
# from sqlalchemy import select
# from sqlalchemy.sql import Select
# from sqlalchemy.sql.elements import BinaryExpression

# class LoaderComposer:
#     def __init__(self, loader: Any, stmt: Optional[Select] = None) -> None:
#         """
#         :param loader: Instance loaderu, který obsahuje atributy:
#                        - dbmodel: SQLAlchemy model
#                        - stmt: Výchozí select statement (např. select(dbmodel))
#                        - executeselect(stmt: Select): metoda pro vykonání select dotazu
#         :param stmt: SQLAlchemy select statement. Pokud není zadán, použije se loader.stmt.
#         """
#         self.loader = loader
#         loader.composer = self  # Reference zpět do composeru
#         self.stmt: Select = stmt if stmt is not None else loader.stmt

#     def load(self, id: Any) -> Any:
#         """
#         Načte jeden záznam dle id pomocí původní metody loader.load.

#         :param id: Identifikátor záznamu.
#         :return: Výsledek načtení záznamu.
#         """
#         return self.loader.load(id)

#     def filter_by(self, **kwargs: Any) -> "LoaderComposer":
#         """
#         Přidá WHERE podmínky do SQLAlchemy select statementu.
#         Příklad použití: composer.filter_by(id=fid)

#         :param kwargs: Klíčové argumenty odpovídající sloupcům modelu.
#         :return: Nová instance LoaderComposer s rozšířeným select statementem.
#         """
#         model = self.loader.dbmodel
#         new_stmt = self.stmt
#         for key, value in kwargs.items():
#             new_stmt = new_stmt.where(getattr(model, key) == value)
#         return LoaderComposer(self.loader, stmt=new_stmt)

#     def skip(self, offset: int) -> "LoaderComposer":
#         """
#         Nastaví offset (počet řádků k přeskočení).

#         :param offset: Počet řádků, které se mají přeskočit.
#         :return: Nová instance LoaderComposer s aplikovaným offsetem.
#         """
#         return LoaderComposer(self.loader, stmt=self.stmt.offset(offset))

#     def limit(self, limit: int) -> "LoaderComposer":
#         """
#         Nastaví limit (maximální počet vrácených řádků).

#         :param limit: Počet řádků, které se mají vrátit.
#         :return: Nová instance LoaderComposer s aplikovaným limitem.
#         """
#         return LoaderComposer(self.loader, stmt=self.stmt.limit(limit))

#     def join(
#         self,
#         target: Any,
#         onclause: Optional[BinaryExpression] = None,
#         isouter: bool = False,
#         full: bool = False
#     ) -> "LoaderComposer":
#         """
#         Přidá JOIN klauzuli do SQLAlchemy select statementu.
#         Příklad použití: composer.join(OtherModel, onclause=Model.id == OtherModel.model_id)

#         :param target: Cílový model nebo tabulka, se kterou se má join provést.
#         :param onclause: Podmínka pro spojení (např. Model.id == OtherModel.model_id).
#         :param isouter: Pokud je True, vytvoří OUTER JOIN, jinak INNER JOIN.
#         :param full: Pokud je True, vytvoří FULL JOIN (v závislosti na podpoře databáze).
#         :return: Nová instance LoaderComposer s rozšířeným select statementem obsahujícím JOIN.
#         """
#         new_stmt = self.stmt.join(target, onclause=onclause, isouter=isouter, full=full)
#         return LoaderComposer(self.loader, stmt=new_stmt)

#     def execute_select(self) -> Any:
#         """
#         Spustí aktuální SQLAlchemy select statement pomocí loader.executeselect.
        
#         :return: Výsledek dotazu (ve formě seznamu DB modelů).
#         """
#         return self.loader.execute_select(self.stmt)
