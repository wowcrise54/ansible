import os
import ansible_runner
from typing import List, Dict
import logging

class AnsibleService:
    def __init__(self):
        # Получаем абсолютный путь к корню проекта
        self.base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.playbooks_dir = os.path.join(self.base_dir, "ansible", "playbooks")
        self.inventory_file = os.path.join(self.base_dir, "ansible", "inventory", "hosts.yml")
        
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)
        
        # Логируем пути для отладки
        self.logger.debug(f"Base dir: {self.base_dir}")
        self.logger.debug(f"Playbooks dir: {self.playbooks_dir}")
        self.logger.debug(f"Inventory file: {self.inventory_file}")

    def get_available_playbooks(self) -> List[str]:
        """Получить список доступных плейбуков"""
        playbooks = []
        for file in os.listdir(self.playbooks_dir):
            if file.endswith('.yml'):
                playbooks.append(file)
        return playbooks

    async def execute_playbook(self, playbook_name: str, host: str, extra_vars: Dict = None) -> Dict:
        """Выполнить выбранный плейбук на указанном хосте"""
        playbook_path = os.path.join(self.playbooks_dir, playbook_name)
        
        self.logger.debug(f"Executing playbook: {playbook_path}")
        self.logger.debug(f"Using inventory: {self.inventory_file}")
        self.logger.debug(f"Target host: {host}")
        
        if not os.path.exists(playbook_path):
            raise FileNotFoundError(f"Playbook не найден: {playbook_path}")
        
        if not os.path.exists(self.inventory_file):
            raise FileNotFoundError(f"Inventory file не найден: {self.inventory_file}")

        extra_vars = extra_vars or {}
        extra_vars['target_host'] = host

        try:
            result = ansible_runner.run(
                private_data_dir='/tmp',
                playbook=playbook_path,
                inventory=self.inventory_file,
                extravars=extra_vars,
                debug=True
            )
            
            if result.rc != 0:
                self.logger.error(f"Ansible execution failed: {result.stderr.read()}")
                
            return {
                "status": "success" if result.rc == 0 else "failed",
                "output": result.stdout.read() if result.stdout else str(result.stderr.read()),
                "playbook_name": playbook_name,
                "host": host
            }
        except Exception as e:
            self.logger.exception("Error executing ansible playbook")
            return {
                "status": "failed",
                "output": str(e),
                "playbook_name": playbook_name,
                "host": host
            } 