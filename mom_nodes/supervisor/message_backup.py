
# mom_nodes/supervisor/message_backup.py

class MessageBackup:
    def __init__(self):
        self.backup_queues = {}
        self.backup_topics = {}

    def backup_queue(self, name, message):
        if name not in self.backup_queues:
            self.backup_queues[name] = []
        self.backup_queues[name].append(message)

    def get_queue_backup(self, name):
        return self.backup_queues.get(name, [])

    def backup_topic(self, name, message):
        if name not in self.backup_topics:
            self.backup_topics[name] = []
        self.backup_topics[name].append(message)

    def get_topic_backup(self, name):
        return self.backup_topics.get(name, [])

backup = MessageBackup()
