# Agent Identity Module

class Agent:
    """Agent 身份和配置"""
    
    def __init__(self, agent_id: str, name: str, company: str, personality: dict = None):
        self.id = agent_id
        self.name = name
        self.company = company
        self.personality = personality or {}
        self.skills = []
        self.reputation = 0
        
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "company": self.company,
            "personality": self.personality,
            "skills": self.skills,
            "reputation": self.reputation
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Agent":
        agent = cls(
            agent_id=data["id"],
            name=data["name"],
            company=data["company"],
            personality=data.get("personality", {})
        )
        agent.skills = data.get("skills", [])
        agent.reputation = data.get("reputation", 0)
        return agent
    
    def introduce(self) -> str:
        """自我介绍"""
        intro = f"你好，我是 {self.name}，来自 {self.company}。"
        if self.personality.get("style"):
            intro += f"\n我的风格: {self.personality['style']}"
        return intro


class AgentRegistry:
    """简单的 Agent 注册表"""
    
    def __init__(self, registry_file: str = "agents/registry.yaml"):
        self.registry_file = registry_file
        self.agents = {}
        self._load()
    
    def _load(self):
        """从 YAML 文件加载"""
        import yaml
        import os
        if os.path.exists(self.registry_file):
            with open(self.registry_file, 'r') as f:
                data = yaml.safe_load(f) or {}
                agents_list = data.get('agents', [])
                for agent_data in agents_list:
                    agent_id = agent_data.get('id')
                    if agent_id:
                        agent = Agent.from_dict(agent_data)
                        self.agents[agent_id] = agent
    
    def _save(self):
        """保存到 YAML 文件"""
        import yaml
        import os
        os.makedirs(os.path.dirname(self.registry_file), exist_ok=True)
        data = {
            'agents': [agent.to_dict() for agent in self.agents.values()]
        }
        with open(self.registry_file, 'w') as f:
            yaml.dump(data, f, default_flow_style=False)
    
    def register(self, agent: Agent):
        """注册 Agent"""
        self.agents[agent.id] = agent
        self._save()
    
    def get(self, agent_id: str) -> Agent:
        """获取 Agent"""
        return self.agents.get(agent_id)
    
    def list_all(self) -> list:
        """列出所有 Agent"""
        return list(self.agents.values())