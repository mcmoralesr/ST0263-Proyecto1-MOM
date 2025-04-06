# mom1/message_broker.py

from typing import Dict, List, Optional
from collections import defaultdict


class MessageBroker:
    def __init__(self):
        self.queues: Dict[str, List[str]] = defaultdict(list)
        self.queue_subscribers: Dict[str, bool] = defaultdict(bool)

        self.topics: Dict[str, Dict[str, List[str]]] = defaultdict(lambda: defaultdict(list))
        self.topic_subscribers: Dict[str, List[str]] = defaultdict(list)

    # === QUEUES (solo un consumidor por mensaje) ===

    def publish_to_queue(self, queue_name: str, message: str):
        self.queues[queue_name].append(message)

    def subscribe_to_queue(self, queue_name: str):
        self.queue_subscribers[queue_name] = True

    def consume_from_queue(self, queue_name: str) -> Optional[str]:
        if not self.queues[queue_name]:
            return None
        return self.queues[queue_name].pop(0)

    # === TOPICS (broadcast con clave) ===

    def publish_to_topic(self, topic_name: str, message: str):
        for key in self.topics[topic_name]:
            self.topics[topic_name][key].append(message)

    def subscribe_to_topic(self, topic_name: str, key: str):
        if key not in self.topics[topic_name]:
            self.topics[topic_name][key] = []

    def get_topic_messages(self, topic_name: str, key: str) -> List[str]:
        return self.topics[topic_name].get(key, [])

    # === INFO ===

    def list_queues(self) -> List[str]:
        return list(self.queues.keys())

    def list_topics(self) -> List[str]:
        return list(self.topics.keys())


# Singleton instance
broker = MessageBroker()