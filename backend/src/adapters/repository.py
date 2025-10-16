import abc
from domain import model

class AbstractRepository(abc.ABC):
    def __init__(self, cache):
        self.cache = cache

    def get(self, conversation_id: model.ChatConversation) -> list[model.ChatConversation]:
        return self._get(conversation_id)

    @abc.abstractmethod
    def _add(self, conversation: model.ChatConversation) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def _multi_add(self, conversations: list[model.ChatConversation]) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, conversation_id: int) -> list[model.ChatConversation]:
        raise NotImplementedError
    
    @abc.abstractmethod
    def _clean(self)->None:
        raise NotImplementedError

class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session, cache):
        super().__init__(cache)
        self.session = session
    
    def _add(self, conversation: model.ChatConversation):
        self.session.add(conversation)

    def _multi_add(self, conversations: list[model.ChatConversation]):
        self.session.add_all(conversations)

    def _get(self, conversation_id) -> list[model.ChatConversation]:
        return (self.session.query(model.ChatConversation)
                .filter(model.ChatConversation.conversation_id == conversation_id)
                .order_by(model.ChatConversation.created_at)
                .all()
        )
    
    def _clean(self)->None:
        self.session.query(model.ChatConversation).delete()